

class Chef:

    def __init__(self, chef):
        self.chef = chef

    def toDTO(self):
        return {
            'id': self.chef.id,
            'name': self.chef.name,
            'surname': self.chef.surname,
            'email': self.chef.email,
            'avatar': self.chef.avatar_thumb('chef_avatar')
        }
