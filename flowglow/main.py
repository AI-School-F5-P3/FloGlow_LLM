# flowglow/main.py
import subprocess
import time
import sys
import os
from app.interface.gradio_app import launch_app
import atexit

def is_ollama_running():
    """Check if Ollama service is running"""
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 11434))
        sock.close()
        return result == 0
    except:
        return False

def start_ollama():
    """Start Ollama service"""
    try:
        print("Starting Ollama service...")
        # Start Ollama as a background process
        process = subprocess.Popen(
            ['ollama', 'serve'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for service to start
        time.sleep(2)
        return process
    except Exception as e:
        print(f"Error starting Ollama: {e}")
        return None

def stop_ollama(process):
    """Stop Ollama service"""
    if process:
        process.terminate()
        process.wait()
        print("\nOllama service stopped")

def main():
    # Check if Ollama is already running
    ollama_process = None
    if not is_ollama_running():
        ollama_process = start_ollama()
        if not ollama_process:
            print("Failed to start Ollama service. Please start it manually with 'ollama serve'")
            sys.exit(1)
        
        # Wait for Ollama to fully start
        time.sleep(5)
        print("Ollama service started successfully")
    
    # Register cleanup function
    if ollama_process:
        atexit.register(lambda: stop_ollama(ollama_process))
    
    # Launch the Gradio app
    try:
        launch_app()
    except KeyboardInterrupt:
        if ollama_process:
            stop_ollama(ollama_process)
        sys.exit(0)

if __name__ == "__main__":
    main()