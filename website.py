import os
import subprocess
import time
import webbrowser

def launch_streamlit_app():
    # Start the Streamlit app as a subprocess
    streamlit_process = subprocess.Popen(
        ["streamlit", "run", "streamlit_app.py", "--server.headless=true"]
    )

    # Wait for the server to start
    time.sleep(2)  # Adjust the delay if needed

    # Open the default web browser to the Streamlit app's URL
    webbrowser.open("http://localhost:8501")

    # Wait for the Streamlit process to finish
    streamlit_process.wait()

if __name__ == "__main__":
    launch_streamlit_app()