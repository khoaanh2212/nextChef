from domain.recipe.edamam.Edamam import Edamam
from ..BaseRepository import BaseRepository


class EdamamRepository(BaseRepository):
    def __init__(self, model):
        BaseRepository.__init__(self, model)

    @staticmethod
    def new(model = Edamam):
        return EdamamRepository(model)
