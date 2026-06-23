from sqlalchemy import Column, Integer, String, Float, Text, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    contact_person = Column(String(50))
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    product_type = Column(String(100))
    credit_rating = Column(Float, default=0.0)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    price_history = relationship("PriceHistory", back_populates="supplier")
    purchase_records = relationship("PurchaseRecord", back_populates="supplier")


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    product_name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(10), default="CNY")
    date = Column(Date, nullable=False)

    supplier = relationship("Supplier", back_populates="price_history")


class PurchaseRecord(Base):
    __tablename__ = "purchase_records"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    product_name = Column(String(100), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_amount = Column(Float)
    purchase_date = Column(Date, nullable=False)
    status = Column(String(20), default="completed")

    supplier = relationship("Supplier", back_populates="purchase_records")


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True)
    temperature = Column(Float)
    humidity = Column(Float)
    precipitation = Column(Float)
    wind_speed = Column(Float)
    weather_condition = Column(String(50))
    city = Column(String(50))