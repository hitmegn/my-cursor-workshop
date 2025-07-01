from fastapi import FastAPI, HTTPException, status
from models import ProductModel
from pydantic import BaseModel, Field
from storage import InMemoryStorage


class HealthResponse(BaseModel):
    """ヘルスチェックのレスポンスモデル"""

    status: str


app = FastAPI(
    title="商品管理API",
    description="シンプルな商品管理機能を持つREST APIです。",
    version="0.1.0",
)

storage = InMemoryStorage()


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """APIのヘルスチェック"""
    return HealthResponse(status="ok")


class CreateProductRequest(BaseModel):
    """商品作成リクエストモデル"""

    name: str = Field(..., min_length=1, description="商品名")
    price: float = Field(..., gt=0, description="単価")


@app.post(
    "/items",
    response_model=ProductModel,
    status_code=status.HTTP_201_CREATED,
    description="新しい商品を作成します。",
)
async def create_product(product_data: CreateProductRequest) -> ProductModel:
    """商品を作成する"""
    return storage.create_product(name=product_data.name, price=product_data.price)


@app.get(
    "/items/{product_id}",
    response_model=ProductModel,
    description="指定されたIDの商品情報を取得します。",
)
async def get_product(product_id: int) -> ProductModel:
    """商品を取得する"""
    product = storage.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product
