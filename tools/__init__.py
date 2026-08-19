from.time_tool import get_current_time, time_tool_schema
from calculator import calculate, calculator_schema
from file_reader import read_file, file_reader_schema

tools = [time_tool_schema, calculator_schema, file_reader_schema]

available_functions = {
    "get_current_time": get_current_time,
    "calculate": calculate,
    "read_file": read_file
}