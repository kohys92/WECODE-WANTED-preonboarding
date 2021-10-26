# WECODE x WANTED Backend Preonboarding 선발 과제

## Noticeboard app CRUD API (게시판 CRUD API)

### Users 
- 유저 생성 및 로그인
- 유효성, 중복, 암호화
  - 정규식 표현을 사용해 email과 password 형식 정의
  (email: @와 .이 포함된 이메일 형식)
  (password: 대문자,소문자,숫자,특수문자 포함 8자 이상 최대 20자)  
- 인증 & 인가 기능 구현
  - Bcrypt로 비밀번호를 암호화하고 JWT 토큰을 로그인 시 발행하여 인증, 인가 구현
  
### Posts
- 글 작성, 글 확인, 글 목록 확인, 글 수정, 글 삭제
  - Create는 로그인 한 유저만 가능 
  - Delete와 Update는 해당 유저의 글만 가능
  - Read는 비회원도 글 확인 가능
  - Read pagination 구현

### Database
- in-memory database로 구현
  - sqlite3
  

## Install

    pip install -r requirements.txt

# REST API

### 회원가입
- Endpoint
```
/users/signup
```
- Request
```
POST "http://127.0.0.1:8000/users/signup HTTP/1.1"

{
    "username" : "tester7",
    "email" : "test7@gmail.com",
    "password" : "Aaaa123!@"
}
```

- Response
```
{
    "message": "USER CREATED"
}
```

### 로그인
- Endpoint
```
/users/login
```

- Request
```
POST "http://127.0.0.1:8000/users/login HTTP/1.1"

{
    "username" : "tester7",
    "password" : "Aaaa123!@"
}
```

- Response
```
{
    "message": "SUCCESS",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Nn0.GN7V9i8DJCo1yDOOUip5gB1zinfdfgOfOTBo9gFndfI"
}
```

### 게시글 작성
- Endpoint
```
/posts
```

- Request
```
POST "http://127.0.0.1:8000/posts HTTP/1.1"

{
    "title" : "WECODE x WANTED",
    "content" : "프리온보딩 선발 과제"
}
```

- Response
```
{
    "message": "CREATED",
    "data": {
        "title": "WECODE x WANTED",
        "author": "tester7",
        "content": "프리온보딩 선발 과제",
        "created_at": "2021-10-26T17:17:24.038",
        "updated_at": "2021-10-26T17:17:24.038"
    }
}
```

### 게시글 확인
- Endpoint
```
/posts/post_id
```
- Request
```
GET "http://127.0.0.1:8000/posts/14 HTTP/1.1"
```

- Response
```
{
    "data": {
        "title": "WECODE x WANTED",
        "author": "tester7",
        "content": "프리온보딩 선발 과제",
        "created_at": "2021-10-26 17:23:11",
        "updated_at": "2021-10-26 17:23:11"
    }
}
```

### 게시글 목록 확인 (pagination)
- Endpoint
```
/posts/list?limit=5&offset=0
```

- Rquest
```
GET "http://127.0.0.1:8000/posts/list?limit=5&offset=0 HTTP/1.1"
```

- Response
```
{
    "count": 5,
    "data": [
        {
            "title": "Hello this is test title 222",
            "author": "test_admin",
            "content": "test 456 456",
            "created_at": "2021-10-25 01:24:30",
            "updated_at": "2021-10-25 01:24:30"
        },
        {
            "title": "Test post 1",
            "author": "test_123",
            "content": "This is first test post 1",
            "created_at": "2021-10-25 02:12:23",
            "updated_at": "2021-10-25 02:12:23"
        },
        {
            "title": "Test post 2",
            "author": "test_123",
            "content": "This is first test post 2",
            "created_at": "2021-10-25 02:12:56",
            "updated_at": "2021-10-25 02:12:56"
        },
        {
            "title": "Test post 5",
            "author": "test_123",
            "content": "This is first test post 5",
            "created_at": "2021-10-25 08:06:37",
            "updated_at": "2021-10-25 08:06:37"
        },
        {
            "title": "Test post 6",
            "author": "test_123",
            "content": "This is test post 7",
            "created_at": "2021-10-25 08:06:59",
            "updated_at": "2021-10-25 08:06:59"
        }
    ]
}
```

### 게시글 수정
- Endpoint
```
/posts/post_id
```

- Request
```
PATCH "http://127.0.0.1:8000/posts/14 HTTP/1.1"

{
    "content" : "프리온보딩 과제 ---> 내용 업데이트 확인"
}
```

- Response
```
{
    "message": "UPDATED SUCCESSFULLY"
}
```

### 게시글 삭제
- Edpoint
```
/posts/post_id
```
- Rquest
```
DELETE "http://127.0.0.1:8000/posts/14 HTTP/1.1"
```
- Response
```
{
    "message": "POST DELETED"
}
```
