from ingredient import Ingredient
from step import Step


class Recipe:

  def __init__(self, recipe_id):
    self.id = recipe_id
    self.questions_dict = dict()
    self.answers_dict = dict()
    self.ingredients = []
    self.steps = []