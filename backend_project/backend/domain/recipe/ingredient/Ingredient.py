from domain.recipe.SelectedAllergens import EdamamSelectedAllergens


class Ingredient:
    def __init__(self, text, weight_in_gr = 0, measure = '', quantity = 1, allergens = EdamamSelectedAllergens(list())):
        self.text = text
        self.weight_in_gr = weight_in_gr
        self.measure = measure
        self.quantity = quantity
        self.allergens = allergens

    def to_dto(self):
        return {
            "text": self.text,
            "weight_in_gr": self.weight_in_gr,
            "measure": self.measure,
            "quantity": self.quantity,
            "allergens": self.allergens.selected_allergens,
        }
