from datetime import date, datetime, timedelta
from database import SessionLocal, engine, Base
from models.supplier import Supplier, PriceHistory, PurchaseRecord, WeatherData
import numpy as np

Base.metadata.create_all(bind=engine)
db = SessionLocal()


suppliers = [
    {
        "name": "上海鑫源食品有限公司",
        "contact_person": "张伟",
        "phone": "13800138001",
        "email": "zhangwei@xinyuan.com",
        "address": "上海市浦东新区张江高科技园区",
        "product_type": "食品原料",
        "credit_rating": 4.8
    },
    {
        "name": "江苏恒通化工集团",
        "contact_person": "李明",
        "phone": "13900139002",
        "email": "liming@hengtong.com",
        "address": "江苏省南京市江宁经济技术开发区",
        "product_type": "化工原料",
        "credit_rating": 4.5
    },
    {
        "name": "浙江绿源农业科技",
        "contact_person": "王芳",
        "phone": "13700137003",
        "email": "wangfang@lvyuan.com",
        "address": "浙江省杭州市余杭区良渚镇",
        "product_type": "农产品",
        "credit_rating": 4.9
    }
]

for s in suppliers:
    supplier = Supplier(**s, created_at=datetime.now(), updated_at=datetime.now())
    db.add(supplier)

db.commit()


def create_price_history(supplier_id, product_name, base_price, variance, days=60):
    today = date.today()
    for i in range(days):
        record_date = today - timedelta(days=i)
        price = base_price + np.random.normal(0, variance)
        price = max(price, base_price * 0.7)
        price = min(price, base_price * 1.3)

        price_history = PriceHistory(
            supplier_id=supplier_id,
            product_name=product_name,
            price=round(price, 2),
            date=record_date
        )
        db.add(price_history)


create_price_history(1, "大豆油", 85.5, 3.0)
create_price_history(1, "白砂糖", 68.0, 2.5)
create_price_history(2, "甲醇", 2800.0, 100.0)
create_price_history(2, "乙二醇", 3200.0, 120.0)
create_price_history(3, "有机大米", 12.5, 0.8)
create_price_history(3, "有机蔬菜", 8.5, 1.2)


def create_purchase_records(supplier_id, product_name, base_price):
    today = date.today()
    for i in range(12):
        record_date = today - timedelta(days=i * 30)
        quantity = np.random.uniform(100, 500)
        unit_price = base_price + np.random.normal(0, base_price * 0.05)

        purchase = PurchaseRecord(
            supplier_id=supplier_id,
            product_name=product_name,
            quantity=round(quantity, 2),
            unit_price=round(unit_price, 2),
            total_amount=round(quantity * unit_price, 2),
            purchase_date=record_date
        )
        db.add(purchase)


create_purchase_records(1, "大豆油", 85.5)
create_purchase_records(2, "甲醇", 2800.0)
create_purchase_records(3, "有机大米", 12.5)


def create_weather_data(days=60):
    today = date.today()
    for i in range(days):
        record_date = today - timedelta(days=i)
        temperature = 15 + np.random.normal(0, 5)
        humidity = 60 + np.random.normal(0, 15)
        precipitation = np.random.exponential(2)
        wind_speed = 5 + np.random.normal(0, 3)

        if precipitation > 10:
            condition = "Rain"
        elif temperature > 25:
            condition = "Sunny"
        else:
            condition = "Cloudy"

        weather = WeatherData(
            date=record_date,
            temperature=round(temperature, 1),
            humidity=round(humidity, 1),
            precipitation=round(precipitation, 2),
            wind_speed=round(wind_speed, 1),
            weather_condition=condition,
            city="Shanghai"
        )
        db.add(weather)


create_weather_data()

db.commit()
db.close()

print("Seed data created successfully!")