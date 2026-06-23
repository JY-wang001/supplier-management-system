from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.supplier import router as supplier_router
from api.prediction import router as prediction_router
from api.weather import router as weather_router
from api.auth import router as auth_router
from database import engine, Base
from models.auth import User
import os

port = int(os.getenv("PORT", "8000"))

app = FastAPI(title="Supplier Management and Price Prediction System", version="1.0.0")

@app.on_event("startup")
def startup_event():
    try:
        from database import engine, Base
        Base.metadata.create_all(bind=engine)
        print("Database tables created or verified successfully.")
    except Exception as e:
        print(f"Error creating database tables: {e}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(supplier_router)
app.include_router(prediction_router)
app.include_router(weather_router)


@app.get("/")
def root():
    return {"message": "Supplier Management and Price Prediction System API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")