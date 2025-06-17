from fastapi import APIRouter, Query, status, Path

from controller.food_controller import FoodController
from models.errors.errors import ValidationError
from models.foodPlans import Food, FoodLinkDTO, FoodIngredientDTO, FoodTimeDTO, Ingredient, IngredientDTO, IngredientQuantityDTO, Plan, PlanAssignment, PlanAssignmentDTO, WeeklyPlan, ExtraFood, ExtraFoodDTO
from models.params import GetAllFoodsParams, PostPlanBody, PostFoodBody, PostExtraFoodBody, GetExtraFoodsParams
from models.response import CustomResponse, ErrorDTO
from sqlalchemy import Engine, Row, text
from database.database import engine
from datetime import datetime

router = APIRouter()


@router.get(
    "/plans",
    summary="Retrieves all the differents plans",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[list[Plan]],
            "description": "List of food plans"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def get_food_plans() -> CustomResponse[list[Plan]]:
    return FoodController().get_plans()


@router.get(
    "/plans/{id}",
    summary="Retrieves a specific detailed weekly plan",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[WeeklyPlan],
            "description": "List of food plans"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorDTO,
            "description": "Plan not found"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def get_plan_by_id(id: int) -> CustomResponse[WeeklyPlan]:
    return FoodController().get_plan(id)


@router.post(
    "/plans",
    summary="Create a new food plan",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "model": CustomResponse[Plan],
            "description": "List of food plans"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def post_plan(
    body: PostPlanBody,
    from_preferences: bool = Query(
        default=False,
        description="If true, the plan will be created from user preferences",
    )
) -> CustomResponse[Plan]:
    if from_preferences and body.preferences:
        return FoodController().create_plan_from_preferences(
            body.preferences.user_id, body.preferences.preferences, body.plan
        )

    if not body.plan:
        raise ValidationError(
            detail="If you want to create a plan from preferences, you need to provide the user_id and preferences. If you want to create a plan from scratch, you need to provide the plan title, description and objective.",
            title="Missing body or wrong body"
        )

    return FoodController().add_plan(body.plan)


@router.get(
    "/users/{user_id}/plan",
    summary="Retrieves the user's plan",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[Plan],
            "description": "List of food plans"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorDTO,
            "description": "Plan not found"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def get_user_plan(user_id: str) -> CustomResponse[Plan]:
    return FoodController().get_user_plan(user_id)


@router.put(
    "/users/{user_id}/plan",
    summary="Replace the user's plan",
    description="If the user already has a plan, it will be replaced. If not, a new plan will be created.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[PlanAssignment],
            "description": "Update user's plans"
        },
        status.HTTP_201_CREATED: {
            "model": CustomResponse[PlanAssignment],
            "description": "Create user's plans"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def put_user_plan(assigment: PlanAssignmentDTO, user_id: str) -> CustomResponse[PlanAssignment]:
    return FoodController().put_user_plan(user_id, assigment)


# def post_user_plan(userId:int, planId:int) -> None:
#    return FoodController().post_user_plan(userId, planId)
#
# 2 formas de obtener las comidas de un plan: por ID de plan o ID de usuario
@router.get(
    "/plans/{plan_id}/foods",
    summary="Get all foods in a plan",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[list[Food]],
            "description": "List of food plans"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def get_foods_from_plan(plan_id: int) -> CustomResponse[list[Food]]:
    return FoodController().get_foods_from_plan(plan_id)


@router.get(
    "/users/{user_id}/plan/foods",
    summary="Get all foods from a user's plan",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[list[Food]],
            "description": "List of food plans"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorDTO,
            "description": "Plan not found"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def get_foods_from_user_plan(user_id: str) -> CustomResponse[list[Food]]:
    return FoodController().get_foods_from_user_plan(user_id)


@router.post(
    "/users/{user_id}/plan/foods",
    summary="Adds a new food for the user's plan",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[WeeklyPlan],
            "description": "List of food plans"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorDTO,
            "description": "Plan not found"
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorDTO,
            "description": "A food already exists at that moment in that day in the plan"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def add_food_to_user_plan(req: FoodLinkDTO, user_id: str) -> CustomResponse[WeeklyPlan]:
    return FoodController().add_food_to_user_plan(user_id, req)


@router.put(
    "/plans/{plan_id}/foods",
    summary="Update a food item for a specific day and moment in plan",
    description="Update a food item for a specific day and moment in plan, retrieves the updated weekly plan",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[WeeklyPlan],
            "description": "Update a food from the user's plan"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorDTO,
            "description": "Item not found"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def update_meal_in_plan(plan_id: int, data: FoodLinkDTO) -> CustomResponse[WeeklyPlan]:
    return FoodController().update_food_in_plan(plan_id, data)


@router.delete(
    "/users/{user_id}/plan/foods",
    summary="remove a food from user's plan",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[WeeklyPlan],
            "description": "Remove a food from the user's plan"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorDTO,
            "description": "Plan not found"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def remove_food_from_user_plan(data: FoodTimeDTO, user_id: str) -> CustomResponse[WeeklyPlan]:
    return FoodController().remove_food_from_user_plan(user_id, data)


@router.get(
    "/foods/{food_id}",
    summary="Get food by id",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[Food],
            "description": "Food found"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorDTO,
            "description": "Food not found"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def get_food_by_id(food_id: int) -> CustomResponse[Food]:
    return FoodController().get_food_by_id(food_id)


@router.get(
    "/foods",
    summary="Get all foods",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[list[Food]],
            "description": "List of foods"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def get_all_foods(search_name: str = Query(None, description="Search food by name. Case insensitive. Anywhere match")) -> CustomResponse[list[Food]]:
    params = GetAllFoodsParams(search_name=search_name)
    return FoodController().get_all_foods(params)

@router.post(
    "/food",
    summary="Create a new food",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "model": CustomResponse[Food],
            "description": "List of foods"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def post_food(body: PostFoodBody) -> CustomResponse[Food]:
    if not body.food:
        raise ValidationError(
            detail="If you want to create a food from scratch, you need to provide a long list of params...",
            title="Missing body or wrong body"
        )
    return FoodController().add_food_in_db(body)

@router.post(
    "/food/ingredients",
    summary="Create a new ingredient",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "model": CustomResponse[Ingredient],
            "description": "New ingredient created"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def post_ingredient(body: IngredientDTO) -> CustomResponse[Ingredient]:
    return FoodController().add_ingredient(body)

@router.get(
    "/foods/{food_id}/ingredients",
    summary="Get ingredients for a specific food item",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[list[str]],
            "description": "List of ingredients for the food"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorDTO,
            "description": "Ingredients not found for the given food ID"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid food ID format"
        },
    }
)
def get_ingredients_by_food_id(food_id: int) -> CustomResponse[list[FoodIngredientDTO]]:
    ingredients = FoodController().get_ingredients_by_food_id(food_id)
    if not ingredients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No ingredients found for food with ID {food_id}"
        )
    return CustomResponse(data=ingredients)

@router.get("/foods/{food_id}/nutrition")
def get_food_nutrition(food_id: int):
    return FoodController().get_nutritional_values(food_id)

@router.get(
    "/foods/ingredients/all",
    summary="Get all ingredients",
    status_code=status.HTTP_200_OK,
    response_model=CustomResponse[list[Ingredient]],
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[list[Ingredient]],
            "description": "List of all ingredients"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
    }
)
def get_all_ingredients() -> CustomResponse[list[Ingredient]]:
    ingredients = FoodController().get_all_ingredients()
    return CustomResponse(data=ingredients)

@router.post(
    "/users/{user_id}/extrafood",
    summary="Add a extra food in a user at specific day",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "model": CustomResponse[Food],
            "description": "List of foods"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid json body format"
        },
    }
)
def post_extra_food(body: PostExtraFoodBody, user_id: str) -> CustomResponse[ExtraFood]:
    if not (body.extraFood and user_id):
        raise ValidationError(
            detail="If you want to create a extra food from scratch, you need to provide a user id and a long list of params...",
            title="Missing body or wrong body")
    return FoodController().add_extra_food(body.extraFood, user_id) 

@router.get(
    "/extrafoods/{user_id}/",
    summary="Get all extra foods from a user ID",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[list[Food]],
            "description": "List of foods"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
    }
)
def get_extra_foods(user_id: str, start_date: datetime, end_date: datetime, moment: str = Query(None, description="Search food by moment. Case insensitive. Anywhere match")) -> CustomResponse[list[ExtraFood]]:
    params = GetExtraFoodsParams(user_id=user_id, start_date=start_date, end_date=end_date, moment=moment)
    return FoodController().get_extra_foods(params)

@router.post("/foods/{food_id}/ingredients/add/{ingredient_id}")
def add_ingredient_to_food(food_id: int, ingredient_id: int, data: IngredientQuantityDTO):
    insert_query = text("""
        INSERT INTO food_ingredients (food_id, ingredient_id, quantity)
        VALUES (:food_id, :ingredient_id, :quantity)
        ON CONFLICT (food_id, ingredient_id) DO UPDATE
        SET quantity = EXCLUDED.quantity
    """)
    with engine.connect() as conn:
        try:
            conn.execute(insert_query, {
                "food_id": food_id,
                "ingredient_id": ingredient_id,
                "quantity": data.quantity
            })
            conn.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": "Ingrediente agregado a la comida exitosamente."}

@router.delete("/foods/{food_id}/ingredients/remove/{ingredient_id}")
def remove_ingredient_from_food(food_id: int, ingredient_id: int):
    delete_query = text("""
        DELETE FROM food_ingredients
        WHERE food_id = :food_id AND ingredient_id = :ingredient_id
    """)
    with engine.connect() as conn:
        try:
            result = conn.execute(delete_query, {
                "food_id": food_id,
                "ingredient_id": ingredient_id
            })
            conn.commit()
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Ingrediente no encontrado en la comida.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Ingrediente eliminado de la comida exitosamente."}

@router.get("/foods/ingredients/{ingredient_search}")
def search_ingredients_by_name(ingredient_search: str = Path(..., min_length=1, description="Partial name of the ingredient")):
    search_query = text("""
        SELECT id, name, measure_type
        FROM ingredients
        WHERE name ILIKE :search_term
    """)
    
    with engine.connect() as conn:
        try:
            result = conn.execute(search_query, {
                "search_term": f"%{ingredient_search}%"
            })
            ingredients = [
                {
                    "id": row.id,
                    "name": row.name,
                    "measure_type": row.measure_type
                }
                for row in result.fetchall()
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return ingredients

@router.get(
    "/extraFood/{extraFoodId}/ingredients",
    summary="Get ingredients for a specific extra food item",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": CustomResponse[list[FoodIngredientDTO]],
            "description": "List of ingredients for the extra food"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorDTO,
            "description": "User unauthorized"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorDTO,
            "description": "No authorization provided"
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorDTO,
            "description": "Ingredients not found for the given extra food ID"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ErrorDTO,
            "description": "Invalid food ID format"
        },
    }
)
def get_ingredients_by_extra_food_id(extraFood_id: int) -> CustomResponse[list[FoodIngredientDTO]]:
    ingredients = FoodController().get_ingredients_by_extra_food_id(extraFood_id)
    if not ingredients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No ingredients found for food with ID {extraFood_id}"
        )
    return CustomResponse(data=ingredients)

@router.post("/users/{id_user}/water_consumption_goal/{water_goal}")
def add_water_goal_to_user(id_user: str, water_goal: int):
    query = text("""
            SELECT id_user
            FROM user_water_goals
            WHERE id_user = :id_user
            LIMIT 1
        """)
    insert_water_goal = text("""
                INSERT INTO user_water_goals (id_user, goal_ml, end_date)
                VALUES (:id_user, :goal_ml, NULL)
            """)
    query_update_goal = text("""
                UPDATE user_water_goals 
                SET end_date = CURRENT_DATE
                WHERE id_user = :id_user AND end_date IS NULL
            """)
    query_search_user = text("""SELECT id_user FROM users
            WHERE id_user = :id_user
            LIMIT 1""")
    params = {"id_user": id_user}

    with engine.connect() as conn:
        hasWaterGoal = conn.execute(query, params).fetchone()
        userExists = conn.execute(query_search_user, params).fetchone()
        _params = {"id_user": id_user, "goal_ml": water_goal}

        if not userExists:
            return {"message": "El usuario no existe"}

        if hasWaterGoal:
            try:
                conn.execute(query_update_goal, _params)
                conn.commit()
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    
        try:
            conn.execute(insert_water_goal, _params)
            conn.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        return  {"message": "Meta de consumo de agua agregada correctamente."}
    
@router.post("/users/{id_user}/water_consumption/{amount_ml}/")
def add_water_consumption_to_user(id_user: str, amount_ml: int):
    query_user_exists = text("""SELECT id_user FROM users WHERE id_user = :id_user LIMIT 1""")
    query_has_water_goal = text("""SELECT id_user FROM user_water_goals WHERE id_user = :id_user LIMIT 1""")
    params = {"id_user": id_user}
    with engine.connect() as conn:
        userExists = conn.execute(query_user_exists, params).fetchone()
        hasWaterGoal = conn.execute(query_has_water_goal, params).fetchone()
        _params = {"id_user": id_user}

        if not userExists:
            return {"message": "El usuario no existe"}
        if not hasWaterGoal:
            return {"message": "El usuario no tiene establecida una meta en su consumo de agua"}
        query_load_water = text("""INSERT INTO water_consumption(id_user, consumption_date, amount_ml) 
        VALUES(:id_user, NOW(), :amount_ml)""")
        params = {"id_user": id_user, "amount_ml": amount_ml}
        result = conn.execute(query_load_water, params)
        conn.commit()
        if not result:
                raise Exception("Error saving water consumption")
        return {"message": "El usuario cargo su consumo de agua satisfactoriamente"}
    
@router.get("/users/{id_user}/water_consumption/")
def get_water_consumption_user(id_user: str):
    query_user_exists = text("""SELECT id_user FROM users WHERE id_user = :id_user LIMIT 1""")
    query_has_water_goal = text("""SELECT id_user FROM user_water_goals WHERE id_user = :id_user LIMIT 1""")
    params = {"id_user": id_user}
    with engine.connect() as conn:
        userExists = conn.execute(query_user_exists, params).fetchone()
        hasWaterGoal = conn.execute(query_has_water_goal, params).fetchone()
        if not userExists:
            return {"message": "El usuario no existe"}
        if not hasWaterGoal:
            return {"message": "El usuario no tiene establecida una meta en su consumo de agua"}
        query_get_current_goal_date = text("""SELECT goal_ml, start_date FROM user_water_goals WHERE id_user=:id_user AND end_date IS NULL LIMIT 1""")
        result = conn.execute(query_get_current_goal_date, params).fetchone()
        query_get_list_consumption = text("""SELECT amount_ml, consumption_date FROM water_consumption WHERE id_user=:id_user AND consumption_date >= :lastDate""")
        amount_and_dates = conn.execute(query_get_list_consumption, {"id_user": id_user, "lastDate": result[1]}).fetchall()
        consumptions = [{"amount_ml": row[0], "consumption_date": row[1]} for row in amount_and_dates]
        return {"goal": {"goal_ml": result[0],},"consumptions": consumptions}