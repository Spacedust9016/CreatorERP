from abc import ABC, abstractmethod
from typing import List, Type
from sqlalchemy.orm import Session
from core.database import Base


class ModuleBase(ABC):
    name: str
    version: str = "1.0.0"
    description: str = ""
    models: List[Type[Base]] = []

    @abstractmethod
    def register_routes(self, app):
        pass

    @abstractmethod
    def get_simulated_data(self):
        pass

    def init_models(self):
        for model in self.models:
            if hasattr(model, "__table__"):
                model.__table__.create(engine, checkfirst=True)
