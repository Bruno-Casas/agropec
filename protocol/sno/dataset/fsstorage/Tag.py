class Tag:
    read_transform = None
    write_transform = None
    
    def __init__(self, read_transform, write_transform):
        self.read_transform = read_transform
        self.write_transform = write_transform
