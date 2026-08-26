import requests

# Ollama local API configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"

def analyze_log(log_data: dict) -> str:
    """Sends log error details to local LLM via Ollama API for SRE analysis.

    Args:
        log_data (dict): Dictionary containing parsed JSON log fields
                        
    Returns:
        str: Generated root cause analysis and remediation steps from the model.
    """

    # Construct structured prompt targeting SRE root cause analysis
    prompt = f"""
    You are an expert SRE. Analyze this error:
    Message: {log_data.get('message')}
    Details: {log_data.get('error_details')}
    Provide Root Cause and Remediation Steps concise.
    """
    # Prepare payload for Ollama REST API
    payload = {
        "model": MODEL_NAME, 
        "prompt": prompt, 
        "stream": False,
        #performance tweak for local LLM
        "options": {
        "num_predict": 120 
        },
        }

    try:
        # Dispatch POST request with 120s timeout
        response = requests.post(OLLAMA_URL, json = payload, timeout=120)
        response.raise_for_status()

        # Extract LLM output
        return response.json().get("response", "No response text generated.") 

    except requests.RequestException as err:
        # Catch specific API/Network connection errors
        print(f"[ALERT]: AI analysis failed! Details: {err}")
        return "Unable to generate AI analysis."

