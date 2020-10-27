
class NuroaModel:
    def __init__(self, *args, **kwargs):
        self.__dict__.update(args, **kwargs)

    def __str__(self):

        return f"Name: {self.name}"
