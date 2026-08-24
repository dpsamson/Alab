import pyttsx3

def text_to_speech(text: str, output_path:str = "response.wav"):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    return output_path