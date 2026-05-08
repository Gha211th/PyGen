import json

splash_text = r"""
    ____        ______                    
   / __ \__  __/ ____/__  ____  ___  _____
  / /_/ / / / / / __/ _ \/ __ \/ _ \/ ___/
 / ____/ /_/ / /_/ /  __/ / / /  __/ /    
/_/    \__, /\____/\___/_/ /_/\___/_/     
      /____/
"""

def detect_value(value):
    if value.isdigit():
        return value
    elif value == "True" or value == "False":
        return value
    else:
        return f'"{value}"'

def generate_action(action, indent=1):
    space = "    " * indent

    if action["type"] == "print":
        return space + f'print("{action["text"]}")\n'
    
    elif action["type"] == "if":
        code = space + f'if {action["condition"]}:\n'

        for child in action["action"]:
            code += generate_action(child, indent + 1)

        return code
    
    elif action["type"] == "loop":
        code = space + f'for i in range({action["times"]}):\n'

        for child in action["action"]:
            code += generate_action(child, indent + 1)
        
        return code

    elif action["type"] == "set":
        value = detect_value(action["value"])

        return space + f'{action["name"]} = {value}\n'
    
    return space + "# unknown action"

def generate_code(data):
    code = ""

    if data["event"] == "MyFunction":
        code += "def MyFunction():\n"

        for action in data["action"]:
            code += generate_action(action)
    
    return code

print(f'{splash_text}\n')
print("Please select something that you want to create: \n 1. Print\n 2. If Statement\n 3. For Loop\n 4. Variable")
input_select = int(input(">> "))

if input_select == 1:
    print("mau print apa: ")
    data_user = input(">> ")
    data = {
            "event": "MyFunction",
            "action": [
                {"type": "print", "text": data_user}
                ]
            }

    result = generate_code(data)
    print(result)

elif input_select == 2:
    print("Build If Condition: ")
    data_user = input(">> ")
    data = {
            "event": "MyFunction",
            "action": [{
                "type": "if",
                "condition": data_user,
                "action": [
                    {"type": "print", "text": "If Statement Is Created!"}
                    ]
                }]
            }

    result = generate_code(data)
    print(result)

elif input_select == 3:
    print("Build For Loop: ")
    data_user = input(">> ")
    data = {
            "event": "MyFunction",
            "action": [
                {
                    "type": "loop",
                    "times": data_user,
                    "action": [
                        {"type": "print", "text": "for loop is generated"}
                        ]
                    }
                ]
            }

    result = generate_code(data)
    print(result)

elif input_select == 4:
    print("give variable name: ")
    var_name = input(">> ")
    print("give the value ex: String/Integer/Boolean: ")
    var_value = input(">> ")

    data = {
            "event": "MyFunction",
            "action": [
                {"type": "set", "value": var_value, "name": var_name}
                ]
            }

    result = generate_code(data)
    print(result)

    
    
