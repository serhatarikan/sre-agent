# Local LLM SRE Agent

An automated, local Site Reliability Engineering (SRE) log monitoring and root-cause analysis tool. It continuously tails application log files in real time, detects critical errors, and uses a locally hosted Large Language Model (Qwen2.5 via Ollama) to generate instant root-cause diagnoses and remediation steps.

---

## Architecture Overview

```text
+-------------------+        Appends Log       +-------------------+
|  chaos_app.py     | -----------------------> |   logs/app.log    |
| (Log Generator)   |                          +-------------------+
+-------------------+                                    |
                                                         | Tails & Watches
                                                         v
                                               +-------------------+
                                               |  log_watcher.py   |
                                               |  (Log Listener)   |
                                               +-------------------+
                                                         |
                                                         | Sends JSON Log
                                                         v
+-------------------+       HTTP POST          +-------------------+
|    Ollama API     | <----------------------- |  llm_analyzer.py  |
|   (qwen2.5:3b)    | -----------------------> |   (LLM Engine)    |
+-------------------+     Analysis Output      +-------------------+
Key Features
Real-time Log Tailing: Continuously monitors log files without blocking system execution.

Error Detection: Filters and isolates critical error logs (ERROR level).

Local & Private AI Analysis: Leverages local LLM inference via Ollama to ensure complete data privacy without reliance on third-party cloud APIs.

Actionable Remediation: Outputs structured diagnostic reports including Root Cause and step-by-step Remediation Steps.

Prerequisites
Python 3.10+

Ollama installed and running locally

Qwen2.5 3B Model pulled via Ollama:

Bash
ollama pull qwen2.5:3b
Quickstart
1. Clone the Repository
Bash
git clone [https://github.com/serhatarikan/sre-agent.git](https://github.com/serhatarikan/sre-agent.git)
cd sre-agent
2. Set Up Virtual Environment & Install Dependencies
Bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
3. Ensure Ollama Service is Active
Check that Ollama is serving requests on http://localhost:11434:

Bash
ollama list
4. Run the Chaos App (Log Producer)
In your first terminal window, start generating mock application errors:

Bash
python3 app/chaos_app.py
5. Run the SRE Agent (Log Watcher)
In a second terminal window, launch the SRE Agent to monitor and analyze incoming errors:

Bash
python3 app/log_watcher.py
Example Output
Plaintext
[*] Starting Log Watcher on logs/app.log...

[ALERT]: Critical ERROR detected!
Message: Request failed: Error 111 connecting to 127.0.0.1:6379. Connection refused.
Details: {'code': 'REDIS_CONNECTION_REFUSED', 'message': 'Connection refused.'}

[SRE AGENT ANALYZING...]

----------------------------------------
**Root Cause:**
The application attempted to establish a TCP connection to Redis on 127.0.0.1:6379, but the target port is actively refusing connections (Error 111).

**Remediation Steps:**
1. Check if the Redis service is running: `systemctl status redis`
2. If inactive, start the service: `sudo systemctl start redis`
3. Verify Redis is listening on port 6379: `netstat -tuln | grep 6379`
----------------------------------------
