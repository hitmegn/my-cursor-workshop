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


async def test_get_product_returns_200(client: "AsyncClient") -> None:
    """存在する商品IDを指定した場合、200を返す"""
    # Arrange: 事前に商品を作成
    create_response = await client.post("/items", json={"name": "取得用商品", "price": 500})
    product_id = create_response.json()["id"]

    # Act: 商品を取得
    get_response = await client.get(f"/items/{product_id}")

    # Assert: ステータスコードを検証
    assert get_response.status_code == 200


async def test_get_product_returns_correct_product(client: "AsyncClient") -> None:
    """存在する商品IDを指定した場合、正しい商品情報を返す"""
    # Arrange: 事前に商品を作成
    create_response = await client.post("/items", json={"name": "取得用商品", "price": 500})
    created_product = create_response.json()
    product_id = created_product["id"]

    # Act: 商品を取得
    get_response = await client.get(f"/items/{product_id}")
    fetched_product = get_response.json()

    # Assert: 内容を検証
    assert fetched_product == created_product


async def test_get_product_with_nonexistent_id_returns_404(
    client: "AsyncClient",
) -> None:
    """存在しない商品IDを指定した場合、404を返す"""
    # Act: 存在しないIDで商品を取得
    response = await client.get("/items/9999")  # 存在し得ないID

    # Assert: ステータスコードを検証
    assert response.status_code == 404
