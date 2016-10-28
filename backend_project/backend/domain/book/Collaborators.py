from domain.InvalidArgumentException import InvalidDomainArgumentException
from django.conf import settings
from chefs.models import Chefs


class InvalidCollaborator(InvalidDomainArgumentException):
    pass


class Collaborators:
    def __init__(self, collaborators):
        self.collaborators = collaborators

    @staticmethod
    def new(collaborators=list()):

        if not all(isinstance(x, Chefs) for x in collaborators):
            raise InvalidCollaborator

        return Collaborators(collaborators)

    def add(self, chef):
        if not isinstance(chef, list) and not isinstance(chef, Chefs):
            raise InvalidCollaborator
        elif isinstance(chef, list) and not all(isinstance(x, Chefs) for x in chef):
            raise InvalidCollaborator
        else:
            self.collaborators.extend(chef) if isinstance(chef, list) else self.collaborators.append(chef)

    def __str__(self):
        _str = ''
        for collaborator in self.collaborators:
            _str += '[%d],' % collaborator.id
        return _str

    def toCollaboratorString(self):
        return self.__str__()

    def collaboratorToList(self,str_collaboratos):
        str_collaboratos = str_collaboratos.replace('[', '')
        str_collaboratos = str_collaboratos.replace(']', '')
        arr_collaboratos = str_collaboratos.split(',')
        for index in range(len(arr_collaboratos)):
            if arr_collaboratos[index]:
                arr_collaboratos[index] = int(arr_collaboratos[index])
            else:
                arr_collaboratos[index] = 0
        return arr_collaboratos
