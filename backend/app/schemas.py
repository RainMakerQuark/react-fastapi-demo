from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    done: bool = False

class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int
    class Config:
        from_attributes = True

class ItemUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None
