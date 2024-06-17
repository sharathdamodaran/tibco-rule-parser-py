class Action:
    def __init__(self):
        self.type = None
        self.value = None
        self.parameters = []
        self.dependencies = []
        
    def to_dict(self):
        return {
            'type': self.type,
            'value': self.value,
            'parameters': self.parameters,
            'dependencies': self.dependencies,
        }