import sqlite3

DB_PATH = "memory.db"

def save_application_details(company: str,
                     role: str,
                     missing_skills: str,
                     url: str = None,
                     deadline: str = None,
                     estimated_study_time: str = None) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO applicaitons (company, role, url, deadline, missing_skills, estimated_study_time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (company, role, url, deadline, missing_skills, estimated_study_time))
    conn.commit()
    conn.close()
    return f"Saved application: {role} at {company}."

save_application_schema = {
    "type": "function",
    "function": {
        "name": "save_application",
        "description": "Saves a job application record after analyze_job_posting has extracted the details.",
        "parameters": {
            "type": "object",
            "properties": {
                "company": {"type": "string"},
                "role": {"type": "string"},
                "missing_skills":{"type": "string"},
                "url": {"type": "string"},
                "deadline": {"type": "string"},
                "estimated_study_time": {"type": "string", "description":"AI-guessed estimate using the calculator tool and the time_tool."}
            },
            "required": ["company", "role", "missing_skills"]
        }
    }
} 