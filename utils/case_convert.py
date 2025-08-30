import re

def to_snake(camel_str: str) -> str:
    """
    convert from camel case string to snake case string
    """
    if not isinstance(camel_str, str) or not camel_str:
        return camel_str
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def convert_dict_keys(d: dict, converter) -> dict:
    new_dict = {}
    for k, v in d.items():
        new_key = converter(k)
        if isinstance(v, dict):
            new_dict[new_key] = convert_dict_keys(v, converter)
        elif isinstance(v, list):
            new_dict[new_key] = [
                convert_dict_keys(i, converter) if isinstance(i, dict) else i for i in v
            ]
        else:
            new_dict[new_key] = v
    return new_dict