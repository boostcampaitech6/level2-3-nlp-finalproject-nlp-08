# How to run

```
docker-compose up
```
- run React App only : [readme](/frontend/README.md)
- run FastAPI only : [readme](/backend/README.md)
- run Airflow only : [readme](/airflow/README.md)

# 프로젝트 개요
 사용자가 읽고자 하는 문서를 입력으로 제공하면 지문에서 중요한 키워드를 추출한 후, 해당 키워드를 정답으로 하는 문제를 생성하여 독자의 읽기 활동을 도와주는 웹 서비스입니다.
![Screenshot 2024-03-21 at 4 27 07 PM](https://github.com/boostcampaitech6/level2-3-nlp-finalproject-nlp-08/assets/76895949/f5c45fc8-116f-43f8-8ba4-d709a81a50f7)
<img src="https://github.com/boostcampaitech6/level2-3-nlp-finalproject-nlp-08/assets/76895949/7f038ec9-9156-4da3-a20b-8e8466290643" width="500">
<img src="https://github.com/boostcampaitech6/level2-3-nlp-finalproject-nlp-08/assets/76895949/2031505c-16fd-4916-b26d-8ffae2e6ac68" width="500">

<img src="https://github.com/boostcampaitech6/level2-3-nlp-finalproject-nlp-08/assets/76895949/f4fcff8a-942d-4867-9ebd-1c41fb858059" width="500">
<img src="https://github.com/boostcampaitech6/level2-3-nlp-finalproject-nlp-08/assets/76895949/e2c75777-00b5-4349-8bdc-58437deba7ec" width="500">

# Models
### 1. 어떻게 사용자의 지문에서 의미 있는 질문을 뽑아낼 수 있을까?
 사용자가 읽고자 하는 독해 지문에서 어떤 질문을 해주어야 할까요? 시험 문제가 중요한 내용을 묻듯이 모델이 지문에서 중요한 단어에 대한 질문을 해주길 원했습니다.
지문의 임베딩 벡터와 유사한 단어를 keybert가 뽑도록하고 해당 키워드를 정답으로 하는 좋은 품질의 질문 문장을 생성하도록 했습니다.
지문, 질문, 정답으로 구성된 korquad 데이터셋을 사용했습니다.

### 2. 지문에서 중요한 키워드 추출
<img width="911" alt="Screenshot 2024-03-21 at 4 06 55 PM" src="https://github.com/boostcampaitech6/level2-3-nlp-finalproject-nlp-08/assets/76895949/0f98fd57-4ed1-4296-b5e8-d0711b5ae198">
  
  Keybert는 Document에서 N-gram 단어들을 추출하여 임베딩한 뒤, 문서 전체를 임베딩한 값과 코사인 유사도를 계산하는 Bert 기반 모델입니다.
문서 전체 내용과 유사도가 높은 단어들을 Keyword로서 추출합니다. 문장의 중요 키워드들은 사용자가 문서를 잘 독해했는지 평가하는 문제의 정답으로 사용됩니다.


### 3. 해당 키워드를 정답으로 하는 질문 문장 생성
<img width="955" alt="Screenshot 2024-03-21 at 4 08 44 PM" src="https://github.com/boostcampaitech6/level2-3-nlp-finalproject-nlp-08/assets/76895949/85f7cfe3-18bd-49c3-b1e4-067f5ef6ebc0">
 
  사용자가 읽고자하는 지문과 앞서 keybert에서 추출한 단어를 special token으로 이어 붙여 입력을 구성했고 
모델이 출력하는 output이 정답 질문과 유사하도록 학습했습니다. 
모델이 물어보아야하는 주제에 대해 ‘질문의 목적’이 되는 정답은 keybert에게 위임할 수 있게 되었기 때문에 BART는 문장 품질이 좋은가에만 집중하여 개선을 시도했습니다.


# Service Architecture
<img width="989" alt="Screenshot 2024-03-21 at 4 10 17 PM" src="https://github.com/boostcampaitech6/level2-3-nlp-finalproject-nlp-08/assets/76895949/06fdfded-5936-4e2f-98f3-cc50c19b9983">

<img width="995" alt="Screenshot 2024-03-21 at 4 10 39 PM" src="https://github.com/boostcampaitech6/level2-3-nlp-finalproject-nlp-08/assets/76895949/ba5c691f-317f-4444-9de6-2b2a6229cc90">

모델이 사용자의 피드백과 함께 계속해서 개선되는 파이프라인을 구축했습니다. 사용자는 제공된 질문을 풀때 질문의 품질이 맘에 들지 않은 경우 ‘싫어요' 버튼을 통해 피드백을 제공할 수 있습니다. 
이렇게 사용자의 의견이 반영된 피드백은 데이터베이스에 저장되고, airflow에서 주기적으로 데이터베이스를 확인해 특정 개수 이상의 데이터가 추가되면 사용자 피드백 데이터를 수집합니다. 
그리고 그중 지문, 정답 데이터를 사용해 chatGPT 를 통해서 해당 지문과 정답에 적합한 새로운 질문을 생성합니다. 
그렇게 구축한 사용자 피드백 학습데이터를 train, valid, test 데이터로 나누어 지금의 모델을 재학습하고 평가합니다. 
학습을 마친 모델은 Hugging face 허브에 업로드되고 fastapi서버는 이곳에서 사용자 피드백이 반영된 모델을 내려받아 탑재하게 됩니다.

<img width="827" alt="Screenshot 2024-03-21 at 4 11 19 PM" src="https://github.com/boostcampaitech6/level2-3-nlp-finalproject-nlp-08/assets/76895949/a895b33b-86ad-40e2-bd17-c9416569035a">




