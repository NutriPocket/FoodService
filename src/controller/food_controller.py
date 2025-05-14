from typing import Optional
from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import Engine, Executable, text
from database.database import engine

from service.food_service import FoodService, IFoodService
from models.foodPlans import Plans, Food, FoodPlanLink, Users

class FoodController:
    def __init__(self, service: Optional[IFoodService] = None):
        self.engine = engine

    def get_plans(self):
        with self.engine.connect() as connection:
            result = connection.execute(text("SELECT id_plan, title, plan_description, objetive FROM plans"))
            plans = []
            for fila in result:
                plan = {
                    "id_plan": fila.id_plan,
                    "title": fila.title,
                    "plan_description": fila.plan_description,
                    "objetive": fila.objetive,
                }
                plans.append(plan)
            return {"plans":plans}

    def get_plan(self, aId) -> Plans:
        print("plan")
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

    def add_plan(self, aTitle, aDescription, aObjetive):
        with self.engine.connect() as connection:
            result = connection.execute(text(f"INSERT INTO plans(title, plan_description, objetive) VALUES ('{aTitle}','{aDescription}', '{aObjetive}')"))
            connection.commit()

    def get_user_plan(self, userId) -> Plans:
        with self.engine.connect() as connection:
            result = connection.execute(text(f"SELECT id_user, name, id_plan FROM users WHERE id_user={userId}"))
            user = result.fetchone()
            idPlan = user.id_plan
            print(idPlan)
            result = connection.execute(text(f"SELECT id_plan, title, plan_description, objetive FROM plans WHERE id_plan={idPlan}"))
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
    
    def post_user(self, username) -> None:
        with self.engine.connect() as connection:
            result = connection.execute(text(f"INSERT INTO users(name) VALUES ('{username}')"))
            connection.commit()
    
    def post_user_plan(self, userId, planId) -> None:
        with self.engine.connect() as connection:
            result = connection.execute(text(f"UPDATE users SET id_plan={planId} WHERE id_user={userId}"))
            connection.commit()
        
