from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Optional, Union
from enum import Enum

class PlanDTO(BaseModel):
    title: str = Field(
        ...,
        title="Plan title",
        description="Title of the food plan",
        max_length=64,
        min_length=1
    )
    plan_description: Optional[str] = Field(
        None,
        title="Plan description",
        description="Description of the food plan",
        max_length=512,
    )
    objetive: str = Field(
        ...,
        title="Plan objective",
        description="Objective of the food plan",
        max_length=64,
        min_length=1
    )


class Plan(PlanDTO):
    id_plan: int = Field(
        ...,
        title="Plan ID",
        description="Unique identifier for the plan",
    )
    created_at: datetime = Field(
        ...,
        title="Creation date",
        description="Date when the plan was created",
    )


class WeeklyPlan(Plan):
    weekly_plan: Dict[str, Dict[str, Optional[Union[dict, str]]]] = Field(
        ...,
        title="Weekly plan",
        description="Weekly food plan with meals for each day and moment",
        examples=[
            {
                "Lunes": {
                    "Desayuno": {
                        "food_id": 1,
                        "name": "Oatmeal",
                        "description": "Healthy oatmeal with fruits",
                        "calories": 200
                    },
                    "Almuerzo": {
                        "food_id": 2,
                        "name": "Grilled Chicken",
                        "description": "Grilled chicken with vegetables",
                        "calories": 300
                    }
                },
                "Martes": {
                    "Desayuno": {
                        "food_id": 3,
                        "name": "Smoothie",
                        "description": "Fruit smoothie with yogurt",
                        "calories": 150
                    },
                    "Almuerzo": {
                        "food_id": 4,
                        "name": "Salad",
                        "description": "Fresh salad with dressing",
                        "calories": 250
                    }
                }
            }
        ]
    )


class PlanAssignmentDTO(BaseModel):
    plan_id: int = Field(
        ...,
        title="Plan ID",
        description="Unique identifier for the plan",
    )


class PlanAssignment(PlanAssignmentDTO):
    updated_at: datetime = Field(
        ...,
        title="Update date",
        description="Date when the plan was updated",
    )

class MeasureType(str, Enum):
    GRAM = "gram"
    UNIT = "unit"

class IngredientDTO(BaseModel):
    name: str = Field(..., max_length=64)
    measure_type: MeasureType = Field(..., description="Whether the ingredient is measured in grams or units")
    
    calories: float = Field(..., ge=0, description="Calories per 100g or per unit")
    protein: float = Field(..., ge=0, description="Protein in grams per 100g or per unit")
    carbs: float = Field(..., ge=0, description="Carbohydrates in grams per 100g or per unit")
    fiber: float = Field(..., ge=0, description="Fiber in grams per 100g or per unit")
    saturated_fats: float = Field(..., ge=0, description="Saturated fats in grams per 100g or per unit")
    monounsaturated_fats: float = Field(..., ge=0, description="Monounsaturated fats in grams per 100g or per unit")
    polyunsaturated_fats: float = Field(..., ge=0, description="Polyunsaturated fats in grams per 100g or per unit")
    trans_fats: float = Field(..., ge=0, description="Trans fats in grams per 100g or per unit")
    cholesterol: float = Field(..., ge=0, description="Cholesterol in mg per 100g or per unit")

class Ingredient(BaseModel):
    id: int = Field(
        ...,
        title="Ingredient ID",
        description="Unique identifier for the ingredient item",
    )
    name: str = Field(
         ...,
        title="Ingredient name",
        description="Unique name for the ingredient",       
    )

class FoodIngredientDTO(BaseModel):
    ingredient: IngredientDTO
    quantity: float = Field(..., gt=0, description="Cantidad usada del ingrediente en gramos o unidades, segun sea el caso")

class IngredientQuantityDTO(BaseModel):
    quantity: float  # en gramos o unidades
    measure: MeasureType


class FoodIngredientLinkDTO(BaseModel):
    ingredient_id: int = Field(..., description="ID of the ingredient")
    quantity: float = Field(..., ge=0, description="Quantity of the ingredient in grams or units")

class FoodDTO(BaseModel):
    name: str = Field(
        ...,
        title="Food name",
        description="Name of the food item",
        max_length=64,
        min_length=1
    )
    description: Optional[str] = Field(
        None,
        title="Food description",
        description="Description of the food item",
        max_length=512,
    )
    price: float = Field(
        ...,
        title="Food price",
        description="Price of the food item",
        ge=0,
    )
    image_url: Optional[str] = Field(
        None,
        title="url",
        description="link to the image"
    )
    ingredients: Optional[List[FoodIngredientLinkDTO]] = Field(
        None,
        title="Ingredients",
        description="List of ingredient's ids used in this food item with their quantities"
    )

class Food(FoodDTO):
    id: int = Field(
        ...,
        title="Food ID",
        description="Unique identifier for the food item",
    )
    created_at: datetime = Field(
        ...,
        title="Creation date",
        description="Date when the food item was created",
    )


class FoodPreferenceRequest(BaseModel):
    user_id: str = Field(
        ...,
        title="User ID",
        description="Unique identifier for the user as UUID",
        max_length=36,
        min_length=36,
        pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    )
    preferences: List[int] = Field(
        ...,
        title="Prefered foods",
        description="List of IDs of prefered foods",
        examples=[
            [420, 69],
            [777],
        ],
    )


class FoodTimeDTO(BaseModel):
    day: str = Field(
        ...,
        title="Day of the week",
        description="Day of the week for the food plan",
        examples=["Lunes", "Martes", "Miércoles",
                  "Jueves", "Viernes", "Sábado", "Domingo"],
        max_length=10,
        min_length=1
    )
    moment: str = Field(
        ...,
        title="Moment of the day",
        description="Moment of the day for the food plan",
        examples=["Desayuno", "Almuerzo", "Merienda", "Cena"],
        max_length=10,
        min_length=1
    )


class FoodLinkDTO(FoodTimeDTO):
    food_id: int = Field(
        ...,
        title="Food ID",
        description="Unique identifier for the food item",
    )

