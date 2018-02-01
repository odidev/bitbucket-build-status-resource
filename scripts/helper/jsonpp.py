import json


# Convenience method for pretty-printing JSON
def json_pp(data):
    print dir(json)
    if isinstance(data, dict):
        return json.dumps(data,
                          sort_keys=True,
                          indent=4,
                          separators=(',', ':')) + "\n"
    elif isinstance(data, str):
        return json.dumps(json.loads(data),
                          sort_keys=True,
                          indent=4,
                          separators=(',', ':')) + "\n"
    else:
        raise NameError('Must be a dictionary or json-formatted string')