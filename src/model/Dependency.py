class Dependency:
    def __init__(self, type=None, value=None):
        self.type = type
        self.value = value
    
    @classmethod
    def create(cls, statement):
        statements = statement.split("|")
        if "CALL" in statements[0]:
            return True, cls("Rule", cls.extract_child_rule_name(statements[0]))
        if "GET" in statements[0]:
            return True, cls("Database", cls.extract_database_table_name(statements[0]))
        return False, None

    @staticmethod
    def extract_child_rule_name(statement):
        child_rule_name = statement
        if ";" in statement:
            child_rule_name=statement[:statement.index(";")]

        has_parameters = "(" in child_rule_name
        if has_parameters:
            child_rule_name = child_rule_name[child_rule_name.index("CALL") + 5:child_rule_name.index("(")]
        else:
            child_rule_name = child_rule_name[child_rule_name.index("CALL") + 5:]
            
        return child_rule_name   
    
    @staticmethod
    def extract_database_table_name(statement):
        table_name = statement
        if ";" in statement:
            table_name=statement[:statement.index(";")]

        has_parameters = "(" in table_name
        if has_parameters:
            table_name = table_name[table_name.index("GET") + 4:table_name.index("(")]
        else:
            table_name = table_name[table_name.index("GET") + 4:]
            
        return table_name
    
    def to_dict(self):
        return {
            'type': self.type,
            'value': self.value,
        }
        