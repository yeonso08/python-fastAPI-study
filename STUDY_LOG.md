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

### 다음 목표
- [ ] `pytest` + FastAPI `TestClient`로 자동화 테스트
- [ ] Alembic으로 DB 마이그레이션 관리
- [ ] PATCH(부분 수정) vs PUT(전체 수정) 차이 다뤄보기

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

## 참고
- 상세 설명은 벨로그 시리즈 "[FastAPI 스터디 N편] 프론트엔드 개발자가 처음 백엔드를 만들어보다" 참고
  - [1편 — 환경설정 ~ DB 연동](https://velog.io/@hjng0825/FastAPI-스터디-1편-프론트엔드-개발자가-처음-백엔드를-만들어보다-환경설정-DB-연동)
  - [2편 — CRUD 완성 편](https://velog.io/@hjng0825/FastAPI-스터디-2편-프론트엔드-개발자가-처음-백엔드를-만들어보다-CRUD-완성-편)
