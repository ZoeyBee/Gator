from backend.types.attributes.attribute_int import AttributeInt


class AttributeCombo(AttributeInt):
    def __init__(self, parent, name, attribute):
        super(AttributeCombo, self).__init__(parent, name, attribute)
        self.options = attribute['options']
