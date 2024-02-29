from datasets import load_dataset
import argparse

# 옵션 arg 받기
parser = argparse.ArgumentParser()
parser.add_argument('--csvout', help='추출할 csv 파일 이름(확장자 빼고)')
parser.add_argument('--subset', default='train', help='train, test, 혹은 valid ')
parser.add_argument('--answer', default='answer', help='정답 칼럼의 이름')
parser.add_argument('--question', default='question', help='질문 칼럼의 이름')
parser.add_argument('--context', default='paragraph', help='지문 칼럼의 이름')
parser.add_argument('--question_level', default='question_level', help='질문 레벨 칼럼의 이름')
parser.add_argument('--question_type', default='question_type', help='질문 타입 칼럼의 이름')
parser.add_argument('--answer_type', default='answer_type', help='정답 타입 칼럼의 이름')
parser.add_argument('--answer_start', default='answer_start', help='정답 시작지점 칼럼의 이름')
parser.add_argument('--clue_start', default='clue_start', help='답변이 있는 문장의 시작지점 칼럼의 이름')
parser.add_argument('--clue_end', default='clue_end', help='답변이 있는 문장의 끝지점 칼럼의 이름')
parser.add_argument('--dataset', default='lmqg/qg_koquad', help='허깅페이스에서 가져올 데이터셋 이름')
args = parser.parse_args()

# 허깅페이스에서 데이터셋 가져오기
dataset = load_dataset(args.dataset)

# 판다스 데이터프레임으로 변환
train_data = dataset[args.subset].to_pandas()

# 칼럼들의 이름을 변경
col_name_dict = { args.answer : 'answer', args.question:'question', args.context:'context',
                  args.question_level:'question_level', args.question_type:'question_type',
                  args.answer_type:'answer_type', args.answer_start:'answer_start',
                  args.clue_start:'clue_start', args.clue_end:'clue_end' }
for key, val in col_name_dict.items():
    # key 칼럼이 존재하면 이름을 val로 바꿈
    if key in train_data.columns:
        train_data = train_data.rename(columns={key: val})
    # key 칼럼이 존재하지 않으면 새 val 칼럼을 만듬
    else:
        train_data[val] = None

# csv 파일로 추출
if(args.csvout is not None):
    train_data.to_csv(f'./{args.csvout}.csv')
else:
    print("출력할 csv 파일 이름을 넣어주지 않아서 아무것도 출력되지 않습니다")