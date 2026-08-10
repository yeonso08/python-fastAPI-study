# FastAPI 스터디 로그

프론트엔드 개발자가 처음 백엔드(Python + FastAPI + SQLAlchemy + PostgreSQL)를 공부하며 남기는 진행 기록.

## 진행 상황

### Items API (CRUD)
- [x] 환경설정 (FastAPI + SQLAlchemy + PostgreSQL 스캐폴딩)
- [x] Create — `POST /items/`
- [x] Read (전체) — `GET /items/`
- [x] Read (단건) — `GET /items/{item_id}` (404 처리 포함)
- [x] Update — `PUT /items/{item_id}`
- [x] Delete — `DELETE /items/{item_id}`
- [x] DB 접속 정보 `.env`로 분리
- [x] git 저장소 초기화 + 기능 단위 커밋

### 모델 간 관계 (Relationship)
- [x] `Category` 모델 추가 + `Item.category_id` (ForeignKey)
- [x] 양방향 `relationship()` + `back_populates` 연결
- [x] Category용 CRUD 엔드포인트 (`/categories/`)

### 자동화 테스트 (pytest + TestClient)
- [x] `conftest.py` — SQLite in-memory 테스트 DB + `get_db` 의존성 오버라이드
- [x] `category_id` / `item` fixture로 테스트 간 반복 데이터 준비 제거
- [x] Category/Item CRUD 전체 케이스 (성공 + 404) 작성 — 14개 테스트 통과

### PATCH(부분 수정) vs PUT(전체 수정)
- [x] `ItemUpdate` 스키마 — 모든 필드 `Optional[...] = None`
- [x] `PATCH /items/{item_id}` — `exclude_unset=True` + `setattr`로 보낸 필드만 반영
- [x] 부분 수정 시 나머지 필드가 유지되는지 테스트로 검증

### Alembic 마이그레이션
- [x] `alembic init alembic` — 뼈대 생성
- [x] `env.py`에서 `.env`의 `DATABASE_URL` 재사용 + `target_metadata = Base.metadata` 연결
- [x] `alembic revision --autogenerate` — 실제 DB로 `create_all`이 놓친 `items.category_id` 컬럼 누락을 발견
- [x] `alembic upgrade head` — 실제 Postgres DB에 누락된 컬럼 반영

### 다음 목표 — 인증(Authentication)
1단계. User 모델 + 회원가입
- [x] `User` 모델 (email unique, hashed_password) + Alembic 마이그레이션
- [x] 비밀번호 해싱 유틸 (`auth.py`) — 평문 저장 금지
- [x] `UserResponse`에 `hashed_password` 제외 — `response_model`을 정보 유출 방어선으로 사용
- [x] `POST /users/` — 이메일 중복 시 400

2단계. 로그인 + JWT 발급
- [ ] `POST /token` — `OAuth2PasswordRequestForm`으로 로그인 (Swagger의 Authorize 버튼이 이 규격을 씀)
- [ ] 비밀번호 검증 실패 시 401
- [ ] `create_access_token()` — `sub`(누구인지) + `exp`(만료) 넣어 서명, `SECRET_KEY`는 `.env`로 분리

3단계. 라우트 보호
- [ ] `get_current_user` 의존성 — 토큰 디코드 → DB 조회, 없거나 만료면 401
- [ ] `POST` / `PATCH` / `DELETE /items/`에 적용 (`GET`은 공개로 두고 대비)
- [ ] `Depends`가 DB 세션뿐 아니라 인증에도 쓰이는 범용 장치임을 확인

4단계. 인증 테스트
- [ ] 토큰 없음 / 잘못된 토큰 → 401 케이스
- [ ] `auth_headers` fixture로 정상 토큰 케이스
- [ ] 인증 추가로 깨진 기존 테스트 14개 복구

### 그 이후 후보
- [ ] `APIRouter`로 파일 분리 (`routers/items.py`, `routers/users.py`) — `main.py` 비대해짐 해소
- [ ] 소유권(`Item.owner_id`) — 내가 만든 것만 수정/삭제, 인증(누구냐) vs 인가(권한 있냐)

## 배운 핵심 개념 (요약)

| 개념 | 한 줄 요약 |
|---|---|
| `Depends(get_db)` | 요청마다 DB 세션을 자동으로 열고 닫아주는 의존성 주입 |
| Path parameter | `/items/{item_id}`처럼 URL 경로에서 값을 받고, 타입 지정 시 자동 검증/변환 |
| `**item.model_dump()` | Pydantic 객체 → dict 변환 후 언패킹해서 모델 생성자에 매핑 |
| `.filter().first() / .all()` | `.filter()`는 조건만 준비, 실제 실행/형태 결정은 `.first()`(단건)·`.all()`(리스트) |
| `HTTPException` | 404 등 에러 상황을 정상적인 HTTP 응답으로 변환해주는 예외 |
| `response_model` | 반환값을 지정한 스키마 모양대로 걸러서 응답 (정보 노출 방지, 문서화, 검증) |
| `db.refresh()` | DB 전체가 아니라 **객체 하나**만 DB 최신값으로 다시 읽어옴 (읽기 전용) |
| 204 vs 200+메시지 | 204는 스펙상 body를 가질 수 없음 — 메시지를 보내려면 200 사용 |
| `ForeignKey` vs `relationship()` | FK는 DB 레벨 제약(숫자 하나), `relationship()`은 ORM 레벨 편의 기능(진짜 객체로 접근) |
| `back_populates` | 양쪽 relationship을 서로 짝지어줌 — 한쪽 변경 시 파이썬 메모리 상 반대쪽도 동기화 |
| `from_attributes = True` | Pydantic이 dict가 아니라 `.속성` 접근 객체(SQLAlchemy ORM 객체)로부터도 값을 채울 수 있게 허용 (응답 스키마에만 필요) |
| `TestClient` | 실제 서버(포트)를 안 띄우고 `app` 코드를 직접 호출 — 로직은 100% 실제로 실행됨 |
| `dependency_overrides` | 테스트에서 `get_db`를 실제 DB 대신 테스트용 DB로 바꿔치기 |
| `StaticPool` | SQLite in-memory는 커넥션마다 별도 DB가 생김 → 커넥션을 하나로 고정해야 테이블이 유지됨 (없으면 `no such table: items`) |
| `pytest.fixture` | pytest판 `Depends()` — 함수 인자 이름으로 선언하면 필요한 순서대로 자동 실행되어 값 주입 |
| 테스트 격리 | 테스트 함수마다 테이블을 새로 만들고 지움 → 테스트끼리 데이터 공유 안 됨 (각자 자기 데이터를 직접 준비해야 함) |
| f-string | `f"/items/{item_id}"` — `{}` 안 변수를 실제 값으로 치환 (앞에 `f` 없으면 글자 그대로 취급됨) |
| `Optional[X] = None` | 필드를 선택값으로 만듦. Update 스키마에서 `None`은 실제 값이 아니라 "이 필드는 안 보냈다"는 신호 |
| `exclude_unset=True` | 없으면 `price`만 보내도 나머지 필드가 `None`으로 덮어써짐 → 클라이언트가 실제로 보낸 필드만 dict로 추출해야 부분 수정이 됨 |
| `setattr(obj, key, value)` | `obj.key = value`를 변수로 된 필드명으로 동적으로 실행 |
| `BaseModel` | Pydantic 기반 클래스. 상속받아야 타입 힌트가 실제 검증/변환 로직으로 동작함 (안 받으면 그냥 힌트일 뿐) |
| `create_all`의 한계 | 테이블이 없을 때만 생성, 이미 있는 테이블의 컬럼 추가/변경은 반영 안 함 → 실제로 `items.category_id` 누락 발견 |
| `alembic revision --autogenerate` | 실제 DB와 `models.py`를 비교해서 차이(diff)를 `upgrade()`/`downgrade()` 코드로 자동 생성 |
| `alembic upgrade head` | 아직 적용 안 된 migration들을 실제 DB에 순서대로 적용 |

## 참고
- 상세 설명은 벨로그 시리즈 "[FastAPI 스터디 N편] 프론트엔드 개발자가 처음 백엔드를 만들어보다" 참고
  - [1편 — 환경설정 ~ DB 연동](https://velog.io/@hjng0825/FastAPI-스터디-1편-프론트엔드-개발자가-처음-백엔드를-만들어보다-환경설정-DB-연동)
  - [2편 — CRUD 완성 편](https://velog.io/@hjng0825/FastAPI-스터디-2편-프론트엔드-개발자가-처음-백엔드를-만들어보다-CRUD-완성-편)
  - [3편 — 관계, 테스트, PATCH, 마이그레이션 편](https://velog.io/@hjng0825/FastAPI-스터디-3편-프론트엔드-개발자가-처음-백엔드를-만들어보다-관계-테스트-PATCH-마이그레이션-편)
