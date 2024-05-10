
from datetime import datetime
import json

def write_token_file(cob_name_1, token_1, cob_name_2, token_2):
    # Create dictionary with cob_name_1, cob_name_2, and current datetime
    token_dict = {
        cob_name_1: token_1,
        cob_name_2: token_2,
        "datetime": int(datetime.now().timestamp())
    }

    # Write dictionary to a .txt file
    with open("tokens.txt", "w") as file:
        json.dump(token_dict, file)

    return

def read_token_file():
    # Read dictionary from the .txt file
    with open("tokens.txt", "r") as file:
        token_dict = json.load(file)
    return token_dict