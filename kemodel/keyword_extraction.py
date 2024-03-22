from keybert import KeyBERT
import pandas as pd
import re
from transformers import BertModel, AutoModel
from collections import defaultdict
from tqdm import tqdm
import argparse
import os
import torch

from utils import preprocessing_data, extracts_nouns, get_cosine_similarity
from keybert_model import KeywordExtraction
from flair.embeddings import TransformerDocumentEmbeddings
import flair

if __name__:
    print(flair.device)
    # koquard 데이터 불러오기
    DATA_DIR = '../../data/squad_kor_v1_test_reformatted.csv'
    train_df = pd.read_csv(DATA_DIR)
    temp_df = train_df[['context', 'question', 'answer']]

    # context별로 id 재구성(같은 context -> 같은 id)
    temp_df['id'] = temp_df['context'].astype('category').cat.codes

    # unique한 context 데이터셋 만들기
    temp_dict = defaultdict()
    docs_list = []
    for _, data in tqdm(temp_df.iterrows(), desc='unique한 context 데이터셋 만들기', total = len(temp_df)):
        id = data['id']
        answer = data['answer']
        if id not in temp_dict.keys():
            temp_dict[id] = [answer]
            docs_list.append([id, preprocessing_data(data['context'])])
        else:
            temp_dict[id].append(answer)

    final_dict = defaultdict()
    for id, answer in temp_dict.items():
        final_dict[id] = list(set(answer))
    docs_df = pd.DataFrame(docs_list, columns=['id', 'context'])
    answer_df = pd.DataFrame(list(final_dict.items()), columns = ['id', 'answer'])
    
    # KeyBERT options
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', required=False, default='roberta-base', help='모델 이름')
    parser.add_argument('--num_to_gen', required=False, type=int, default=5, help='생성할 keyword 수')
    # parser.add_argument('--n_gram', required=False, type=int, default=1, help='keyword의 max n gram')
    parser.add_argument('--use_maxsum', required=True, default = True, help='다양성 방법1')
    parser.add_argument('--nr_candidates',required=False, default=3, type=int, help='use_maxsum=True일 경우 고려할 대상 개수')
    parser.add_argument('--use_mmr', required=True, default = True, help='다양성 방법2')
    parser.add_argument('--diversity', required=False, type=float, default=0.1, help='use_mmr=True할 경우 다양성을 얼마나 줄건지(숫자 클수록 다양성 커짐)')
    args = parser.parse_args()
    
    kw_model = KeyBERT()

    keywords_object = KeywordExtraction(kw_model, 
                                        num_to_gen = args.num_to_gen, 
                                        stop_words = None,
                                        use_maxsum=args.use_maxsum, 
                                        nr_candidates=args.nr_candidates,
                                        use_mmr=args.use_mmr,
                                        diversity=args.diversity)
    
    # 키워드 추출
    new_data = []
    for _, data in tqdm(docs_df[:7].iterrows(), desc='keyword extraction', total = len(docs_df)):
        id = data['id']
        context = data['context']
        keywords_candidates = keywords_object.generate_keywords(context, 1)
        keywords_candidates = [extracts_nouns(i) for i in keywords_candidates if len(extracts_nouns(i))>0]
        new_data.append([id, context, set(keywords_candidates)])
    keyword_df = pd.DataFrame(new_data, columns=['id', 'context', 'keyword'])
    
    total_answer = sum(len(answer_df.iloc[i]['answer']) for i in range(len(answer_df)))
    total_keyword = 0
    total_cs_score = 0
    score = 0   # 점수 계산
    # if_keyword_exist = 0    # keyword가 context에 있는지 확인
    cs_limit = 0.7
    for _, data in keyword_df.iterrows():
        id = data['id']
        context_str = str(docs_df[docs_df['id']==id]['context'].values[0])
        for keyword in tqdm(data['keyword'], total=len(data)):
            if keyword in context_str:  # 정답이 context에 있는 경우
                total_keyword += 1
                cs_score = get_cosine_similarity(args.model_name, keyword, answer_df[answer_df['id']==id]['answer'].tolist()[0])
                if (cs_limit <= cs_score) or (keyword in answer_df[answer_df['id']==id]['answer'].tolist()[0]):
                    total_cs_score += cs_score
                    score += 1

    precision = score / total_keyword
    recall = score / total_answer

    f1_score = '{:.4f}'.format(2*precision*recall/(precision+recall))
    # score_rate = '{:.4f}'.format(score/total_keyword)
    # if_keyword_exist = '{:.4f}'.format(if_keyword_exist/total_keyword)
    total_cs_score = '{:.4f}'.format(total_cs_score/total_keyword)
    score_dict = {
        'f1_score':f1_score,
        'cs_score':total_cs_score,
        'model_name':args.model_name, 
        'num_to_gen':args.num_to_gen,
        'use_maxsum':args.use_maxsum, 
        'nr_candidates':args.nr_candidates, 
        'use_mmr':args.use_mmr, 
        'diversity':args.diversity,
        }
    score_df = pd.DataFrame([score_dict])

    #keyword vs answer 비교 csv파일
    merged_df = pd.merge(keyword_df, answer_df, on='id', how='left')

    # merged_df[['id', 'keyword', 'answer', 'context']].to_csv(os.path.join('keyword_answer', f'{only_model}_{args.num_to_gen}_{args.use_maxsum}_{args.nr_candidates}_{args.use_mmr}_{args.diversity}.csv'), index=False)
    merged_df[['id', 'keyword', 'answer', 'context']].to_csv('keyword_answer.csv', index=False)

    file = 'score.csv'
    if os.path.isfile(file):
        with open(file, 'a') as file_data:
            score_df.to_csv(file, mode='a',index=False, header=False)
    else:
        score_df.to_csv(file, index=False)