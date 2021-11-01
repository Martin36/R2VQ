import json
from collections import defaultdict
from ingredient import Ingredient
from recipe import Recipe
from step import Step

if __name__ == "__main__":
  with open("text_annotation.csv") as f:
    stats = defaultdict(int)
    recipes = []
    
    def process_newdoc(line):
      recipe_id = line.split("=")[-1].strip()
      recipe = Recipe(recipe_id)
      recipes.append(recipe)
      stats["nr_recipes"] += 1
      return recipe
      
    def process_question(line):
      line_split = line.split("=")
      question_id = line_split[0].split()[-1].strip()
      question_text = line_split[-1].strip()
      stats["nr_questions"] += 1
      return question_id, question_text
    
    def process_answer(line):
      line_split = line.split("=")
      answer_id = line_split[0].split()[-1].strip()
      answer_text = line_split[-1].strip()
      stats["nr_answers"] += 1
      return answer_id, answer_text
      
      
    for line in f:
      if line[0] == "#":
        if "newdoc" in line:
          recipe = process_newdoc(line)
          # Reset sent_id when new recipe
          sent_id = ""

        if "question" in line:
          question_id, question_text = process_question(line)
          recipe.questions_dict[question_id] = question_text
        
        if "answer" in line:
          answer_id, answer_text = process_answer(line)
          recipe.answers_dict[answer_id] = answer_text

        if "sent_id" in line:
          sent_id = line.split("=")[-1]
          if "ingredient" in sent_id:
            ingredient = Ingredient(sent_id)
            recipe.ingredients.append(ingredient)
          if "step" in sent_id:
            step = Step(sent_id)
            recipe.steps.append(step)
        
        if "text" in line:
          text = line.split("=")[-1]
          if "ingredient" in sent_id:
            ingredient.text = text
          if "step" in sent_id:
            step.text = text
      
      else:
        cell_values = line.split("\t")
        if "ingredient" in sent_id:
          for i, value in enumerate(cell_values):
            if i == 0:
              ingredient.token_ids.append(value)
            elif i == 1:
              ingredient.tokens.append(value)
            elif i == 2:
              ingredient.lemmas.append(value)
            elif i == 3:
              ingredient.pos_tags.append(value)
        
        if "step" in sent_id:
          for i, value in enumerate(cell_values):
            if i == 0:
              step.token_ids.append(value)
            elif i == 1:
              step.tokens.append(value)
            elif i == 2:
              step.lemmas.append(value)
            elif i == 3:
              step.pos_tags.append(value)
            elif i == 4:
              step.entity_types.append(value)
            elif i == 5:
              # PART: Word index of the head of EVENT entity when the participant-of relation exists between the event and another entity in current line.
              pass
            elif i == 6:
              # PART: Word index of the head of EVENT entity when the result-of relation exists between the event and another entity in current line.
              pass
  
  with open("stats.json", "w") as f:
    f.write(json.dumps(stats, indent=2))
