from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from typing import List



class Queries(BaseModel):
    queries: List[str] = Field(description="List of queries to look for in the documentation.")


parser = PydanticOutputParser(pydantic_object=Queries)

prompt_get_query = PromptTemplate.from_template(
                                                template = """ With the following description of the AWS Services and how it will interract with each other and how they will be used, 
                                                  Description : {description}
                                                  What we should look for inside of the terraform documentations?
                                                  Which services should have access in between each other? 
                                                  Do we need IAM role? Do we need IAM Policy? Do we need resoure policy?
                                                  What are the security best practices?

                                                  Answer all of these questions to queries that makes search on Terraform documentation easily.
                                                  Format your answer in the following format:
                                                  {format_instructions}

                                                  Answer me only with the above format. Do not add any additional text.
                                                  """ ,
                                                partial_variables={"format_instructions": parser.get_format_instructions()}
                                                )

prompt_generate_terraform_code = PromptTemplate.from_template(
                                                template = """
                                                This is the description of the architecture on AWS:
                                                    {description}
                                                
                                                These are the results found from the terraform documentation.
                                                {results}
                                                
                                                Now I want you to generate terraform code from this result found from the documentation.
                                                
                                                
                                                """ 
                                                )
