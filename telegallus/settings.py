from types import SimpleNamespace

from dotenv import dotenv_values

TEST = True

def get_parameters():
    config = dotenv_values(".env")
    parameters = {}

    for key, value in config.items():
        parts = key.split("_")
        if TEST:
            if parts[0] == "TEST":
                parameters["_".join(parts[1:])] = value
        else:
            if parts[0] != "TEST":
                parameters["_".join(parts)] = value

    return SimpleNamespace(**parameters)


parameters_col = get_parameters()