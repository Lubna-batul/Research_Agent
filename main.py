from langchain.agents import create_tool_calling_agent, AgentExecutor
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import search_tool
load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

    

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
parser=PydanticOutputParser(pydantic_object=ResearchResponse)
prompt=ChatPromptTemplate.from_messages(
    [
   (
"system",
"""
You are an expert research assistant.

Use tools when necessary.

If a tool does not return useful information, answer from your own knowledge.

Always return valid JSON.

{format_instructions}
"""
),
        ("placeholder","{chat_history}"),
        ("human","{query}"),
        ("placeholder","{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

def main():
    
    tools=[search_tool]
    agent=create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
    )

    agent_executor=AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
    )
    query=input("What can i help you research? ")
    raw_response=agent_executor.invoke({"query": query})



    try:
        strucuted_response=parser.parse(raw_response["output"])
        print(strucuted_response)
    except Exception as e:
        print("Error parsing response", e, "Raw Response - ", raw_response)

if __name__=="__main__":
    main()