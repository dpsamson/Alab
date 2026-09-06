import sqlite3

DB_PATH = "alab_memory.db"

def analyze_job_posting(job_text: str):
    """
    Takes pasted job description text, compares it against known skills
    stored in memory, and returns raw data for the model to reason over.
    Does NOT save the application itself — save_application does that,
    called by the model in a follow-up tool call.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM memory WHERE key LIKE 'skill_%'")
    known_skills = {row[0].replace("skill_",""): row[1] for row in cursor.fetchall()}
    conn.close()

    return{
        "job_text": job_text,
        "known_skills": known_skills,
        "instruction_for_model": (
            "Compare the job_text against known_skills. Extract company, role, "
            "and deadline if present in the test. Identify missing_skills (skills"
            "mentioned in the poisting that are NOT in known_skills). Then call"
            "save_application with the extracted data."
        )
    }

analyze_job_posting_schema = {
    "type": "function",
    "function": {
        "name": "analyze_job_posting",
        "description": "Analyzes a pasted job description against known skills to identify gaps. Always follow this with save_application to persist the result.",
        "parameters":{
            "type": "object",
            "properties":{
                "job_text": {
                    "type": "string",
                    "description": "The full pasted job desciption text"
                }
            },
            "required": ["job_text"]
        }
    }
}