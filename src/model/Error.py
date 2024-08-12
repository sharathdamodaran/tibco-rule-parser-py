from .Action import Action

class Error:
    def __init__(self, type=None, value=None, actions=None):
        self.type = type
        self.value = value
        self.actions = actions if actions is not None else []
        
    def __init__(self, statements):
        actions = []
        for statement in statements.split("\n"):
            if ":" in statement:
                self.value = statement[:statement.find(":")].strip()
            elif ";" in statement:
                action = Action()
                action.value=statement.strip()
                actions.append(action)
        self.type = "Exception"
        self.actions = actions
            
                
        
    def to_dict(self):
        return {
            'type': self.type,
            'value': self.value,
            'actions': [action.to_dict() for action in self.actions],
        }