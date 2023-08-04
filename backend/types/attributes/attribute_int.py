from backend.types.attributes.base_attribute import BaseAttribute


class AttributeInt(BaseAttribute):
    def clean_value(self, value):
        return super(AttributeInt, self).clean_value(int(value))
