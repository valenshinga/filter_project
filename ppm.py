from PIL import Image 

class PPM:
    @classmethod
    def empty_PPM(cls):
        return cls()
    
    @classmethod
    def read(cls, path):
        img = Image.open(path)
        width = img.width
        height = img.height
        res = cls(width, height)
        res.data = img
        return res

    def __init__(self, width=0, height=0):
        self.width = width
        self.height = height
        self.size = width * height
        self.data = Image.new("RGB", (width, height), color="black")

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Imagen de dimension: ({self.width}, {self.height})"
    
    def __setitem__(self, key, new_value):
        self.data.putpixel(key, new_value)
    
    def __getitem__(self, key):
        return self.data.getpixel(key)
    
    def show(self):
        self.data.show()

    def write(self, path):
        self.data.save(path)
        