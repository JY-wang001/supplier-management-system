from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from models.supplier import Supplier, PriceHistory, PurchaseRecord
from schemas.supplier import (
    Supplier as SupplierSchema,
    SupplierCreate,
    SupplierUpdate,
    PriceHistory as PriceHistorySchema,
    PriceHistoryCreate,
    PurchaseRecord as PurchaseRecordSchema,
    PurchaseRecordCreate,
)
from database import get_db

router = APIRouter(prefix="/suppliers", tags=["suppliers"])


@router.get("/", response_model=List[SupplierSchema])
def get_suppliers(db: Session = Depends(get_db)):
    return db.query(Supplier).all()


@router.get("/{supplier_id}", response_model=SupplierSchema)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


@router.post("/", response_model=SupplierSchema)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    db_supplier = Supplier(
        **supplier.dict(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier


@router.put("/{supplier_id}", response_model=SupplierSchema)
def update_supplier(supplier_id: int, supplier: SupplierUpdate, db: Session = Depends(get_db)):
    db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    for key, value in supplier.dict(exclude_unset=True).items():
        setattr(db_supplier, key, value)

    db_supplier.updated_at = datetime.now()
    db.commit()
    db.refresh(db_supplier)
    return db_supplier


@router.delete("/{supplier_id}")
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    db.delete(supplier)
    db.commit()
    return {"message": "Supplier deleted successfully"}


@router.get("/{supplier_id}/price-history", response_model=List[PriceHistorySchema])
def get_price_history(supplier_id: int, db: Session = Depends(get_db)):
    return db.query(PriceHistory).filter(
        PriceHistory.supplier_id == supplier_id
    ).order_by(PriceHistory.date).all()


@router.post("/price-history", response_model=PriceHistorySchema)
def create_price_history(price_history: PriceHistoryCreate, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(
        Supplier.id == price_history.supplier_id
    ).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    db_price = PriceHistory(**price_history.dict())
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price


@router.get("/{supplier_id}/purchase-records", response_model=List[PurchaseRecordSchema])
def get_purchase_records(supplier_id: int, db: Session = Depends(get_db)):
    return db.query(PurchaseRecord).filter(
        PurchaseRecord.supplier_id == supplier_id
    ).order_by(PurchaseRecord.purchase_date).all()


@router.post("/purchase-records", response_model=PurchaseRecordSchema)
def create_purchase_record(purchase_record: PurchaseRecordCreate, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(
        Supplier.id == purchase_record.supplier_id
    ).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    if purchase_record.total_amount is None:
        purchase_record.total_amount = purchase_record.quantity * purchase_record.unit_price

    db_purchase = PurchaseRecord(**purchase_record.dict())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase