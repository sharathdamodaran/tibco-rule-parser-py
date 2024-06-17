from .Action import Action

class Expression:
    def __init__(self, type=None, value=None, actions=None):
        self.type = type
        self.value = value
        self.actions = actions if actions is not None else []
        
    def __init__(self, index, action_statements, conditions):
        exp_value = next((condition for condition in conditions if condition.values[index] == True), None)
        if exp_value is not None:
            self.value=exp_value.condition_statement
            self.type="Condition"
        else:
            self.value=""
            self.type="Default"
        actions = []
        for statement in action_statements:
            if len(statement.values) >= index + 1 and statement.values[index] == True:
                action = Action()
                action.value=statement.statement
                actions.append(action)
        self.actions=actions
                
        
    def to_dict(self):
        return {
            'type': self.type,
            'value': self.value,
            'actions': [action.to_dict() for action in self.actions],
        }