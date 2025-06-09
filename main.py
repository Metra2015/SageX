# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.database import engine, Base
from api import auth, trade, training, knowledge, notifications, coin_ranking
from core.database import SessionLocal
from api import debug



app.include_router(debug.router, prefix="/debug", tags=["Debug"])


# Create all tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="SageX Backend",
    description="AI Crypto Trading Assistant Backend",
    version="1.0.0",
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(trade.router, prefix="/trade", tags=["Trading"])
app.include_router(training.router, prefix="/training", tags=["Training"])
app.include_router(knowledge.router, prefix="/knowledge", tags=["Knowledge Center"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
app.include_router(coin_ranking.router, prefix="/ranking", tags=["Coin Ranking"])


def test_db_connection():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")  # Basic ping
        db.close()
        print("✅ Database connected successfully.")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to SageX API"}




