class Sentence:

  def __init__(self, id) -> None:
    self.id = id
    self.text = ""
    self.token_ids = []
    self.tokens = []
    self.lemmas = []
    self.pos_tags = []
