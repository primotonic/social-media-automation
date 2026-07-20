from dotenv import load_dotenv
import os

load_dotenv()

FB_USER_TOKEN = os.getenv("FB_USER_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")