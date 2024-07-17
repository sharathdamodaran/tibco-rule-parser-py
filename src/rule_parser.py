import json
import model.ActionStatement
import model.Condition
import model.Expression
import model.Dependency

def create_rule(rule_location):    
    conditions = []
    actions = []
    dependencies = []

    with open(rule_location, 'r') as file:
        sections = file.read().split('--------------\n')

    first_section = sections[0]
    first_sections = first_section.split('+---------------------------------------------------------------------------+\n')

    declaration_section = first_sections[0]
    summary_section = first_sections[1]
    condition_section = first_sections[2]
    action_section = sections[1]
    error_section = ""
    if len(sections)==3:
        error_section = sections[2]

    rule = model.Rule(declaration_section, summary_section)

    for statement in condition_section.split("\n"):
        if statement.startswith(" ---"):
            continue
        condition = model.Condition(statement.strip())
        conditions.append(condition)
        
        is_exist, dependency = model.Dependency.create(statement.strip())
        if is_exist:
            dependencies.append(dependency)

    prev_action = None
    for statement in action_section.split("\n"):
        if statement.startswith(" ---"):
            continue
        is_new, action = model.ActionStatement.create_or_update(statement.strip(), prev_action)
        if is_new:
            prev_action=action
            actions.append(action)

        is_exist, dependency = model.Dependency.create(statement.strip())
        if is_exist:
            dependencies.append(dependency)

    expressions = []
    matrix_length = 1
    if len(conditions)>0:
        matrix_length = len(conditions[0].values)

    for i in range(matrix_length):
        expression = model.Expression(i, actions, conditions)
        expressions.append(expression)
    rule.expressions=expressions

    errors = []
    if error_section != "":
        for statements in [s for s in error_section.split(" ON") if s]:
            error = model.Error(statements)
            errors.append(error)

            for statement in statements.split("\n"):
                is_exist, dependency = model.Dependency.create(statement.strip())
                if is_exist:
                    dependencies.append(dependency)
    rule.errors = errors
    rule.dependencies = dependencies

    return rule

# for i in range(1, 44):
#     rule = create_rule("resources/rules/Rule"+str(i))
#     rule_dict = rule.to_dict()
#     json_string = json.dumps(rule_dict, indent=2)
#     print(json_string)
#     print("Rule Number is =============> ",i)
    
# rule = create_rule("resources/rules/Rule32")
# rule_dict = rule.to_dict()
# json_string = json.dumps(rule_dict, indent=2)
# print(json_string)    