class Rule:
    def __init__(self, name=None, parameters=None, variables=None, expressions=None):
        self.name = name
        self.parameters = parameters if parameters is not None else []
        self.variables = variables if variables is not None else []
        self.expressions = expressions if expressions is not None else []
    
    def __init__(self, declaration_section):
        self.variables = []
        self.parameters = []
        for statement in declaration_section.split("\n"):
            invalid_statement = ";" not in statement
            if invalid_statement:
                continue
            if "LOCAL" in statement:
                rule_vars = statement.split("LOCAL")[1].split(";")[0]
                self.variables=rule_vars.split(",")
            if "(" in statement:
                rule_def = statement.split("(")
                self.name=rule_def[0]
                rule_params = rule_def[1].split(")")[0]
                self.parameters=rule_params.split(",")
            else:
                self.name=statement[:statement.find(";")].strip()
        
    def to_dict(self):
        return {
            'name': self.name,
            'parameters': self.parameters,
            'variables': self.variables,
            'expressions': [expression.to_dict() for expression in self.expressions],
        }
