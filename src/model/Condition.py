import re

class Condition:
    def __init__(self, condition_statement=None, values=None):
        self.condition_statement = condition_statement if condition_statement is not None else ""
        self.values = values if values is not None else []
        
    def __init__(self, statement):
        statements = re.split(r'(?<!\|)\|(?!\|)', statement)
        condition_matrix_values = []
        if len(statements) > 1:
            for i in range(1, len(statements[1]), 2):
                condition_matrix_values.append(
                    self.convert_condition_value_to_boolean(statements[1][i])
                )
        self.condition_statement=statements[0].strip()
        self.values=condition_matrix_values
    
    def convert_condition_value_to_boolean(self, value):
        if value == 'Y':
            return True
        else:
            return False