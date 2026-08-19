def calculate(expression: str):
    try:
        return eval(expression,{"__builtins__": {}})
    except Exception as e:
        return f"Error: {e}"

calculator_schema ={
    "type":"function",
    "function": {
        "name": "calculate",
        "description": "Evaluate a mathematical expression, e.g. '47 * 12'",
        "parameters":{
            "type":"object",
            "properties":{
                "expression":{
                    "type":"string",
                    "description":"The math expression to evaluate"
                }
            },
            "required":["expression"]
        }
    }
}