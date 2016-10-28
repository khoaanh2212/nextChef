from books.models import Book
from legacy_wrapper.legacymodelwrap import legacymodelwrap
from domain.book.Collaborators import Collaborators

@legacymodelwrap(Book)
class Book:

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
            'collaborators': self.model.collaborators
        }

    def save(self, *args, **kwargs):
        return self.model.save(*args, **kwargs)

    def set_collaborators(self, collaborators):
        self.model.collaborators = collaborators.toCollaboratorString()

    def get_collaborators(self):
        return Collaborators.new(self.model.collaborators.split(", "))

