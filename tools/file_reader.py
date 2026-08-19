def read_file(filepath: str):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return content[:2000]
    except Exception as e:
        return f"Error reading file: {e}"

file_reader_schema = {
    "type":"function",
    "function": {
        "name": "read_file",
        "description": "Read the content of a file based on the path",
        "parameters":{
            "type":"object",
            "properties":{
                "filepath":{
                    "type":"string",
                    "description":"The path to the file to read"
                }
            },
            "required":["filepath"]
        }
    }
}