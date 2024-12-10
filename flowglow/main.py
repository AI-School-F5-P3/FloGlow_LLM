from app.interface.gradio_app import launch_app
from dotenv import load_dotenv
from app.core.config import settings

def main():
    load_dotenv()
    print(f"OLLAMA_HOST: {settings.OLLAMA_HOST}") 
    launch_app()

if __name__ == "__main__":
    main()