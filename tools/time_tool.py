from datetime import datetime

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

time_tool_schema = {
    "type":"function",
    "function": {
        "name": "get_current_time",
        "description": "Get the current time and date",
        "parameters":{
            "type":"object",
            "properties":{},
            "required":[]
        }
    }
}