from src.llm.model import llm
from src.llm.input_format import format_input
from src.llm.prompts import prompt_get_query, parser
from langgraph.prebuilt import create_react_agent
import time


def getDescription(image_path, text):
    input = format_input(text=text, image_path=image_path)
    output =llm.invoke([input])
    return output.content

def getQuery(image_path, text):
    start = time.time()
    description = getDescription(image_path, text)
    input = {"description": description}
    chain = prompt_get_query | llm | parser
    output = chain.invoke(input)
    end = time.time()
    print(f"Processing Time: {end - start}seconds")
    return output.dict()['queries']
