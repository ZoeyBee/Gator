from utils.dict_place_or_create import dict_place_or_create


class AttributeManagerMixin:
    def __init__(self, *args, **kwargs):
        super(AttributeManagerMixin, self).__init__(*args, **kwargs)
        self.animated_attributes = {}

    def set_attribute_animated(self, attribute, animated):
        if animated:
            dict_place_or_create(self.animated_attributes, attribute.parent.uid, attribute.name, attribute)
        else:
            if attribute.animated:
                self.animated_attributes[attribute.parent.uid].pop(attribute.name)
                if not self.animated_attributes[attribute.parent.uid]:
                    self.animated_attributes.pop(attribute.parent.uid)
        attribute.animated = animated
        self.signals.call_signal('attribute_animated_changed', attribute)
