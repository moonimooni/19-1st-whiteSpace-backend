# Team WhiteSpace

## 🖥 프로젝트 소개

React & Django를 사용한 '공백' 웹사이트 클론

## 📅 프로젝트 기간

2021.04.12 ~ 2021.04.23

## 🎥 프로젝트 시연영상

[https://vimeo.com/540894798](https://vimeo.com/540894798)

## 👩🏻‍💻🧑🏻‍💻 프로젝트 참가자 (Front & Back)

🔜 FrontEnd

- 김남선, 김동현, 박단비

🔙 BackEnd

- 문희원, 홍태경

## 🔧 기술 스택

- FrontEnd

    ![HTML](https://img.shields.io/badge/-HTML/CSS-E44D26)

    ![https://img.shields.io/badge/-SCSS-ff69b4](https://img.shields.io/badge/-SCSS-ff69b4)

    ![https://img.shields.io/badge/-JavaScript(ES6%2B)-F0DB4D](https://img.shields.io/badge/-JavaScript(ES6%2B)-F0DB4D)

    ![https://img.shields.io/badge/-React-blue](https://img.shields.io/badge/-React-blue)

- BackEnd

    ![https://img.shields.io/badge/-Python-376FA0](https://img.shields.io/badge/-Python-376FA0)

    ![https://img.shields.io/badge/-Django-043829](https://img.shields.io/badge/-Django-043829)

    ![https://img.shields.io/badge/-CORS%20Header-F0DB4D](https://img.shields.io/badge/-CORS%20Header-F0DB4D)

    ![https://img.shields.io/badge/-Bcrypt-2A334C](https://img.shields.io/badge/-Bcrypt-2A334C)

    ![https://img.shields.io/badge/-PyJWT-black](https://img.shields.io/badge/-PyJWT-black)

    ![https://img.shields.io/badge/-MySQL-DD8A00](https://img.shields.io/badge/-MySQL-DD8A00)

    ![https://img.shields.io/badge/-AqeuryTool-6A9CA7](https://img.shields.io/badge/-AqeuryTool-6A9CA7)
    
    ![https://img.shields.io/badge/-RDS-brightgreen](https://img.shields.io/badge/-RDS-brightgreen)

    ![https://img.shields.io/badge/-S3-DA5041](https://img.shields.io/badge/-S3-DA5041)
    
    ![https://img.shields.io/badge/-EC2-orange](https://img.shields.io/badge/-EC2-orange)
    

- 협업 도구

    ![https://img.shields.io/badge/-Slack-D91D57](https://img.shields.io/badge/-Slack-D91D57)

    ![https://img.shields.io/badge/-Git-black](https://img.shields.io/badge/-Git-black)

    ![https://img.shields.io/badge/-Trello-036AA7](https://img.shields.io/badge/-Trello-036AA7)

---

# ⭐️ 팀 중 맡은 역할

## 🌱 Backend

### 모델링 구축

- AQuerytool을 활용한 모델링 논의
- MySQL, AWS RDS로 모델 구축

### 회원가입 & 로그인

- bcrypt를 사용한 암호화
- JWT 로그인 구현 및 @decorator를 이용해서 토큰 인증
- Email & 비밀번호 & 전화번호 정규화를 통한 Validation적용

### 네비게이션 바

- 카테고리 정보 보여주기

### 상품 리스트 API

- 가장 많이 팔리는 상품 3가지 필터링
- 카테고리별 상품 필터링
- 검색 키워드에 따른 상품 필터링
- 각 상품별로 신상품인지, 한정재고품인지 체크하는 로직 구현

### 상품 상세 API

- 상품 상세 페이지 (상품 정보: 가격, 사진, 옵션, 재고)
- 각 상품 옵션에 따른 재고 정보 제공
- 제품 설명란 이미지 순서에 맞게 제공

### 장바구니 API

- GET 장바구니 내역 조회
- POST 상품 장바구니에 등록 (개수 포함)
- PATCH 장바구니 상품 수량 변경 및 가격반영(DB에 전부 반영되도록 설정)
- DELETE 장바구니 상품 선택제거 / 전체제거

### 결제 API

- 주문창에서 해당 사용자 정보 확인
- POST 주문시 장바구니에서 해당 상품목록 제거 & 새로운 주문 생성
- 주문 과정 트랜잭션 처리

### 상품 리뷰 API

- 상품 리뷰 보기 (작성자, 평점, 리뷰 내용, 이미지, 구매한 옵션 정보)
- 구매한 사용자만 리뷰 작성 권한 부여
- 리뷰 작성시 이미지 업로드 가능 (Aws S3),
- 해당 상품의 각 평점(1~5) 개수 카운트
- 해당 상품의 총 평균 평점 정보 제공

---

# 👥 후기

[1차 프로젝트 회고 기록](https://fierycoding.tistory.com/70)

---

# ❗️ 레퍼런스

이 프로젝트는 공백 웹사이트를 참조하여 학습목적으로 만들었습니다. 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다. 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.
