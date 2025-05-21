from typing import Optional
from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import Engine, Executable, text
from database.database import engine

from service.food_service import FoodService, IFoodService
from models.foodPlans import Plan, Plans, Food, PlanAssigment, Users

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

    from sqlalchemy import text

    def get_plan(self, plan_id: int):
        with self.engine.connect() as connection:
            # 1. Get plan data
            plan = connection.execute(
                text("SELECT id_plan, title, plan_description, objetive FROM plans WHERE id_plan = :plan_id"),
                {"plan_id": plan_id}
            ).fetchone()
            if not plan:
                raise Exception(f"Plan with id {plan_id} not found")

            # 2. Query all days × meal moments + food (left join)
            result = connection.execute(
                text("""
                SELECT
                    wd.id AS day_id,
                    wd.name AS day_name,
                    mm.id AS meal_moment_id,
                    mm.name AS meal_moment_name,
                    f.id AS food_id,
                    f.name AS food_name,
                    f.description AS food_description,
                    f.price AS food_price
                FROM
                    week_days wd
                CROSS JOIN meal_moments mm
                LEFT JOIN weekly_meal_plan_food wmpf
                ON wmpf.plan_id = :plan_id
                AND wmpf.day_id = wd.id
                AND wmpf.meal_moment_id = mm.id
                LEFT JOIN foods f ON f.id = wmpf.food_id
                ORDER BY wd.id, mm.id
                """),
                {"plan_id": plan_id}
            )

            # 3. Build structured response
            schedule = {}
            for row in result:
                day = row.day_name
                moment = row.meal_moment_name
                food = None
                if row.food_id:
                    food = {
                        "id": row.food_id,
                        "name": row.food_name,
                        "description": row.food_description,
                        "price": float(row.food_price)
                    }
                else:
                    food = "No meal selected"

                if day not in schedule:
                    schedule[day] = {}

                schedule[day][moment] = food
            print(schedule)
            # 4. Return full response
            return {
                "id_plan": plan.id_plan,
                "title": plan.title,
                "plan_description": plan.plan_description,
                "objetive": plan.objetive,
                "weekly_plan": schedule
            }


    def add_plan(self, aTitle, aDescription, aObjetive):
        print("add plan")
        with self.engine.connect() as connection:
            result = connection.execute(
            text("""
                INSERT INTO plans(title, plan_description, objetive)
                VALUES (:title, :description, :objetive)
                RETURNING id_plan
            """),
            {"title": aTitle, "description": aDescription, "objetive": aObjetive}
            )
            connection.commit()
            plan_id = result.scalar()
            return plan_id

    def get_user_plan(self, userId) -> Plans:
        with self.engine.connect() as connection:
            result = connection.execute(text(f"SELECT id_user, id_plan FROM users WHERE id_user='{userId}'"))
            
            user = result.fetchone()
            idPlan = user.id_plan
            
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
    
    def put_user_plan(self, userId, planId) -> None:
        with self.engine.connect() as connection:
            print("put user plan")
            print(userId)
            print(planId)

            # Verificar si exl usuario existe
            result = connection.execute(
                text("SELECT id_user FROM users WHERE id_user = :userId"),
                {"userId": userId}
            )
            user = result.fetchone()
            if user:
                # Si existe, actualizar el plan
                print("entra a actualizar el plan")
                connection.execute(
                    text("UPDATE users SET id_plan = :planId WHERE id_user = :userId"),
                    {"planId": planId, "userId": userId}
                )
            else:
                # Si no existe, crear el usuario con ese plan
                print("entra a crear un nuevo usuario")
                connection.execute(
                    text("INSERT INTO users (id_user, id_plan) VALUES (:userId, :planId)"),
                    {"userId": userId, "planId": planId}
                )
            connection.commit()

    def get_foods_from_plan(self, plan_id: int):
        with self.engine.connect() as connection:
            result = connection.execute(text(
                f"""
                SELECT f.id, f.name, f.description, f.price, f.created_at
                FROM foodplanlink fpl
                JOIN foods f ON fpl.food_id = f.id
                WHERE fpl.plan_id = {plan_id}
                """
            ))

            foods = []
            for row in result:
                foods.append({
                    "id": row.id,
                    "name": row.name,
                    "description": row.description,
                    "price": float(row.price),
                    "created_at": str(row.created_at),
                })

            return {"foods": foods}

    def get_foods_from_user_plan(self, user_id: str):
        with self.engine.connect() as connection:
            user_result = connection.execute(text(
                f"SELECT id_plan FROM users WHERE id_user = '{user_id}'"
            ))
            user = user_result.fetchone()
            if not user or user.id_plan is None:
                return {"foods": []}

            plan_id = user.id_plan

            foods_result = connection.execute(text(
                f"""
                SELECT f.id, f.name, f.description, f.price, f.created_at
                FROM foodplanlink fpl
                JOIN foods f ON fpl.food_id = f.id
                WHERE fpl.plan_id = {plan_id}
                """
            ))

            foods = []
            for row in foods_result:
                foods.append({
                    "id": row.id,
                    "name": row.name,
                    "description": row.description,
                    "price": float(row.price),
                    "created_at": str(row.created_at),
                })
            print(foods)

            return {"foods": foods}


    def add_food_to_user_plan(self, userId: int, foodId: int) -> None:
        with self.engine.connect() as connection:
            user_result = connection.execute(text(f"SELECT id_plan FROM users WHERE id_user = {userId}"))
            user = user_result.fetchone()
            if not user or user.id_plan is None:
                raise Exception("User or user's plan not found")

            planId = user.id_plan

            existing = connection.execute(text(
                f"SELECT 1 FROM foodplanlink WHERE food_id = {foodId} AND plan_id = {planId}"
            )).fetchone()

            if not existing:
                connection.execute(text(
                    f"INSERT INTO foodplanlink(food_id, plan_id) VALUES ({foodId}, {planId})"
                ))
                connection.commit()

    def remove_food_from_user_plan(self, userId: int, foodId: int) -> None:
        with self.engine.connect() as connection:
            user_result = connection.execute(text(f"SELECT id_plan FROM users WHERE id_user = {userId}"))
            user = user_result.fetchone()
            if not user or user.id_plan is None:
                raise Exception("User or user's plan not found")

            planId = user.id_plan

            connection.execute(text(
                f"DELETE FROM foodplanlink WHERE food_id = {foodId} AND plan_id = {planId}"
            ))
            connection.commit()

    def create_plan_from_preferences(self, user_id: int, preferences: list) -> Plans:
        with self.engine.connect() as connection:
            if not preferences:
                raise Exception("No food preferences provided.")

            food_id_placeholders = ','.join([str(int(fid)) for fid in preferences])
            result = connection.execute(
                text(f"SELECT id FROM foods WHERE id IN ({food_id_placeholders})")
            )
            matching_foods = [row.id for row in result]

            if not matching_foods:
                raise Exception("None of the provided food IDs were found in the database.")

            # 2. Create a new plan
            title = f"Plan for User {user_id}"
            description = f"Generated from selected food IDs"
            objective = "Automatically generated based on preferences"

            new_plan_id = self.add_plan(title, description, objective)


            # result = connection.execute(
            #     text("""
            #         INSERT INTO plans(title, plan_description, objetive)
            #         VALUES (:title, :desc, :obj)
            #         RETURNING id_plan
            #     """),
            #     {"title": title, "desc": description, "obj": objective}
            # )
            # new_plan_id = result.scalar()

            print(f"New plan ID: {new_plan_id}")

            # 4. Link all selected foods to the plan
            for food_id in matching_foods:
                connection.execute(
                    text("INSERT INTO foodplanlink(food_id, plan_id) VALUES (:food_id, :plan_id)"),
                    {"food_id": food_id, "plan_id": new_plan_id}
                )

            # 5. Fill the weekly_meal_plan_food table (7 days × 4 moments)
            week_days = connection.execute(text("SELECT id FROM week_days ORDER BY id")).fetchall()
            meal_moments = connection.execute(text("SELECT id FROM meal_moments ORDER BY id")).fetchall()

            food_index = 0
            total_foods = len(matching_foods)

            for day in week_days:
                for moment in meal_moments:
                    food_id = matching_foods[food_index % total_foods]
                    connection.execute(
                        text("""
                            INSERT INTO weekly_meal_plan_food (plan_id, day_id, meal_moment_id, food_id)
                            VALUES (:plan_id, :day_id, :moment_id, :food_id)
                        """),
                        {
                            "plan_id": new_plan_id,
                            "day_id": day.id,
                            "moment_id": moment.id,
                            "food_id": food_id
                        }
                    )
                    food_index += 1

            self.put_user_plan(user_id, new_plan_id)
            print(f"User {user_id} assigned to new plan {new_plan_id}")
            connection.commit()

            return {
                "id_plan": new_plan_id,
                "title": title,
                "plan_description": description,
                "objetive": objective
            }

