! airflow 2.8.3 -> python 3.9 버전 이하만 지원

## 추가로 설치가 필요한 라이브러리

```Shell
pip install 'apache-airflow-providers-postgres'
pip install openai
```

## Connection 설정 방법

1. airflow 웹 인터페이스에 접속
2. 상단 메뉴바에서 Admin > Connections
3. '+' 버튼 클릭
4. 필요한 부분 작성
    - connection id: 코드에는 my_postgres 사용중. 원하시는 아이디 작성하시고, 코드 수정하셔도 됩니다.
    - connection type: postgres 선택. postgres 가 없는 경우, 위의 라이브러리 설치 여부와 Python 버전 확인 부탁드립니다.
    - host: localhost
    - database: testdb
    - login: 데이터베이스의 postgresql 유저 이름. postgresql 셸에서 데이터베이스에 접속 후 \c 로 확인 가능.
    - password: 위의 유저에 비밀번호가 설정되어 있는 경우 사용. 없으면 공백.
    - port: postgresql 에서 사용하는 포트 번호
5. 저장

## Varible 설정 방법

1. airflow 웹 인터페이스에 접속
2. 상단 메뉴바에서 Admin > Variables
3. '+' 버튼 클릭
4. 필요한 부분 작성
    - key: 코드에서는 last checked time 사용중. 원하는 변수명 사용하고 코드 수정하셔도 됩니다.
    - val: 변수에 저장할 값. 초기값은 1970-01-01 00:00:00 형식으로 원하시는 날짜로 사용해주세요.
    - description: 변수 설명. 생략 가능.
5. 저장