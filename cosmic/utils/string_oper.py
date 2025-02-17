import re
from num2words import num2words


def to_snake_case(name: str) -> str:
    """Converts a given string to snake_case.

    Args:
        name (str): The string to be converted.

    Returns:
        str: The string in snake_case.
    """
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def generate_function_name(condition: str) -> str:
    """Resolve the function name from the condition.
    :Warning: This function is implemented just as a placeholder.
    It is advised to not declare anonymous functions in the xml file.

    Args:
        condition (str): The condition to be resolved.

    Returns:
        str: the function name.
    """
    operators_map = {
        "!=": "neq",
        "==": "eq",
        ">": "gt",
        "<": "lt",
        ">=": "gte",
        "<=": "lte",
        "&&": "and",
        "||": "or",
    }
    if condition.startswith("!"):
        condition = condition[1:]
    if condition.endswith("++"):
        condition = condition.replace("++", "_increment")
    if condition.endswith("--"):
        condition = condition.replace("--", "_decrement")
    components = condition.replace("\n", "").split(" ")
    components_processed = [None] * len(components)
    for idx, c in enumerate(components):
        if c.isnumeric():
            components_processed[idx] = to_snake_case(
                num2words(c).replace(" ", "_").replace("-", "_"),
            )
        else:
            components_processed[idx] = to_snake_case(operators_map.get(c, c))
    return "_".join(components_processed)
