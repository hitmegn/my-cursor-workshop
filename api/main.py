from fastapi import FastAPI
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """ヘルスチェックのレスポンスモデル"""

    status: str


app = FastAPI(
    title="商品管理API",
    description="シンプルな商品管理機能を持つREST APIです。",
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """APIのヘルスチェック"""
    return HealthResponse(status="ok")
