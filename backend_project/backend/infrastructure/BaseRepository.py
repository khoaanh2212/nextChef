class BaseRepository:

    def __init__(self, model):
        self.model = model

    def save(self, object):
        object.save()
        return object

    def findById(self, id):
        if isinstance(id, list):
            return self.model.objects.filter(id__in=id)
        return self.model.objects.get(id=id)
