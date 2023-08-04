from backend.types.attributes.base_attribute import BaseAttribute


class AttributePosition(BaseAttribute):
    def __init__(self, parent, name, attribute):
        super(AttributePosition, self).__init__(parent, name, attribute)
        link_name = attribute['link']
        self.dimension = attribute['type'].split(':')[1]
        if link_name in parent.attributes:
            self.link = parent.attributes[link_name]
            self.link.link = self
