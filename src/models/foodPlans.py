from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Optional, Union


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
    calories_per_100g: Optional[int] = Field(
        None,
        title="Calories per 100g",
        description="Amount of calories per 100 grams in kilocalories",
        ge=0
    )
    protein_per_100g: Optional[int] = Field(
        None,
        title="Protein per 100g",
        description="Amount of protein per 100 grams in grams",
        ge=0,
        le=100
    )
    carbs_per_100g: Optional[int] = Field(
        None,
        title="Carbohydrates per 100g",
        description="Amount of carbohydrates per 100 grams in grams",
        ge=0,
        le=100
    )
    fiber_per_100g: Optional[int] = Field(
        None,
        title="Fiber per 100g",
        description="Amount of fiber per 100 grams in grams",
        ge=0,
        le=100
    )
    saturated_fats_per_100g: Optional[int] = Field(
        None,
        title="Saturated Fats per 100g",
        description="Amount of saturated fats per 100 grams in grams",
        ge=0,
        le=100
    )
    monounsaturated_fats_per_100g: Optional[int] = Field(
        None,
        title="Monounsaturated Fats per 100g",
        description="Amount of monounsaturated fats per 100 grams in grams",
        ge=0,
        le=100
    )
    polyunsaturated_fats_per_100g: Optional[int] = Field(
        None,
        title="Polyunsaturated Fats per 100g",
        description="Amount of polyunsaturated fats per 100 grams in grams",
        ge=0,
        le=100
    )
    trans_fats_per_100g: Optional[int] = Field(
        None,
        title="Trans Fats per 100g",
        description="Amount of trans fats per 100 grams in grams",
        ge=0,
        le=100
    )
    cholesterol_per_100g: Optional[int] = Field(
        None,
        title="Cholesterol per 100g",
        description="Amount of cholesterol per 100 grams in milligrams",
        ge=0,
        le=100
    )
    ingredients: Optional[List[str]] = Field(
        None,
        title="Ingredients",
        description="List of ingredients with recommended quantities and home measurements"
    )
    image_url: Optional[str] = Field(
        None,
        title="url",
        description="link to the image"
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


class ExtraFoodDTO(BaseModel):
    name: str = Field(
        ...,
        title="Extra food name",
        description="Name of the extra food item",
        max_length=64,
        min_length=1
    )
    description: str = Field(
        ...,
        title="extra food description",
        description="Description of the extra food item",
        max_length=512,
    )
    ingredients: List[str] = Field(
        ...,
        title="Ingredients",
        description="List of ingredients with recommended quantities and home measurements"
    )
    image_url: Optional[str] = Field(
        None,
        title="url",
        description="link to the image"
    )
    day: str = Field(
        ...,
        title="day",
        description="Lunes, Martes, ..",
        max_length=64,
        min_length=1
    )
    moment: str = Field(
        ...,
        title="moment",
        description="Desayuno, almuerzo, cena",
        max_length=64,
        min_length=1
    )
    date: datetime = Field(
        ...,
        title="a date ",
        description="Date",
    )

class ExtraFood(ExtraFoodDTO):
    id_extra_food: int = Field(
        ...,
        title="Extra Food ID",
        description="Unique identifier for the extra food item",
    )
    created_at: datetime = Field(
        ...,
        title="Creation date",
        description="Date when the food item was created",
    )