from typing import Optional
from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import Engine, Executable, text
from database.database import engine

from service.food_service import FoodService, IFoodService
from models.foodPlans import Plans, Food, FoodPlanLink

class FoodController:
    def __init__(self, service: Optional[IFoodService] = None):
        self.engine = engine

    def get_plans(self):
        with self.engine.connect() as connection:
            result = connection.execute(text("SELECT id_plan, title, plan_description, objetive FROM plans"))
            plans = []
            for fila in result:
                plan = {
                    "id_plan": row.id_plan,
                    "title": row.title,
                    "plan_description": row.plan_description,
                    "objetive": row.objetive,
                }
                plans.append(plan)
            return {"plans":plans}

    def get_plan(self, aId) -> Plans:
        with self.engine.connect() as connection:
            result = connection.execute(text(f"SELECT id_plan, title, plan_description, objetive FROM plans WHERE id_plan={aId}"))
            plan = result.fetchone()
            if plan:
                plan_json = {
                    "id_plan": plan.id_plan,
                    "title": plan.title,
                    "plan_description": plan.plan_description,
                    "objetive": plan.objetive,
                }
                return Plans(**plan_json)
            else:
                return Plans()

    def get_user_plan(self, aUser):
        # ACA hay que revisar como se implemento users
        pass

    def add_plan(self, aTitle, aDescription, aObjetive):
        with self.engine.connect() as connection:
            result = connection.execute(text(f"INSERT INTO plans(title, plan_description, objetive) VALUES ('{aTitle}','{aDescription}', '{aObjetive}')"))
            connection.commit()    
