from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
#duckdduckgo search
search=DuckDuckGoSearchRun()
 
search_tool=Tool(
    name="web_search",
    func=search.run,
    description="search the web for info"
)

#wikipedia search 

wiki = WikipediaQueryRun(
    api_wrapper = WikipediaAPIWrapper()
)
wiki_tool = Tool(
    name="wiki_search",
    func=wiki.run,
    description="Search Wikipedia for information."
)