import re
# from konlpy.tag import Mecab

def preprocessing_data(context):
    '''
    html tag 제거, 공백 하나로 대체
    '''
    temp_context = re.sub(r'<[^>]+>', ' ', context)
    temp_context = re.sub(r'\s+', ' ', temp_context)
    final_context = temp_context.lower()
    return final_context

# def extracts_nouns(context):
#     context = preprocessing_data(context)
#     mecab = Mecab()
#     nouns = mecab.nouns(context)
#     return nouns