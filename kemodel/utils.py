import re
from konlpy.tag import Kkma
from kiwipiepy import Kiwi

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

