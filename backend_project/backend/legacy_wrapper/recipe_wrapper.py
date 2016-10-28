from recipe.models import Recipes
from domain.recipe.SelectedAllergens import SelectedAllergens
from legacy_wrapper.legacymodelwrap import legacymodelwrap


@legacymodelwrap(Recipes)
class Recipe:
    @classmethod
    def new(cls, *args, **kwargs):
        return cls.objects.create(*args, **kwargs)

    @classmethod
    def from_legacy_model(cls, model):
        return cls(model)

    def __init__(self, model):
        self.model = model

    def toDTO(self):
        return {
            'id': self.model.id,
            'name': self.model.name,
            'chef_type_class': self.model.chef.type_class,
            'to_sell': self.model.to_sell,
            'url': self.model.full_url,
            'image_url': self.model.thumb_explore_box,
            'chef_full_name': self.model.chef.full_name,
            'last_comment': self.model.last_comments,
            'nb_likes': self.model.nb_likes,
            'nb_comments': self.model.nb_comments,
            'nb_added': self.model.nb_added,
            'nb_shares': self.model.nb_shares
        }

    def to_dto(self):
        return {
            'allergens': self.model.allergens
        }

    def to_instance(self):
        return self.model

    def save(self, *args, **kwargs):
        return self.model.save(*args, **kwargs)

    def set_allergens(self, selected_allergens):
        self.model.allergens = selected_allergens.toAllergenString()

    def get_allergens(self):
        return SelectedAllergens.new(self.model.allergens.split(", "))
