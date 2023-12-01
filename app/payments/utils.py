import regex as re
from app.payments.banks import (
    get_data_bcp,
    get_data_ibk,
    get_data_bbva,
    get_data_scotiabank,
    get_data_banbif,
)

BANK_FUNCTIONS = {
    "BCP": get_data_bcp,
    "INTERBANK": get_data_ibk,
    "BBVA": get_data_bbva,
    "SCOTIABANK": get_data_scotiabank,
    "BANBIF": get_data_banbif,
}

BANK_PATTERNS = {
    "BCP": re.compile(r"BCP"),
    "INTERBANK": re.compile(r"INTERBANK"),
    "BBVA": re.compile(r"BBV"),
    "SCOTIABANK": re.compile(r"SCOTIABANK"),
    "BANBIF": re.compile(r"BANBIF"),
}

def select_bank(result_list):
    length = len(result_list)
    try:
        for key, pattern in BANK_PATTERNS.items():
            for result in result_list[:length//2]:
                if pattern.search(result):
                    return key
    except StopIteration:
        return "BCP"

    
def get_bank_data(selection, result_list):
    try:
        if selection in BANK_FUNCTIONS:
            return BANK_FUNCTIONS[selection](result_list)
        else:
            return BANK_FUNCTIONS["BCP"](result_list)
    except Exception as e:
        print(f"Error getting bank data: {str(e)}")
        return {}
