from abc import ABCMeta, abstractmethod
from typing import Any, Optional, Sequence, List
from sqlalchemy import Engine, Row, text
from database.database import engine
from models.errors.errors import EntityAlreadyExistsError, NotFoundError
from models.foodPlans import Food, FoodDTO, FoodLinkDTO, FoodIngredientDTO, FoodTimeDTO, Ingredient, IngredientDTO, Plan, PlanAssignment, PlanAssignmentDTO, PlanDTO, WeeklyPlan
from models.params import GetAllFoodsParams
from sqlalchemy.exc import IntegrityError
from models.foodPlans import MeasureType


class IFoodRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_plans(self) -> list[Plan]:
        pass

    @abstractmethod
    def get_plan_by_id(self, plan_id: int) -> Optional[Plan]:
        pass

    @abstractmethod
    def get_weekly_plan_by_id(self, plan_id: int) -> Sequence[Row[Any]]:
        pass

    @abstractmethod
    def save_plan(self, plan: PlanDTO) -> Plan:
        pass

    @abstractmethod
    def get_plan_by_user_id(self, user_id: str) -> Optional[Plan]:
        pass

    @abstractmethod
    def save_user_plan(self, user_id: str, assignment: PlanAssignmentDTO) -> PlanAssignment:
        pass

    @abstractmethod
    def update_user_plan(self, user_id: str, assignment: PlanAssignmentDTO) -> PlanAssignment:
        pass

    @abstractmethod
    def get_foods_from_plan(self, plan_id: int) -> list[Food]:
        pass

    @abstractmethod
    def remove_food_from_plan(self, plan_id: int, data: FoodTimeDTO) -> None:
        pass

    @abstractmethod
    def update_food_weekly_plan(self, plan_id: int, data: FoodLinkDTO) -> None:
        pass

    @abstractmethod
    def save_food_weekly_plan(self, plan_id: int, day: int, moment: int, food_id: int) -> None:
        pass

    @abstractmethod
    def get_day_by_name(self, day: str) -> Optional[int]:
        pass

    @abstractmethod
    def get_moment_by_name(self, moment: str) -> Optional[int]:
        pass

    @abstractmethod
    def get_matching_food_ids(self, foods: list[str]) -> list[int]:
        pass

    @abstractmethod
    def get_days(self) -> list[dict]:
        pass

    @abstractmethod
    def get_moments(self) -> list[dict]:
        pass

    @abstractmethod
    def get_food_by_id_from_plan(self, plan_id: int, food_id: int) -> Optional[Food]:
        pass

    @abstractmethod
    def get_food_by_id(self, food_id: int) -> Optional[Food]:
        pass

    @abstractmethod
    def get_all_foods(self, params: GetAllFoodsParams) -> list[Food]:
        pass

    @abstractmethod
    def save_food(self, food: FoodDTO) -> Food:
        pass

    @abstractmethod
    def save_ingredient(self, ingredient: IngredientDTO) -> Ingredient:
        pass

    @abstractmethod
    def save_food_ingredients(self, food_id: int, ingredients: List[FoodIngredientDTO]) -> None:
        pass

    @abstractmethod 
    def link_food_to_plan(self, food_id: int, plan_id: int, day_id: Optional[int], meal_moment_id: Optional[int]) -> None:
        pass


class FoodRepository(IFoodRepository):
    def __init__(self, engine_: Optional[Engine] = None):
        self.engine = engine_ or engine

    def get_plans(self) -> list[Plan]:
        query = text("""
            SELECT id_plan, title, plan_description, objetive, created_at
            FROM plans
        """)

        with self.engine.begin() as connection:
            result = connection.execute(query).fetchall()

            return [Plan(**row._mapping) for row in result]

    def get_plan_by_id(self, plan_id: int) -> Optional[Plan]:
        query = text("""
            SELECT id_plan, title, plan_description, objetive, created_at
            FROM plans
            WHERE id_plan = :plan_id
            LIMIT 1
        """)

        params = {"plan_id": plan_id}

        with self.engine.begin() as connection:
            result = connection.execute(query, params).fetchone()

            if result:
                return Plan(**result._mapping)

    def get_weekly_plan_by_id(self, plan_id: int) -> Sequence[Row[Any]]:
        query = text("""
            SELECT
                wd.id AS day_id,
                wd.name AS day_name,
                mm.id AS meal_moment_id,
                mm.name AS meal_moment_name,
                f.id AS food_id,
                f.name AS food_name,
                f.description AS food_description,
                f.price AS food_price,
                f.created_at AS food_created_at
            FROM
                week_days wd
            CROSS JOIN meal_moments mm
            LEFT JOIN foodplanlink fpl
                ON fpl.plan_id = :plan_id
                AND fpl.day_id = wd.id
                AND fpl.meal_moment_id = mm.id
            LEFT JOIN foods f ON f.id = fpl.food_id
            ORDER BY wd.id, mm.id
        """)

        params = {"plan_id": plan_id}

        with self.engine.begin() as connection:
            return connection.execute(query, params).fetchall()

    def save_plan(self, plan: PlanDTO) -> Plan:
        query = text("""
            INSERT INTO plans (title, plan_description, objetive)
            VALUES (:title, :plan_description, :objetive)
            RETURNING id_plan, title, plan_description, objetive, created_at
        """)

        params = {
            "title": plan.title,
            "plan_description": plan.plan_description,
            "objetive": plan.objetive
        }

        with self.engine.begin() as connection:
            result = connection.execute(query, params).fetchone()

            if not result:
                raise Exception("Error saving plan")

            return Plan(**result._mapping)

    def get_plan_by_user_id(self, user_id: str) -> Optional[Plan]:
        query = text("""
            SELECT p.id_plan, p.title, p.plan_description, p.objetive, p.created_at
            FROM users u
            JOIN plans p ON u.id_plan = p.id_plan
            WHERE u.id_user = :user_id
        """)

        params = {"user_id": user_id}

        with self.engine.begin() as connection:
            result = connection.execute(query, params).fetchone()

            if result:
                return Plan(**result._mapping)

    def save_user_plan(self, user_id: str, assignment: PlanAssignmentDTO) -> PlanAssignment:
        query = text("""
            INSERT INTO users (id_user, id_plan, updated_at)
            VALUES (:user_id, :plan_id, NOW())
            RETURNING id_plan AS plan_id, updated_at
        """)

        params = {"user_id": user_id, "plan_id": assignment.plan_id}

        with self.engine.begin() as connection:
            result = connection.execute(query, params).fetchone()

            if not result:
                raise Exception("Error saving user plan")

            return PlanAssignment(**result._mapping)

    def update_user_plan(self, user_id: str, assignment: PlanAssignmentDTO) -> PlanAssignment:
        query = text("""
            UPDATE users
            SET
                id_plan = :plan_id,
                updated_at = NOW()
            WHERE id_user = :user_id
            RETURNING id_plan AS plan_id, updated_at
        """)

        params = {"user_id": user_id, "plan_id": assignment.plan_id}

        with self.engine.begin() as connection:
            result = connection.execute(query, params).fetchone()

            if not result:
                raise Exception("Error updating user plan")

            return PlanAssignment(**result._mapping)

    def get_foods_from_plan(self, plan_id: int) -> list[Food]:
        query = text("""
            SELECT DISTINCT
                f.id, 
                f.name, 
                f.description, 
                f.price, 
                f.created_at
            FROM foodplanlink_general pf
            JOIN foods f ON pf.food_id = f.id
            WHERE pf.plan_id = :plan_id
        """)

        params = {"plan_id": plan_id}

        with self.engine.begin() as connection:
            result = connection.execute(query, params).fetchall()
            return [Food(**row._mapping) for row in result]

    def remove_food_from_plan(self, plan_id: int, data: FoodTimeDTO) -> None:
        query = text("""
            DELETE FROM foodplanlink
            WHERE plan_id = :plan_id
                AND day_id = :day_id
                AND meal_moment_id = :moment_id
        """)

        params = {
            "plan_id": plan_id,
            "day_id": data.day,
            "moment_id": data.moment
        }

        with self.engine.begin() as connection:
            connection.execute(query, params)

    def update_food_weekly_plan(self, plan_id: int, data: FoodLinkDTO) -> None:
        query = text("""
            UPDATE foodplanlink
            SET food_id = :food_id
            WHERE plan_id = :plan_id AND day_id = :day_id AND meal_moment_id = :moment_id
        """)

        params = {
            "food_id": data.food_id,
            "plan_id": plan_id,
            "day_id": data.day,
            "moment_id": data.moment
        }

        with self.engine.begin() as conn:
            result = conn.execute(query, params)
            if result.rowcount == 0:
                raise NotFoundError(detail="Meal entry not found in plan")

    def save_food_weekly_plan(self, plan_id: int, day: int, moment: int, food_id: int) -> None:
        query = text("""
            INSERT INTO foodplanlink (plan_id, day_id, meal_moment_id, food_id, updated_at)
            VALUES (:plan_id, :day_id, :moment_id, :food_id, NOW())
        """)

        params = {
            "plan_id": plan_id,
            "day_id": day,
            "moment_id": moment,
            "food_id": food_id
        }

        try:
            with self.engine.begin() as connection:
                connection.execute(query, params)

        except IntegrityError:
            raise EntityAlreadyExistsError(
                title="A food in that moment already exists",
                detail=f"A food for the plan {plan_id} on day {day} and moment {moment} already exists"
            )

    def get_day_by_name(self, day: str) -> Optional[int]:
        query = text("""
            SELECT id
            FROM week_days
            WHERE name = :name
            LIMIT 1
        """)

        params = {"name": day}

        with self.engine.begin() as connection:
            result = connection.execute(query, params).scalar_one()

            return result if result else None

    def get_moment_by_name(self, moment: str) -> Optional[int]:
        query = text("""
            SELECT id
            FROM meal_moments
            WHERE name = :name
            LIMIT 1
        """)

        params = {"name": moment}

        with self.engine.begin() as connection:
            result = connection.execute(query, params).scalar_one()

            return result if result else None

    def get_matching_food_ids(self, foods: list[str]) -> list[int]:
        query = text(f"""
            SELECT id
            FROM foods
            WHERE id IN ({','.join([f":food{i}" for i in range(len(foods))])})
        """)

        params = {f"food{i}": food_id for i, food_id in enumerate(foods)}

        with self.engine.begin() as connection:
            result = connection.execute(query, params).fetchall()

            return [row.id for row in result]

    def get_days(self) -> list[dict]:
        query = text("""
            SELECT id, name
            FROM week_days
        """)

        with self.engine.begin() as connection:
            result = connection.execute(query).fetchall()

            return [dict(row._mapping) for row in result]

    def get_moments(self) -> list[dict]:
        query = text("""
            SELECT id, name
            FROM meal_moments
        """)

        with self.engine.begin() as connection:
            result = connection.execute(query).fetchall()

            return [dict(row._mapping) for row in result]

    def get_food_by_id_from_plan(self, plan_id: int, food_id: int) -> Optional[Food]:
        query = text("""
            SELECT f.id, f.name, f.description, f.price, f.created_at
            FROM foodplanlink fpl
            JOIN foods f ON fpl.food_id = f.id
            WHERE fpl.plan_id = :plan_id AND f.id = :food_id
        """)

        params = {"plan_id": plan_id, "food_id": food_id}

        with self.engine.begin() as connection:
            result = connection.execute(query, params).fetchone()

            if result:
                return Food(**result._mapping)

    def get_food_by_id(self, food_id: int) -> Optional[Food]:
        query = text("""
            SELECT 
                id, 
                name, 
                description, 
                price, 
                created_at,
                image_url
            FROM foods
            WHERE id = :food_id
        """)

        params = {"food_id": food_id}

        with self.engine.begin() as connection:
            result = connection.execute(query, params).fetchone()

            if result:
                return Food(**result._mapping)

    def get_all_foods(self, params: GetAllFoodsParams) -> list[Food]:
        query = text("""
            SELECT id, name, description, price, created_at
            FROM foods
        """)

        _params: dict[str, Any] = dict()

        if params.search_name:
            query = text("""
                SELECT id, name, description, price, created_at
                FROM foods
                WHERE name ILIKE :search_name
            """)

            _params["search_name"] = f"%{params.search_name}%"

        with self.engine.begin() as connection:
            result = connection.execute(query, _params).fetchall()

            return [Food(**row._mapping) for row in result]

    def save_food(self, food: FoodDTO) -> Food:
        query = text("""
            INSERT INTO foods (name, description, price, image_url)
            VALUES (:name, :description, :price, :image_url)
            RETURNING id, name, description, price, image_url, created_at
        """)

        params = {
            "name": food.name,
            "description": food.description,
            "price": food.price,
            "image_url": food.image_url
        }

        with self.engine.begin() as connection:
            result = connection.execute(query, params).fetchone()

            if not result:
                raise Exception("Error saving food")

            return Food(**result._mapping)

    def save_food_ingredients(self, food_id: int, ingredients: List[FoodIngredientDTO]) -> None:
        query = text("""
            INSERT INTO food_ingredients (food_id, ingredient_id, quantity)
            VALUES (:food_id, :ingredient_id, :quantity)
        """)

        with self.engine.begin() as connection:
            for item in ingredients:
                connection.execute(query, {
                    "food_id": food_id,
                    "ingredient_id": item.ingredient_id,
                    "quantity": item.quantity
                })

    def link_food_to_plan(self, food_id: int, plan_id: int, day_id: Optional[int], meal_moment_id: Optional[int]) -> None:
        if day_id is None and meal_moment_id is None:
            query = text("""
                INSERT INTO foodplanlink_general (food_id, plan_id, updated_at)
                VALUES (:food_id, :plan_id, NOW())
                ON CONFLICT (food_id, plan_id) DO NOTHING
            """)
            params = {
                "food_id": food_id,
                "plan_id": plan_id
            }
        else:
            query = text("""
                INSERT INTO foodplanlink (food_id, plan_id, day_id, meal_moment_id, updated_at)
                VALUES (:food_id, :plan_id, :day_id, :meal_moment_id, NOW())
                ON CONFLICT DO NOTHING
            """)
            params = {
                "food_id": food_id,
                "plan_id": plan_id,
                "day_id": day_id,
                "meal_moment_id": meal_moment_id
            }

        with self.engine.begin() as connection:
            connection.execute(query, params)

    def save_ingredient(self, ingredient: IngredientDTO) -> Ingredient:
        query = text("""
            INSERT INTO ingredients (
                name,
                measure_type,
                calories,
                protein,
                carbs,
                fiber,
                saturated_fats,
                monounsaturated_fats,
                polyunsaturated_fats,
                trans_fats,
                cholesterol
            )
            VALUES (
                :name,
                :measure_type,
                :calories,
                :protein,
                :carbs,
                :fiber,
                :saturated_fats,
                :monounsaturated_fats,
                :polyunsaturated_fats,
                :trans_fats,
                :cholesterol
            )
            RETURNING
                id,
                name,
                measure_type,
                calories,
                protein,
                carbs,
                fiber,
                saturated_fats,
                monounsaturated_fats,
                polyunsaturated_fats,
                trans_fats,
                cholesterol,
                created_at
        """)

        params = {
            "name": ingredient.name,
            "measure_type": ingredient.measure_type.value,  # assuming MeasureType is Enum
            "calories": ingredient.calories,
            "protein": ingredient.protein,
            "carbs": ingredient.carbs,
            "fiber": ingredient.fiber,
            "saturated_fats": ingredient.saturated_fats,
            "monounsaturated_fats": ingredient.monounsaturated_fats,
            "polyunsaturated_fats": ingredient.polyunsaturated_fats,
            "trans_fats": ingredient.trans_fats,
            "cholesterol": ingredient.cholesterol,
        }

        with self.engine.begin() as connection:
            result = connection.execute(query, params).fetchone()

            if not result:
                raise Exception("Error saving ingredient")

            return Ingredient(**result._mapping)
            
    def get_nutritional_values(self, food_id: int) -> Optional[dict]:
        query = text("""
            SELECT 
                SUM(i.calories * fi.quantity / 100.0) AS calories,
                SUM(i.protein * fi.quantity / 100.0) AS protein,
                SUM(i.carbs * fi.quantity / 100.0) AS carbs,
                SUM(i.fiber * fi.quantity / 100.0) AS fiber,
                SUM(i.saturated_fats * fi.quantity / 100.0) AS saturated_fats,
                SUM(i.monounsaturated_fats * fi.quantity / 100.0) AS monounsaturated_fats,
                SUM(i.polyunsaturated_fats * fi.quantity / 100.0) AS polyunsaturated_fats,
                SUM(i.trans_fats * fi.quantity / 100.0) AS trans_fats,
                SUM(i.cholesterol * fi.quantity / 100.0) AS cholesterol
            FROM food_ingredients fi
            JOIN ingredients i ON fi.ingredient_id = i.id
            WHERE fi.food_id = :food_id
            GROUP BY fi.food_id
        """)
        with self.engine.connect() as conn:
            result = conn.execute(query, {"food_id": food_id}).fetchone()
            if result is None:
                return None
            return dict(result._mapping)

    def get_ingredients_by_food_id(self, food_id: int) -> list[FoodIngredientDTO]:
        query = text("""
            SELECT 
                i.name,
                i.measure_type,
                i.calories,
                i.protein,
                i.carbs,
                i.fiber,
                i.saturated_fats,
                i.monounsaturated_fats,
                i.polyunsaturated_fats,
                i.trans_fats,
                i.cholesterol,
                fi.quantity
            FROM food_ingredients fi
            JOIN ingredients i ON fi.ingredient_id = i.id
            WHERE fi.food_id = :food_id
        """)

        with engine.connect() as conn:
            result = conn.execute(query, {"food_id": food_id})
            rows = result.fetchall()

        return [
            FoodIngredientDTO(
                ingredient=IngredientDTO(
                    name=row[0],
                    measure_type=MeasureType(row[1]),
                    calories=row[2],
                    protein=row[3],
                    carbs=row[4],
                    fiber=row[5],
                    saturated_fats=row[6],
                    monounsaturated_fats=row[7],
                    polyunsaturated_fats=row[8],
                    trans_fats=row[9],
                    cholesterol=row[10]
                ),
                quantity=row[11]
            )
            for row in rows
        ]

    def get_all_ingredients(self) -> list[Ingredient]:
        query = text("""
            SELECT id, name
            FROM ingredients
        """)
        with engine.connect() as conn:
            result = conn.execute(query)
            ingredients = []
            for row in result.fetchall():
                ingredients.append(Ingredient(
                    id=row.id,
                    name=row.name
                ))
        return ingredients