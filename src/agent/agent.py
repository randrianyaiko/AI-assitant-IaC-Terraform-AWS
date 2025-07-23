from src.llm.model import llm
from langgraph.prebuilt import create_react_agent
from src.image_to_text.diagram_to_code import getDescription
from src.agent.tools import search

def create_agent():
    agent = create_react_agent(model=llm,
                               prompt=  """ 
                                        Act as you are an AWS Cloud Engineer with expertise in Terraform. 
                                        Find the answer by searching to the documentation. Always use the search tool. Do not answer me appart from using the search tool.
                                        
                                        """,
                               tools = [search]
                               )
    
    return agent

def get_code(image_path, text):
    agent = create_agent()
    description = getDescription(image_path, text)
    description = description + '\n' +"For each components, search for them in the documentation. Use a very detailed query to get better results. After finding results, keep them and start writing the Terraform code."
    code = agent.invoke({"messages": [{"role": "user", "content": description}]})
    return {'code':code['messages'][-1].content}
