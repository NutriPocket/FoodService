from abc import ABCMeta, abstractmethod
from typing import Optional

from models.errors.errors import NotFoundError
from models.foodPlans import Food, FoodDTO, FoodLinkDTO, FoodTimeDTO, Plan, PlanAssignment, PlanAssignmentDTO, PlanDTO, WeeklyPlan, ExtraFoodDTO, ExtraFood
from models.params import GetAllFoodsParams
from repository.food_repository import FoodRepository, IFoodRepository


class IFoodService(metaclass=ABCMeta):
    @abstractmethod
    def get_plans(self) -> list[Plan]:
        pass

    @abstractmethod
    def get_plan(self, plan_id: int) -> Plan:
        pass

    @abstractmethod
    def get_weekly_plan_by_id(self, plan_id: int) -> WeeklyPlan:
        pass

    @abstractmethod
    def save_food_plan(self, plan: PlanDTO) -> Plan:
        pass

    @abstractmethod
    def get_food_plan_by_user_id(self, user_id: str) -> Plan:
        pass

    @abstractmethod
    def put_user_plan(self, user_id: str, assignment: PlanAssignmentDTO) -> PlanAssignment:
        pass

    @abstractmethod
    def get_foods_from_plan(self, plan_id: int) -> list[Food]:
        pass

    @abstractmethod
    def get_foods_from_user_plan(self, user_id: str) -> list[Food]:
        pass

    @abstractmethod
    def save_food_to_user_plan(self, user_id: str, data: FoodLinkDTO) -> WeeklyPlan:
        pass

    @abstractmethod
    def remove_food_from_user_plan(self, user_id: str, data: FoodTimeDTO) -> WeeklyPlan:
        pass

    @abstractmethod
    def update_food_in_plan(self, plan_id: int, data: FoodLinkDTO) -> WeeklyPlan:
        pass

    @abstractmethod
    def create_food_plan_by_preferences(self, user_id: str, preferences: list) -> Plan:
        pass

    @abstractmethod
    def get_food_by_id(self, food_id: int) -> Food:
        pass

    @abstractmethod
    def get_all_foods(self, params: GetAllFoodsParams) -> list[Food]:
        pass

    @abstractmethod
    def save_food_in_db(self, food: FoodDTO) -> Food:
        pass

    @abstractmethod
    def get_ingredients(self, food_id: int) -> Optional[list[str]]:
        pass

    @abstractmethod
    def save_extra_food(self, food: ExtraFoodDTO) -> ExtraFood:
        pass


class FoodService(IFoodService):
    def __init__(self, repository: Optional[IFoodRepository] = None):
        self.repository = repository or FoodRepository()

    def get_plans(self) -> list[Plan]:
        return self.repository.get_plans()

    def get_plan(self, plan_id: int) -> Plan:
        _plan = self.repository.get_plan_by_id(plan_id)

        if not _plan:
            raise NotFoundError(f"Plan with id {plan_id} not found")

        return _plan

    def get_weekly_plan_by_id(self, plan_id: int) -> WeeklyPlan:
        plan = self.get_plan(plan_id)

        _plan = self.repository.get_weekly_plan_by_id(plan_id)

        if not _plan:
            raise NotFoundError(f"Plan with id {plan_id} not found")

        schedule = {}
        for row in _plan:
            day = row.day_name
            moment = row.meal_moment_name
            food = None
            if row.food_id:
                food = {
                    "id": row.food_id,
                    "name": row.food_name,
                    "description": row.food_description,
                    "price": float(row.food_price),
                    "created_at": row.food_created_at
                }
            else:
                food = None

            if day not in schedule:
                schedule[day] = {}

            schedule[day][moment] = food

        return WeeklyPlan(
            **dict(plan),
            weekly_plan=schedule
        )

    def save_food_plan(self, plan: PlanDTO) -> Plan:
        return self.repository.save_plan(plan)

    def get_food_plan_by_user_id(self, user_id: str) -> Plan:
        _plan = self.repository.get_plan_by_user_id(user_id)

        if not _plan:
            raise NotFoundError(f"Plan for user {user_id} not found")

        return _plan

    def put_user_plan(self, user_id: str, assignment: PlanAssignmentDTO) -> PlanAssignment:
        _plan = self.repository.get_plan_by_user_id(user_id)

        if not _plan:
            return self.repository.save_user_plan(user_id, assignment)

        return self.repository.update_user_plan(user_id, assignment)

    def get_foods_from_plan(self, plan_id: int) -> list[Food]:
        return self.repository.get_foods_from_plan(plan_id)

    def get_foods_from_user_plan(self, user_id: str) -> list[Food]:
        _plan = self.repository.get_plan_by_user_id(user_id)

        if not _plan:
            raise NotFoundError(f"Plan for user {user_id} not found")

        return self.repository.get_foods_from_plan(_plan.id_plan)

    def save_food_to_user_plan(self, user_id: str, data: FoodLinkDTO) -> WeeklyPlan:
        _plan = self.repository.get_plan_by_user_id(user_id)

        if not _plan:
            raise NotFoundError(f"Plan for user {user_id} not found")

        _day = self.repository.get_day_by_name(data.day)
        if not _day:
            raise NotFoundError(f"Day {data.day} not found")

        _moment = self.repository.get_moment_by_name(data.moment)
        if not _moment:
            raise NotFoundError(f"Moment {data.moment} not found")

        self.repository.save_food_weekly_plan(
            _plan.id_plan, _day, _moment, data.food_id
        )

        return self.get_weekly_plan_by_id(_plan.id_plan)

    def remove_food_from_user_plan(self, user_id: str, data: FoodTimeDTO) -> WeeklyPlan:
        _plan = self.repository.get_plan_by_user_id(user_id)
        if not _plan:
            raise NotFoundError(f"Plan for user {user_id} not found")

        _day = self.repository.get_day_by_name(data.day)
        if not _day:
            raise NotFoundError(f"Day {data.day} not found")

        _moment = self.repository.get_moment_by_name(data.moment)
        if not _moment:
            raise NotFoundError(f"Moment {data.moment} not found")

        data.day = str(_day)
        data.moment = str(_moment)

        self.repository.remove_food_from_plan(_plan.id_plan, data)

        return self.get_weekly_plan_by_id(_plan.id_plan)

    def update_food_in_plan(self, plan_id: int, data: FoodLinkDTO) -> WeeklyPlan:
        _plan = self.repository.get_plan_by_id(plan_id)
        if not _plan:
            raise NotFoundError(f"Plan with id {plan_id} not found")

        _day = self.repository.get_day_by_name(data.day)
        if not _day:
            raise NotFoundError(f"Day {data.day} not found")

        _moment = self.repository.get_moment_by_name(data.moment)
        if not _moment:
            raise NotFoundError(f"Moment {data.moment} not found")

        data.day = str(_day)
        data.moment = str(_moment)

        self.repository.update_food_weekly_plan(plan_id, data)

        return self.get_weekly_plan_by_id(plan_id)

    def create_food_plan_by_preferences(self, user_id: str, preferences: list) -> Plan:
        food_id_placeholders = [str(int(fid)) for fid in preferences]
        _matches = self.repository.get_matching_food_ids(food_id_placeholders)
        if not _matches:
            raise NotFoundError("No matching foods found")

        _new_plan = PlanDTO(
            title=f"Plan for user {user_id}",
            plan_description=f"Generated from selected food IDs",
            objetive="Automatically generated based on preferences"
        )

        new_plan: Plan = self.save_food_plan(_new_plan)

        _days = self.repository.get_days()
        _moments = self.repository.get_moments()

        food_index = 0
        total_foods = len(_matches)

        for day in _days:
            for moment in _moments:
                food_id = _matches[food_index % total_foods]
                self.repository.save_food_weekly_plan(
                    new_plan.id_plan, day["id"], moment["id"], food_id
                )
                food_index += 1

        self.put_user_plan(user_id, PlanAssignmentDTO(
            plan_id=new_plan.id_plan
        ))

        _ret = self.repository.get_plan_by_id(new_plan.id_plan)
        if not _ret:
            raise NotFoundError(f"Plan with id {new_plan.id_plan} not found")

        return _ret

    def get_food_by_id(self, food_id: int) -> Food:
        food = self.repository.get_food_by_id(food_id)

        if not food:
            raise NotFoundError(f"Food with id {food_id} not found")

        return food

    def get_all_foods(self, params: GetAllFoodsParams) -> list[Food]:
        return self.repository.get_all_foods(params)

    def save_food_in_db(self, food: FoodDTO) -> Food:
        return self.repository.save_food(food)

    def save_extra_food(self, food: ExtraFoodDTO, userId: str) -> ExtraFood:
        extra_food: ExtraFood = self.repository.save_extra_food(food, userId)
        link = self.link_extra_food_with_user(extra_food.id, userId)
        if not link:
            raise NotFoundError("user id invalid")
        return extra_food

    def create_food_plan_by_preferences(self, user_id: str, preferences: list, plan: PlanDTO) -> Plan:
        food_id_placeholders = [str(int(fid)) for fid in preferences]
        _matches = self.repository.get_matching_food_ids(food_id_placeholders)
        if not _matches:
            raise NotFoundError("No matching foods found")

        new_plan: Plan = self.save_food_plan(plan)

        _days = self.repository.get_days()
        _moments = self.repository.get_moments()

        food_index = 0
        total_foods = len(_matches)

        for day in _days:
            for moment in _moments:
                food_id = _matches[food_index % total_foods]
                self.repository.save_food_weekly_plan(
                    new_plan.id_plan, day["id"], moment["id"], food_id
                )
                food_index += 1

        self.put_user_plan(user_id, PlanAssignmentDTO(
            plan_id=new_plan.id_plan
        ))

        _ret = self.repository.get_plan_by_id(new_plan.id_plan)
        if not _ret:
            raise NotFoundError(f"Plan with id {new_plan.id_plan} not found")

        return _ret

    def get_ingredients(self, food_id: int) -> list[str]:
        ingredients = self.repository.get_ingredients_by_food_id(food_id)

        if not ingredients:
            raise NotFoundError(
                f"Ingredients for food with id {food_id} not found")

        return ingredients
