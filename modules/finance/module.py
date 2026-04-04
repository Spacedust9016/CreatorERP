from core.module_base import ModuleBase
from core.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from fastapi import APIRouter
from typing import List, Optional
from pydantic import BaseModel


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    description = Column(String(200))
    amount = Column(Float)
    category = Column(String(50))
    source = Column(String(50))
    is_income = Column(Boolean, default=True)
    date = Column(DateTime, default=datetime.utcnow)


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    description = Column(String(200))
    amount = Column(Float)
    category = Column(String(50))
    date = Column(DateTime, default=datetime.utcnow)


class TransactionModel(BaseModel):
    id: int
    description: str
    amount: float
    category: str
    source: str
    is_income: bool
    date: str


class RevenueSource(BaseModel):
    source: str
    amount: float
    percentage: float


router = APIRouter(prefix="/api/finance", tags=["finance"])


@router.get("/overview")
async def get_overview():
    return {
        "total_revenue_month": 4820,
        "total_expenses_month": 320,
        "net_income": 4500,
        "revenue_change": 12,
        "expense_change": 8,
    }


@router.get("/revenue-sources", response_model=List[RevenueSource])
async def get_revenue_sources():
    return [
        {"source": "Udemy", "amount": 3940, "percentage": 81.7},
        {"source": "AdSense", "amount": 620, "percentage": 12.9},
        {"source": "Sponsors", "amount": 260, "percentage": 5.4},
    ]


@router.get("/transactions", response_model=List[TransactionModel])
async def get_transactions():
    return [
        {
            "id": 1,
            "description": "New video published",
            "amount": 0,
            "category": "Content",
            "source": "YouTube",
            "is_income": False,
            "date": "2026-04-05",
        },
        {
            "id": 2,
            "description": "Newsletter #48 sent",
            "amount": 0,
            "category": "Marketing",
            "source": "Email",
            "is_income": False,
            "date": "2026-04-04",
        },
        {
            "id": 3,
            "description": "12 new enrollments",
            "amount": 180,
            "category": "Courses",
            "source": "Udemy",
            "is_income": True,
            "date": "2026-04-04",
        },
        {
            "id": 4,
            "description": "AdSense payout",
            "amount": 620,
            "category": "Ads",
            "source": "YouTube",
            "is_income": True,
            "date": "2026-04-01",
        },
        {
            "id": 5,
            "description": "Sponsorship deal",
            "amount": 260,
            "category": "Sponsors",
            "source": "Brand X",
            "is_income": True,
            "date": "2026-03-28",
        },
    ]


@router.get("/revenue-chart")
async def get_revenue_chart():
    return {"labels": ["Udemy", "AdSense", "Sponsors"], "data": [3940, 620, 260]}


@router.get("/audience-chart")
async def get_audience_chart():
    return {"labels": ["YouTube", "Instagram", "X"], "data": [71200, 34200, 18400]}


class FinanceModule(ModuleBase):
    name = "finance"
    version = "1.0.0"
    description = "Financial tracking and analytics"
    models = [Transaction, Expense]

    def register_routes(self, app):
        app.include_router(router)

    def get_simulated_data(self):
        return {
            "monthly_revenue": 4820,
            "sources": [
                {"source": "Udemy", "amount": 3940},
                {"source": "AdSense", "amount": 620},
                {"source": "Sponsors", "amount": 260},
            ],
        }
