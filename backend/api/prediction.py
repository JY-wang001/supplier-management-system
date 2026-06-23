from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.supplier import PricePredictionRequest, PricePredictionResponse
from ml.predictor import predict_prices
from database import get_db

router = APIRouter(prefix="/prediction", tags=["prediction"])


@router.post("/price", response_model=PricePredictionResponse)
def predict_price(request: PricePredictionRequest, db: Session = Depends(get_db)):
    result = predict_prices(db, request.supplier_id, request.product_name, request.days_ahead)

    if 'error' in result['model_metrics']:
        raise HTTPException(status_code=400, detail=result['model_metrics']['error'])

    return PricePredictionResponse(
        supplier_id=request.supplier_id,
        product_name=request.product_name,
        predictions=result['predictions'],
        metrics=result['model_metrics']
    )