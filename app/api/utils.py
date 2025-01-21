import httpx
import json

from app.db.database import Product


async def __fetch_product_data(artikul: int, url: str) -> list | None:
    url = f"{url}{artikul}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            products = data.get('data', {}).get('products', [])
            return products
        except httpx.HTTPStatusError as e:
            print(f"Error fetching data: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error: {e}")
            return None


async def fetch_product_data(artikul: int, url: str) -> Product | None:
    product_data = await __fetch_product_data(artikul, url)
    if len(product_data) > 0:
        product_data = product_data[0]
        total_quantity = sum(
            item.get('qty', 0) for item in product_data.get('sizes', []) if item.get('qty') is not None
        )
        product = Product(
            artikul=artikul,
            name=product_data.get('name'),
            price=product_data.get('salePriceU') / 100,
            rating=product_data.get('rating'),
            total_quantity=total_quantity
        )
        return product

