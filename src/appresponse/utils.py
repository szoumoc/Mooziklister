
import re
import ast

def extract_dict(response_text):
    match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
    if match:
        dict_string = match.group(1)
        try:
            return ast.literal_eval(dict_string)
        except Exception as e:
            print(f"Error parsing dict: {e}")
    return None


