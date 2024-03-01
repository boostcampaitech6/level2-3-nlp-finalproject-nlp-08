'''
    데이터셋의 형태를 통일된 형태로 바꿔주는 코드
'''
from datasets import load_dataset
import argparse
from tqdm import tqdm

# 옵션 arg 받기
parser = argparse.ArgumentParser()
parser.add_argument('--csvout', help='추출할 csv 파일 이름(확장자 빼고)')
parser.add_argument('--subset', default='train', help='train, test, 혹은 valid ')
parser.add_argument('--dataset', default='lmqg/qg_koquad', help='허깅페이스에서 가져올 데이터셋 이름')
args = parser.parse_args()
# answer = 'answer' # 정답 칼럼의 이름
# question ='question' # 질문 칼럼의 이름'
# context ='paragraph'# 지문 칼럼의 이름'
# question_level = 'question_level' # 질문 레벨 칼럼의 이름
# question_type = 'question_type' # 질문 타입 칼럼의 이름
# answer_type = 'answer_type' # 정답 타입 칼럼의 이름
# answer_start = 'answer_start' # 정답 시작지점 칼럼의 이름
# clue_start = 'clue_start' # 답변이 있는 문장의 시작지점 칼럼의 이름
# clue_end = 'clue_end' # 답변이 있는 문장의 끝지점 칼럼의 이름


# 허깅페이스에서 데이터셋 가져오기
dataset = load_dataset(args.dataset)

# 판다스 데이터프레임으로 변환
train_data = dataset[args.subset].to_pandas()



# 칼럼들의 이름을 변경
# if args.dataset == 'squad_kor_v1':
#     col_name_dict = { answer : 'answer', question:'question', 'paragraph':'context',
#                       question_level:'question_level', question_type:'question_type',
#                       answer_type:'answer_type', answer_start:'answer_start',
#                       clue_start:'clue_start', clue_end:'clue_end' }

if args.dataset == 'lmqg/qg_koquad':
    col_name_dict = { 'answer' : 'answer', 'question':'question', 'paragraph':'context',
                      'question_level':'question_level', 'question_type':'question_type',
                      'answer_type':'answer_type', 'answer_start':'answer_start',
                      'clue_start':'clue_start', 'clue_end':'clue_end' }
    # 칼럼 이름 바꾸거나 생성
    for key, val in col_name_dict.items():
        # key 칼럼이 존재하면 이름을 val로 바꿈
        if key in train_data.columns:
            train_data = train_data.rename(columns={key: val})
        # key 칼럼이 존재하지 않으면 새 val 칼럼을 만듬
        else:
            train_data[val] = None
    
    # answer_start, clue_start, clue_end 칼럼에 값 넣어주기(토큰단위가 아닌 글자단위 인덱스)
    for idx, row in tqdm(train_data.iterrows()):
        clue_start = train_data.loc[idx,'clue_start'] = row.context.find(row.sentence)
        train_data.loc[idx,'clue_end'] = clue_start + len(row.sentence)
        train_data.loc[idx,'answer_start'] = clue_start + row.sentence.find(row.answer)

    # question_level, question_type, answer_type도 값을 넣어줄 수 있다면 넣어주자.
        
    # 불필요한 열 삭제 paragraph_question, sentence, sentence_answer, paragraph_answer, paragraph_sentence, paragraph_id
    train_data.drop(['paragraph_question', 'sentence', 'sentence_answer', 'paragraph_answer', 'paragraph_sentence', 'paragraph_id'], axis=1, inplace=True)

# csv 파일로 추출
if args.csvout is not None:
    train_data.to_csv(f'./{args.csvout}.csv')
else:
    print("출력할 csv 파일 이름을 넣어주지 않아서 아무것도 출력되지 않습니다")