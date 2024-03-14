import re
from konlpy.tag import Kkma

def preprocessing_data(context):
    '''
    html tag 제거, 공백 하나로 대체
    '''
    temp_context = re.sub(r'<[^>]+>', ' ', context)
    temp_context = re.sub(r'\s+', ' ', temp_context)
    final_context = temp_context.lower()
    return final_context

def extracts_nouns(keyword):
    kkma = Kkma()
    for k in keyword.split():
        temp_keyword = ''
        for word, pos in kkma.pos(k):
            if pos.startswith('N'):
                temp_keyword += word
        if len(temp_keyword) != 0:
            return temp_keyword