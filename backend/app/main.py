from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .db import SessionLocal, init_db
from . import models, schemas

app = FastAPI(title="Interview Starter API", version="1.0.0", root_path="")

# If serving the React build from FastAPI (e.g., on Replit), uncomment StaticFiles below
# from fastapi.staticfiles import StaticFiles
# app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="static")

# CORS (relaxed for demo; in dev Vite proxy makes this unnecessary)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

API_PREFIX = "/api"

@app.get(f"{API_PREFIX}/items", response_model=list[schemas.ItemRead])
def list_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

@app.post(f"{API_PREFIX}/items", response_model=schemas.ItemRead, status_code=201)
def create_item(payload: schemas.ItemCreate, db: Session = Depends(get_db)):
    item = models.Item(title=payload.title, done=payload.done)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.get(f"{API_PREFIX}/items/{{item_id}}", response_model=schemas.ItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.patch(f"{API_PREFIX}/items/{{item_id}}", response_model=schemas.ItemRead)
def update_item(item_id: int, payload: schemas.ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(models.Item).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if payload.title is not None:
        item.title = payload.title
    if payload.done is not None:
        item.done = payload.done
    db.commit()
    db.refresh(item)
    return item

@app.delete(f"{API_PREFIX}/items/{{item_id}}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return JSONResponse(status_code=204, content=None)
