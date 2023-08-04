from backend.types.attributes.base_attribute import BaseAttribute


class AttributeInvisible(BaseAttribute):
    def __init__(self, parent, name, attribute):
        self.maximum = attribute['value']
        self.minimum = attribute['value']
        super(AttributeInvisible, self).__init__(parent, name, attribute)

    def clean_value(self, value):
        return value
