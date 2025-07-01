import json

import pytest
import respx
from httpx import Response

from api.models import ProductModel
from ui.api_client import BASE_URL, create_product, get_product

# このモジュールのすべてのテストをanyioで実行するようマーク
pytestmark = pytest.mark.anyio


@respx.mock
async def test_get_product_success() -> None:
    """get_productが成功時にProductModelを返すことをテストする"""
    mock_product_data = {
        "id": 1,
        "name": "Test Product",
        "price": 100.0,
        "created_at": "2023-01-01T00:00:00",
    }
    respx.get(f"{BASE_URL}/items/1").mock(return_value=Response(200, json=mock_product_data))

    product = await get_product(1)

    assert isinstance(product, ProductModel)
    assert product.id == 1
    assert product.name == "Test Product"


@respx.mock
async def test_get_product_not_found() -> None:
    """get_productが存在しないIDでNoneを返すことをテストする"""
    respx.get(f"{BASE_URL}/items/999").mock(return_value=Response(404))

    product = await get_product(999)

    assert product is None


@respx.mock
async def test_create_product_success() -> None:
    """create_productが成功時にProductModelを返すことをテストする"""
    request_data = {"name": "New Product", "price": 150.0}
    response_data = {
        "id": 2,
        "name": "New Product",
        "price": 150.0,
        "created_at": "2023-01-02T00:00:00",
    }
    respx.post(f"{BASE_URL}/items").mock(return_value=Response(201, json=response_data))

    new_product = await create_product(name="New Product", price=150.0)

    assert isinstance(new_product, ProductModel)
    assert new_product.id == 2
    assert new_product.name == "New Product"
    # モックが正しいリクエストデータで呼び出されたかを確認
    last_request = respx.calls.last.request
    assert last_request is not None
    assert json.loads(last_request.content) == request_data


@respx.mock
async def test_create_product_validation_error() -> None:
    """create_productがバリデーションエラーでNoneを返すことをテストする"""
    respx.post(f"{BASE_URL}/items").mock(
        return_value=Response(422, json={"detail": "Validation Error"})
    )
    product = await create_product(name="", price=-100)  # 不正なデータ
    assert product is None


@respx.mock
async def test_create_product_server_error() -> None:
    """create_productがサーバーエラーでNoneを返すことをテストする"""
    respx.post(f"{BASE_URL}/items").mock(return_value=Response(500))
    product = await create_product(name="Good Product", price=100)
    assert product is None
