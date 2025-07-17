import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

resp = model.generate_content("List three themes from a tech earnings call.", generation_config={"temperature": 0})
print(resp.text)
