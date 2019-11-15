
class NuroaModel:
    def __init__(self, name = '',description='', price= '0.0', features = '',location=''):
        self.name = name
        self.description = description
        self.price = price
        self.features = features
        self.location = location


    def __str__(self):
        return '{0} \n{1} \n{2} \n{3} \n{4}'.format(self.name, self.description, self.price, self.features, self.location)
