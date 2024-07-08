class ActionStatement:
    def __init__(self, statement=None, values=None):
        self.statement = statement
        self.values = values if values is not None else []
    
    @classmethod
    def create_or_update(cls, action_statement, prev_action):
        statements = action_statement.split("|")
        action_matrix_values = []
        if len(statements) == 1 or not statements[1].strip():
            prev_action.statement=prev_action.statement + "\n" + statements[0]
            return False, prev_action
        else:
            for i in range(1, len(statements[1]), 2):
                action_matrix_values.append(
                    cls.convert_action_value_to_boolean(statements[1][i])
                )
            return True, cls(statements[0].strip(),action_matrix_values)
    
    @staticmethod 
    def convert_action_value_to_boolean(value):
        if value.isdigit():
            return True
        else:
            return False
    