from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve the api key
API_KEY = os.getenv('API_KEY')