from typing import Optional

from models.params import GetAllFoodsParams
from models.response import CustomResponse
from service.food_service import FoodService, IFoodService
from models.foodPlans import Food, FoodDTO, FoodLinkDTO, FoodTimeDTO, PlanAssignmentDTO, PlanDTO, WeeklyPlan, Plan, PlanAssignment


class FoodController:
    def __init__(self, service: Optional[IFoodService] = None):
        self.service = service or FoodService()

    def get_plans(self) -> CustomResponse[list[Plan]]:
        _plans = self.service.get_plans()

        return CustomResponse(data=_plans)

    def get_plan(self, plan_id: int) -> CustomResponse[WeeklyPlan]:
        _weekly_plan = self.service.get_weekly_plan_by_id(plan_id)

        return CustomResponse(data=_weekly_plan)

    def add_plan(self, plan: PlanDTO) -> CustomResponse[Plan]:
        _plan = self.service.save_food_plan(plan)

        return CustomResponse(data=_plan)

    def get_user_plan(self, userId: str) -> CustomResponse[Plan]:
        _plan = self.service.get_food_plan_by_user_id(userId)

        return CustomResponse(data=_plan)

    def put_user_plan(self, userId: str, assignment: PlanAssignmentDTO) -> CustomResponse[PlanAssignment]:
        _plan_assignment = self.service.put_user_plan(userId, assignment)

        return CustomResponse(data=_plan_assignment)

    def get_foods_from_plan(self, plan_id: int) -> CustomResponse[list[Food]]:
        _foods = self.service.get_foods_from_plan(plan_id)

        return CustomResponse(data=_foods)

    def get_foods_from_user_plan(self, user_id: str) -> CustomResponse[list[Food]]:
        _foods = self.service.get_foods_from_user_plan(user_id)

        return CustomResponse(data=_foods)

    def add_food_to_user_plan(self, userId: str, food: FoodLinkDTO) -> CustomResponse[WeeklyPlan]:
        _foods = self.service.save_food_to_user_plan(userId, food)

        return CustomResponse(data=_foods)

    def remove_food_from_user_plan(self, userId: str, data: FoodTimeDTO) -> CustomResponse[WeeklyPlan]:
        _foods = self.service.remove_food_from_user_plan(userId, data)

        return CustomResponse(data=_foods)

    def create_plan_from_preferences(self, user_id: str, preferences: list) -> CustomResponse[Plan]:
        _plan = self.service.create_food_plan_by_preferences(
            user_id, preferences)

        return CustomResponse(data=_plan)

    def update_food_in_plan(self, plan_id: int, data: FoodLinkDTO) -> CustomResponse[WeeklyPlan]:
        _plan = self.service.update_food_in_plan(plan_id, data)

        return CustomResponse(data=_plan)

    def get_food_by_id(self, food_id: int) -> CustomResponse[Food]:
        _food = self.service.get_food_by_id(food_id)

        return CustomResponse(data=_food)

    def get_all_foods(self, params: GetAllFoodsParams) -> CustomResponse[list[Food]]:
        _foods = self.service.get_all_foods(params)

        return CustomResponse(data=_foods)
    
    def add_food_in_db(self, food: FoodDTO) -> CustomResponse[Food]:
        _foods = self.service.save_food_in_db(food)
        return CustomResponse(data=_foods)