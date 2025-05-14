from typing import Optional
from fastapi import status
from fastapi.responses import JSONResponse
from database.database import engine

from service.food_service import FoodService, IFoodService
from models.foodPlans import Plans, Food, FoodPlanLink

class FoodController:
    def __init__(self, service: Optional[IFoodService] = None):
        self.engine = engine

    def get_plans(self):
        with self.engine.connect() as connection:
            result = connection.execute(text("SELECT id_plan, title, planDescription, objetive FROM plans"))
            plans = []
            for row in result:
                plan = {
                    "id_plan": row.id_plan,
                    "title": row.title,
                    "planDescription": row.planDescription,
                    "objetive": row.objetive,
                }
                plans.append(plan)
            return {"plans":plans}

    def get_plan(self, aId):
        with self.engine.connect() as connection:
            result = connection.execute(text(f"SELECT id_plan, title, planDescription, objetive FROM plans WHERE id_plan={aId}"))
            plan = result.fetchone()
            if plan:
                plan_json = {
                    "id_plan": plan.id_plan,
                    "title": plan.title,
                    "planDescription": plan.planDescription,
                    "objetive": plan.objetive,
                }
                return plan_json
            else:
                return {"message": "Plan not found"}

    def get_user_plan(self, aUser):
        # ACA hay que revisar como se implemento users
        pass

    def add_plan(self, aTitle, aDescription, aObjetive):
        with self.engine.connect() as connection:
            result = connection.execute(text(f"INSERT INTO plans(title, planDescription, objetive) VALUES ('{aTitle}','{aDescription}', '{aObjetive}')"))
            connection.commit()    
