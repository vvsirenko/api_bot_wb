from concurrent.futures import ThreadPoolExecutor

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import Product

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


async def save_product_to_db(session: AsyncSession, product: Product):
    try:
        async with session.begin():
            query = select(Product).where(Product.artikul == product.artikul)
            result = await session.execute(query)
            obj = result.scalars().first()
            if obj:
                obj.name = product.name
                obj.price = product.price
                obj.rating = product.rating
                obj.total_quantity = product.total_quantity
                await session.flush()
            else:
                obj = product
                session.add(obj)
                await session.flush()
            return obj
    except Exception as exp:
        await session.rollback()
        raise exp


class CustomScheduler:

    def __init__(self, store_url: str):
        self.store_url = store_url
        self.scheduler = self._create_scheduler()

    def _create_scheduler(self) -> AsyncIOScheduler:
        jobstores = {'default': SQLAlchemyJobStore(url=self.store_url)}
        executors = {'default': ThreadPoolExecutor(10)}
        scheduler = AsyncIOScheduler(jobstores=jobstores, executors=executors)
        return scheduler

    def add_job(self, other):
        self.scheduler.add_job(
            other, 'interval',
            minutes=30, id='update_data_job',
            replace_existing=True
        )

    def start(self):
        self.scheduler.start()

