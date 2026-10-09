from src.parsers.llm_parser import LLMParser

QUERY = "Winnipeg"
CONTENT = """
Thank you Winnipeg for Nic Ehlers! #SoundTheSiren
"""

response = LLMParser(QUERY, CONTENT)
print(response)