from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from httpx import AsyncClient


async def test_health(client: "AsyncClient") -> None:
    """ヘルスチェックエンドポイントのテスト"""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_create_product_returns_201(client: "AsyncClient") -> None:
    """商品作成が成功すると201を返す"""
    response = await client.post("/items", json={"name": "テスト商品", "price": 1000})
    assert response.status_code == 201


async def test_create_product_returns_created_product(client: "AsyncClient") -> None:
    """作成した商品の情報を返す"""
    response = await client.post("/items", json={"name": "テスト商品", "price": 1000})
    data = response.json()
    assert data["name"] == "テスト商品"
    assert data["price"] == 1000
    assert "id" in data
    assert "created_at" in data


async def test_create_product_with_empty_name_returns_422(client: "AsyncClient") -> None:
    """商品名が空の場合、422エラーを返す"""
    response = await client.post("/items", json={"name": "", "price": 1000})
    assert response.status_code == 422


async def test_create_product_with_negative_price_returns_422(
    client: "AsyncClient",
) -> None:
    """価格が0以下の場合、422エラーを返す"""
    response = await client.post("/items", json={"name": "商品", "price": -100})
    assert response.status_code == 422
