import re

class Dependency:
    def __init__(self, type=None, value=None):
        self.type = type
        self.value = value
    
    @classmethod
    def create(cls, statement):
        statements = re.split(r'(?<!\|)\|(?!\|)', statement)
        if "CALL " in statements[0]:
            return True, cls("Rule", cls.extract_child_rule_name(statements[0]))
        if re.search(r'([A-Z]{4}_[A-Z]{2}_[_A-Z0-9]+)\(\w+(, \w+)*\)', statements[0]):
            return True, cls("Rule", cls.extract_child_rule_name2(statements[0]))
        if "GET " in statements[0]:
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
    def extract_child_rule_name2(statement):
        pattern = r'([A-Z]{4}_[A-Z]{2}_[_A-Z0-9]+)\(\w+(, \w+)*\)'
        child_rule_name = re.search(pattern, statement)
        return child_rule_name.group(1)

    
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
        