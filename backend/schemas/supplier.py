from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List, Dict


class SupplierBase(BaseModel):
    name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    product_type: Optional[str] = None
    credit_rating: Optional[float] = 0.0


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(SupplierBase):
    pass


class Supplier(SupplierBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PriceHistoryBase(BaseModel):
    product_name: str
    price: float
    currency: Optional[str] = "CNY"
    date: date


class PriceHistoryCreate(PriceHistoryBase):
    supplier_id: int


class PriceHistory(PriceHistoryBase):
    id: int
    supplier_id: int

    model_config = {"from_attributes": True}


class PurchaseRecordBase(BaseModel):
    product_name: str
    quantity: float
    unit_price: float
    total_amount: Optional[float] = None
    purchase_date: date
    status: Optional[str] = "completed"


class PurchaseRecordCreate(PurchaseRecordBase):
    supplier_id: int


class PurchaseRecord(PurchaseRecordBase):
    id: int
    supplier_id: int

    model_config = {"from_attributes": True}


class WeatherDataBase(BaseModel):
    date: date
    temperature: float
    humidity: float
    precipitation: float
    wind_speed: float
    weather_condition: str
    city: str


class WeatherData(WeatherDataBase):
    id: int

    model_config = {"from_attributes": True}


class PricePredictionRequest(BaseModel):
    supplier_id: int
    product_name: str
    days_ahead: int = 7


class PricePredictionResponse(BaseModel):
    supplier_id: int
    product_name: str
    predictions: List[Dict]
    metrics: Dict

    model_config = {"protected_namespaces": ()}