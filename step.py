from sentence import Sentence


class Step(Sentence):
  def __init__(self, id) -> None:
    super().__init__(id)
    self.entity_types = []
    
