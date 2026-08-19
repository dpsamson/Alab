def write_file(filepath: str, content: str):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing the file: {e}"

file_writer_schema = {
    "type":"function",
    "function": {
        "name": "write_file",
        "description": "Writes the content to a file or overwriting a file",
        "parameters":{
            "type":"object",
            "properties":{
                "filepath":{
                    "type":"string",
                    "description":"The path to the file to write"
                },
                "content":{
                    "type":"string",
                    "description":"The content to write to the file"
                }
            },
            "required":["filepath", "content"]
        }
    }
}