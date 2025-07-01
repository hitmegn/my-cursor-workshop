from typing import Dict

from .models import ProductModel


class InMemoryStorage:
    """インメモリデータストレージ"""

    def __init__(self) -> None:
        self._data: Dict[int, ProductModel] = {}
        self._next_id: int = 1

    def create_product(self, name: str, price: float) -> ProductModel:
        """新しい商品を作成して保存する"""
        product = ProductModel(id=self._next_id, name=name, price=price)
        self._data[product.id] = product
        self._next_id += 1
        return product

    def get_product(self, product_id: int) -> ProductModel | None:
        """IDで商品を検索する"""
        return self._data.get(product_id)
