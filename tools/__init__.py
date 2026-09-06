from .time_tool import get_current_time, time_tool_schema
from .calculator import calculate, calculator_schema
from .file_reader import read_file, file_reader_schema
from .file_writer import write_file, file_writer_schema
from .web_search import search_web, web_search_schema
from .analyze_job import analyze_job_posting, analyze_job_posting_schema
from .save_application import save_application_details, save_application_schema
from .memory import save_memory, recall_memory, save_memory_schema, recall_memory_schema, list_memories, list_memories_schema
tools = [time_tool_schema, calculator_schema, file_reader_schema, file_writer_schema, web_search_schema, save_memory_schema, recall_memory_schema, list_memories_schema, analyze_job_posting_schema, save_application_schema]

available_functions = {
    "get_current_time": get_current_time,
    "calculate": calculate,
    "read_file": read_file,
    "write_file": write_file,
    "web_search": search_web,
    "save_memory": save_memory,
    "recall_memory": recall_memory,
    "analyze_job_posting": analyze_job_posting,
    "save_application": save_application_details,
    "list_memories": list_memories
}