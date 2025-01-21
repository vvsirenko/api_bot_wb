from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.utils import save_product_to_db
from app.db.database import get_async_session
from app.db.schemas import ProductCreate, ProductResponse
from app.api.utils import fetch_product_data
from app import config

router = APIRouter(prefix="/api/v1", tags=["Products"])


@router.post("/products", response_model=ProductResponse)
async def create_product(
        product_data: ProductCreate,
        session: AsyncSession = Depends(get_async_session)
):
    product = await fetch_product_data(product_data.artikul, config.PARSED_URL)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    await save_product_to_db(session, product)
    return product

# @router.get("/subscribe/{artikul}", dependencies=[Depends(get_token)])
# async def subscribe_to_product(artikul: int, session: AsyncSession = Depends(get_async_session)):
#     from app.main import scheduler
#     from app.api.models import fetch_product_data
#     from app.jobs import scheduled_task
#     if not scheduler.get_job(str(artikul)):
#         scheduler.add_job(scheduled_task, 'interval', minutes=30, args=[artikul, session], id=str(artikul))
#     return {"message": f"Subscribed to product {artikul}"}