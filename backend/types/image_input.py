from backend.types.base_type import BaseType
from PIL import Image


class ImageInput(BaseType):
    type = 'Image'

    def __init__(self, input_path, *args, **kwargs):
        super(ImageInput, self).__init__(*args, **kwargs)
        self.input_path = input_path
        self.image = Image.open(self.input_path)

    def get_image(self, *args, **kwargs):
        return self.image
