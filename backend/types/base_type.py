from backend.types.attributes.base_attribute import BaseAttribute
from backend.types.attributes.attribute_int import AttributeInt
from backend.types.attributes.attribute_combo import AttributeCombo
from backend.types.attributes.attribute_position import AttributePosition
from backend.types.attributes.attribute_invisible import AttributeInvisible
from backend.types.keyframe import Keyframe


class BaseType:
    def __init__(self, data=None, uid=None, *args, **kwargs):
        super(BaseType, self).__init__(*args, **kwargs)
        self.uid = uid
        self.data = data
        self.attribute_change_listeners = []
        self.deleted = False
        if data is not None and uid is not None: self.data.objects[self.uid] = self

    def add_attribute_change_listener(self, callback):
        self.attribute_change_listeners.append(callback)

    def setup_attribute(self, attribute_name, attribute):
        attr = BaseAttribute
        if attribute['type'] == 'int':         attr = AttributeInt
        elif attribute['type'] == 'combo':     attr = AttributeCombo
        elif attribute['type'] == 'invisible': attr = AttributeInvisible
        elif 'position' in attribute['type']:  attr = AttributePosition

        self.attributes[attribute_name] = attr(self, attribute_name, attribute)
        self.keyframes[1][attribute_name] = Keyframe(
            self.data, self.uid, 1, self.attributes[attribute_name],
            attribute['value'], self.keyframes)
        for listener in self.attribute_change_listeners: listener(self.attributes[attribute_name], 'add')

    def setup_attributes(self, attribute_dict):
        self.attributes = {}; self.keyframes = {}
        for attribute_name, attribute in attribute_dict.items():
            self.setup_attribute(attribute_name, attribute)

    def get_attribute_value(self, attribute_name, frame):
        return self.attributes[attribute_name].get_value(frame)

    def get_attribute_values(self, frame):
        result = {}
        for attribute_name, attribute in self.attributes.items():
            result[attribute_name] = attribute.get_value(frame)
        return result

    def get_keyframes(self):
        for frame, keyframes in list(self.keyframes.items()):
            for attribute_name, keyframe in list(keyframes.items()):
                yield(frame, attribute_name, keyframe)

    def delete(self):
        for __, __, keyframe in list(self.get_keyframes()): keyframe.delete()
        self.deleted = True
        if self.uid and self.data:
            self.data.objects.pop(self.uid)
