class Rule:
    def __init__(self, name=None, summary=None, unit=None, parameters=None, variables=None, expressions=None, errors=None, dependencies=None):
        self.name = name
        self.summary = summary
        self.unit = unit
        self.parameters = parameters if parameters is not None else []
        self.variables = variables if variables is not None else []
        self.expressions = expressions if expressions is not None else []
        self.errors =  errors if errors is not None else []
        self.dependencies =  dependencies if dependencies is not None else []

    def process_declaration_section(self, declaration_section):
        self.variables = []
        self.parameters = []
        for statement in declaration_section.split("\n"):
            invalid_statement = ";" not in statement
            if invalid_statement:
                continue
            if "LOCAL" in statement:
                rule_vars = statement.split("LOCAL")[1].split(";")[0].strip()
                self.variables=rule_vars.split(", ")
            elif "(" in statement:
                rule_def = statement.split("(")
                self.name=rule_def[0].strip()
                rule_params = rule_def[1].split(")")[0]
                self.parameters=rule_params.split(", ")
            else:
                self.name=statement[:statement.find(";")].strip()

    def process_summary_section(self, summary_section):
        for statement in summary_section.split("\n"):
            if "Summary" in statement:
                rule_summaries = statement.split(":")
                self.summary = rule_summaries[1][:rule_summaries[1].find("|")].strip()
            elif "Unit" in statement:
                rule_units = statement.split(":")
                self.unit = rule_units[1][:rule_units[1].find("  ")].strip()

    def __init__(self, declaration_section, summary_section):
        self.process_declaration_section(declaration_section)
        self.process_summary_section(summary_section)
        
    def to_dict(self):
        return {
            'name': self.name,
            'summary': self.summary,
            'unit': self.unit,
            'parameters': self.parameters,
            'variables': self.variables,
            'expressions': [expression.to_dict() for expression in self.expressions],
            'errors': [error.to_dict() for error in self.errors],
            'dependencies': [dependency.to_dict() for dependency in self.dependencies],
        }
