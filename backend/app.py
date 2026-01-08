from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from models import Article
from data import ARTICLES

app = FastAPI()

# Allow local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/articles", response_model=List[Article])
def list_articles(featured: Optional[str] = Query(None)):
    articles = ARTICLES

    if featured:
        if featured.lower() == "true":
            articles = [a for a in articles if a.is_featured]
        elif featured.lower() == "false":
            articles = [a for a in articles if not a.is_featured]

    return articles

@app.get("/api/articles/{article_id}", response_model=Article)
def get_article(article_id: int):
    # Lookup by ID, not index
    for article in ARTICLES:
        if article.id == article_id:
            return article
    raise HTTPException(status_code=404, detail="Article not found")

@app.post("/api/articles", response_model=Article, status_code=201)
def create_article(article: Article):
    # Prevent duplicate IDs
    if any(existing.id == article.id for existing in ARTICLES):
        raise HTTPException(
            status_code=409,
            detail="Article with this ID already exists"
        )

    ARTICLES.append(article)
    return article
