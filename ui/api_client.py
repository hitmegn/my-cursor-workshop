from typing import Any, Dict, Optional

import httpx

from api.models import ProductModel

BASE_URL = "http://localhost:8000"


async def get_product(product_id: int) -> Optional[ProductModel]:
    """商品IDを指定してAPIから商品情報を取得する"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/items/{product_id}")
        if response.status_code == 200:
            return ProductModel(**response.json())
        return None


async def create_product(name: str, price: float) -> Optional[ProductModel]:
    """新しい商品をAPI経由で登録する"""
    # APIの`create_item`はProductModelを期待するが、
    # 実際にはnameとpriceのみで動作するはず。
    # idとcreated_atはサーバー側で生成される。
    product_data = {"name": name, "price": price}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{BASE_URL}/items", json=product_data)
            response.raise_for_status()  # 2xx以外はHTTPErrorを発生させる
            return ProductModel(**response.json())
        except (httpx.HTTPStatusError, httpx.RequestError):
            return None
