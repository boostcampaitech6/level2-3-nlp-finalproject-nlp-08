import re
from kiwipiepy import Kiwi
from sklearn.metrics.pairwise import cosine_similarity
from flair.embeddings import TransformerDocumentEmbeddings
from flair.data import Sentence

def make_embeddings(model_name, keyword, answers_list):
    embedding = TransformerDocumentEmbeddings(model_name)
    keyword = Sentence(keyword)
    embedding.embed(keyword)
    keyword_emb = keyword.embedding.tolist()

    answer_emb = []
    for answer in answers_list:
        answer = Sentence(answer)
        embedding.embed(answer)
        answer_emb.append(answer.embedding.tolist())

    return [keyword_emb], answer_emb

def preprocessing_data(context):
    '''
    html tag 제거, 공백 하나로 대체
    '''
    temp_context = re.sub(r'<[^>]+>', ' ', context)
    temp_context = re.sub(r'\s+', ' ', temp_context)
    final_context = temp_context.lower()
    return final_context

def extracts_nouns(keyword):
    kiwi = Kiwi()
    final_keyword = []
    for k in keyword.split():
        temp_keyword = ''
        for i in kiwi.tokenize(k):
            if i.tag.startswith('N') or i.tag=='SN' and i.tag !='NP':
                temp_keyword += i.form
        final_keyword.append(temp_keyword)
    if len(final_keyword) != 0:
        return ' '.join(final_keyword)

def get_cosine_similarity(model_name, keyword, answers_list):
    keyword_emb, answers_embs = make_embeddings(model_name, keyword, answers_list)
    cosine_list = cosine_similarity(keyword_emb, answers_embs)
    return cosine_list.max()