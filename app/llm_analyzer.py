import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"

def analyze_log(log_data: dict) -> str:
    prompt = f"""
    You are an expert SRE. Analyze this error:
    Message: {log_data.get('message')}
    Details: {log_data.get('error_details')}
    Provide Root Cause and Remediation Steps concise.
    """
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False}

    try:
        response = requests.post(OLLAMA_URL, json = payload, timeout=30)
        response.raise_for_status()
        return response.json().get("response", "No response text generated.") 
    except requests.RequestException as err:
        print(f"[ALERT]: AI analysis failed! Details: {err}")
        return "Unable to generate AI analysis."

