from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from pynamodb import attributes, models
from pynamodb.exceptions import DoesNotExist


class Item(models.Model):
    class Meta:
        region = "ap-northeast-1"
        table_name = "item"

    id = attributes.UnicodeAttribute(hash_key=True)
    name = attributes.UnicodeAttribute()
    description = attributes.UnicodeAttribute(null=True, default=None)
    price = attributes.NumberAttribute()
    tax = attributes.NumberAttribute(null=True, default=None)
    version = attributes.VersionAttribute()


class PostRequest(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class PutRequest(PostRequest):
    version: int


class ItemResponse(BaseModel):
    id: str
    name: str
    description: str | None
    price: float
    tax: float | None
    version: int


app = FastAPI()


@app.post("/items/", response_model=ItemResponse, response_model_exclude_none=True)
def create_item(request: PostRequest) -> ItemResponse:
    item = Item(
        id=str(uuid4()),
        name=request.name,
        description=request.description,
        price=request.price,
        tax=request.tax,
    )
    item.save()
    return ItemResponse.parse_raw(item.to_json())


def get_valid_item(item_id: str) -> Item:
    try:
        return Item.get(item_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Item not found")


@app.put(
    "/items/{item_id}", response_model=ItemResponse, response_model_exclude_none=True
)
def put_item(request: PutRequest, item: Item = Depends(get_valid_item)) -> ItemResponse:
    actions = [
        Item.name.set(request.name),
        Item.description.set(request.description),
        Item.price.set(request.price),
        Item.tax.set(request.tax),
    ]
    item.update(actions=actions)
    return ItemResponse.parse_raw(item.to_json())
