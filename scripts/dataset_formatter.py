from datasets import load_dataset
import argparse

# 옵션 arg 받기
parser = argparse.ArgumentParser()
parser.add_argument('--csvout', help='추출할 csv 파일 이름')
parser.add_argument('--subset', default='train', help='train, test, 혹은 valid ')
parser.add_argument('--column', default='paragraph', help='지문 칼럼의 이름')
parser.add_argument('--dataset', default='lmqg/qg_koquad', help='허깅페이스에서 가져올 데이터셋 이름')
args = parser.parse_args()

# 허깅페이스에서 데이터셋 가져오기
dataset = load_dataset(args.dataset)

#판다스 데이터프레임으로 변환
train_data = dataset[args.subset].to_pandas()

train_data = train_data.rename(columns={args.column: 'paragraph'})

# csv 파일로 추출
if(args.csvout is not None):
    train_data.to_csv(f'./{args.csvout}.csv')