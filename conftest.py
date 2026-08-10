import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from database import Base
from main import app, get_db

# 실제 .env DB 대신 테스트용 SQLite in-memory DB 사용
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    # StaticPool: 커넥션을 하나만 유지 → in-memory DB가 요청마다 새로 생기지 않고 유지됨
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


# main.py의 get_db 의존성을 테스트용 DB로 교체
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def client():
    # 테스트마다 테이블을 새로 만들고, 끝나면 지워서 테스트 간 데이터가 섞이지 않게 함
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def category_id(client):
    # 여러 테스트에서 반복되는 "category부터 만들기"를 한 곳에 모아둔 fixture
    response = client.post("/categories/", json={"name": "전자기기"})
    return response.json()["id"]


@pytest.fixture()
def item(client, category_id):
    # item 하나가 이미 존재하는 상태가 필요한 테스트(조회/수정/삭제)에서 재사용
    response = client.post("/items/", json={
        "name": "Foo",
        "price": 5000,
        "is_available": True,
        "category_id": category_id,
    })
    return response.json()
