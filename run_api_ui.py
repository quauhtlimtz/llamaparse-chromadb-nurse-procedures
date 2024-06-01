import subprocess
import os

# Paths to your FastAPI and Streamlit apps
fastapi_app = "run"
streamlit_app = "ui/chat_ui.py"

def run_fastapi():
    return subprocess.Popen(["fastapi", fastapi_app, "--host", "0.0.0.0", "--port", "8000"])

def run_streamlit():
    return subprocess.Popen(["streamlit", "run", streamlit_app])

if __name__ == "__main__":
    # Start FastAPI and Streamlit in separate processes
    p1 = run_fastapi()
    p2 = run_streamlit()
    
    # Wait for both processes to complete
    p1.wait()
    p2.wait()