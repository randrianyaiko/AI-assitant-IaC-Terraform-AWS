from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()

llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_LLM_MODEL"),
                             api_key=os.getenv("GOOGLE_API_KEY"), 
                             temperature=os.getenv("GOOGLE_LLM_TEMPERATURE")
                             )