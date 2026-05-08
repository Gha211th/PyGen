import json
import re
import os

splash_text = r"""
    ____        ______                    
   / __ \__  __/ ____/__  ____  ___  _____
  / /_/ / / / / / __/ _ \/ __ \/ _ \/ ___/
 / ____/ /_/ / /_/ /  __/ / / /  __/ /    
/_/    \__, /\____/\___/_/ /_/\___/_/     
      /____/
"""

user_guide = r"""
!Note: Please select by the number (ex: 1 = print)

1. print    2. If Statement     3. For Loop     4. Variable     5. If-Else

command: press "c" for clear the system

"""

def detect_value(value):
    if value.isdigit():
        return value
    elif value == "True" or value == "False":
        return value
    else:
        return f'"{value}"'

def change_space(var_name):
    var_name = var_name.lower()
    var_name = var_name.replace(" ", "_")
    var_name = re.sub(r'[^a-zA-Z0-9_]', '', var_name)

    return var_name

def generate_action(action, indent=1):
    
    space = "    " * indent

    if action["type"] == "print":
        return space + f'print("{action["text"]}")\n'

    elif action["type"] == "if":
        if_state = space + f'if {action["condition"]}:\n'

        for child in action["action"]:
            if_state += generate_action(child, indent + 1)

        return if_state

    elif action["type"] == "if-else":
        if_state = space + f'if {action["condition"]}:\n'

        for child in action["action"]:
            if_state += generate_action(child, indent + 1)

        else_state = space + f'else:\n'

        for child in action["action"]:
            else_state += generate_action(child, indent + 1)

        return if_state + else_state

    elif action["type"] == "loop":
        for_loop = space + f'for i in range({action["times"]}):\n'

        for child in action["action"]:
            for_loop += generate_action(child, indent + 1)

        return for_loop

    elif action["type"] == "set":
        value = detect_value(action["value"])

        return space + f'{action["name"]} = {value}\n'

    return space + "#unknown action / value :("

def generate_code(data):
    code = ""

    if data["event"] == "function":
        code += "\ndef MyFunction():\n"

        for action in data["action"]:
            code += generate_action(action)

    return code

# print splash also the input/output

print(f'{splash_text}\n')

while True:
    print("What do you want to make? (command --help to see the list or 'q' to quit):")
    input_select = input(">> ").lower()

    if input_select == "--help":
        print(user_guide)
    
    elif input_select == "c":
        os.system("clear")

    elif input_select == "q":
        break

    elif input_select == "1":
        print("type any text to print: ")
        user_data = input(">> ")
        data = {
                "event": "function",
                "action": [
                    {"type": "print", "text": user_data}
                    ]
                }

        result = generate_code(data)
        print(result)

    elif input_select == "2":
        print("Build If Condition: ")
        user_data = input(">> ")
        data = {
                "event": "function",
                "action": [
                    {
                        "type": "if",
                        "condition": "user_data",
                        "action": [
                            {"type": "print", "text": "If Statement was created!"}
                            ]
                        }
                    ]
                }
        
        result = generate_code(data)
        print(result)

    elif input_select == "5":
        print("build the if-else state condition: ")
        user_data = input(">> ")
        data = {
                "event": "function",
                "action": [
                    {
                        "type": "if-else",
                        "condition": user_data,
                        "action": [
                            {"type": "print", "text": "if-else state was created!"}
                            ]
                        }
                    ]
                }

        result = generate_code(data)
        print(result)


    elif input_select == "3":
        print("Build For Loop: ")
        user_data = input(">> ")
        data = {
                "event": "function",
                "action": [
                    {
                        "type": "if",
                        "times": user_data,
                        "action": [
                            {"type": "print", "text": "for loop is created!"}
                            ]
                        }
                    ]
                }

        result = generate_code(data)
        print(result)

    elif input_select == "4":
        print("Give The variable name: ")
        var_name = change_space(input(">> "))
        print(f'Give the value for {var_name} ex: String/Boolean/Integer: ')
        var_value = input(">> ")

        data = {
                "event": "function",
                "action": [
                    {
                        "type": "set",
                        "name": var_name,
                        "value": var_value
                        }
                    ]
                }

        result = generate_code(data)
        print(result)
