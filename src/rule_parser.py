import json
import model.ActionStatement
import model.Condition
import model.Expression

def create_expressions_with_actions(action_statements, conditions):
    expressions = []
    matrix_length = len(conditions[0].values)

    for i in range(matrix_length):
        expression = model.Expression()
        exp_value = next((condition for condition in conditions if condition.values[i] == True), None)
        if exp_value is not None:
            expression.value=exp_value.condition_statement
            expression.type="Condition"
        else:
            expression.value=""
            expression.type="Default"
        actions = []
        for statement in action_statements:
            if len(statement.values) >= i + 1 and statement.values[i] == True:
                action = model.Action()
                action.value=statement.statement
                actions.append(action)
        expression.actions=actions
        expressions.append(expression)
    
    return expressions

def create_rule_with_name_parameters_and_variables(declaration_section):
    rule = model.Rule()
    for statement in declaration_section.split("\n"):
        if statement.startswith("_ ---"):
            continue
        if statement.startswith("_ LOCAL "):
            rule_vars = statement.split("LOCAL")[1].split(";")[0]
            rule.variables=rule_vars.split(",")
        else:
            rule_def = statement.split("(")
            rule.name=rule_def[0]
            rule_params = rule_def[1].split(")")[0]
            rule.parameters=rule_params.split(",")
    return rule

def create_condition(statement):
    statements = statement.split("¦")
    condition_matrix_values = []
    if len(statements) > 1:
        for i in range(1, len(statements[1]), 2):
            condition_matrix_values.append(
                convert_condition_value_to_boolean(statements[1][i])
            )
    return model.Condition(statements[0], condition_matrix_values)

def create_action(statement, previous_action):
    statements = statement.split("¦")
    action_matrix_values = []
    if len(statements) == 1 or not statements[1].strip():
        previous_action.statement=previous_action.statement + "\n" + statements[0]
        return False, previous_action
    else:
        for i in range(1, len(statements[1]), 2):
            action_matrix_values.append(
                convert_action_value_to_boolean(statements[1][i])
            )
        return True, model.ActionStatement(statements[0], action_matrix_values)

def convert_condition_value_to_boolean(value):
    if value == 'Y':
        return True
    else:
        return False
    
def convert_action_value_to_boolean(value):
    if value.isdigit():
        return True
    else:
        return False

def create_rule(rule_location):    
    conditions = []
    actions = []

    with open(rule_location, 'r') as file:
        sections = file.read().split('--------------\n')

    first_section = sections[0]
    first_sections = first_section.split('+---------------------------------------------------------------------------+\n')

    declaration_section = first_sections[0]
    summary_section = first_section[1]
    condition_section = first_sections[2]
    action_section = sections[1]
    error_section = ""
    if len(sections)==3:
        error_section = sections[2]

    rule = model.Rule(declaration_section)

    for statement in condition_section.split("\n"):
        if statement.startswith(" ---"):
            continue
        condition = model.Condition(statement.strip())
        conditions.append(condition)

    prev_action = None
    for statement in action_section.split("\n"):
        if statement.startswith(" ---"):
            continue
        is_new, action = model.ActionStatement.create_or_update(statement.strip(), prev_action)
        if is_new:
            prev_action=action
            actions.append(action)

    expressions = []
    matrix_length = 1
    if len(conditions)>0:
        matrix_length = len(conditions[0].values)

    for i in range(matrix_length):
        expression = model.Expression(i, actions, conditions)
        expressions.append(expression)

    rule.expressions=expressions
    return rule

rule = create_rule("resources/RuleExample2.md")
rule_dict = rule.to_dict()
json_string = json.dumps(rule_dict)
print(json_string)