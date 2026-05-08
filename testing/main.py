def generate_action(action):
    if action["type"] == "print":
        return f'print("{action["text"]}")'
    
    return "# unknown action"

def generate_code(data):
    code = ""

    if data["event"] == "on_click":
        code += "def on_click():\n"

        for action in data["action"]:
            line = generate_action(action)
            code += "   " + line + "\n"
    
    return code

print("masukan kata/kalimat untuk diprint: ")
user_text = input("> ")

data = {
    "event": "on_click",
    "action": [
        {"type": "print", "text": user_text}
    ]
}

result = generate_code(data)
print(result)