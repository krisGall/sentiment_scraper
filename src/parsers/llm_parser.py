import ollama
from utils.terminal_utils import get_current_time


class LLMParser:
    """
    LLM Parser validates the context of the response relates the query using the system prompt given.
    Arguments:
        query - query for bluesky api
        content - content response from bluesky api
    Returns:
        boolean value showing if context is valid
    """

    def __new__(cls, query, content):

        # Asking LLM for context parsing
        prompt = f"""
        You are a Canadian city checker who checks text to see if it belongs to a Canadian city. You are given the following text:
        {content}
        and you will check it to see if you can tell if its referring to the Canadian city of the same name: {query}.

        Your response will be either: True, False or None. You will choose True if it refers to the Canadian city. You will chose
        False if it does not. You will choose None if you cannot tell. You will only return these 3 values in the form of a string.
        The response will have no punctuation.

        Your response will contain no other information.
        """
        response = ollama.chat(
            model= 'llama3.2',
            messages= [
                {
                    'role': 'user',
                    'content': prompt
                },
            ]
        )

        # Mapping response to boolean
        bool_map = {
            "False": 0, 
            "True": 1, 
            "None": None
            }

        # Catching Malformed LLM Responses
        try:
            mapped_response = bool_map[response['message']['content']]
            return mapped_response
        except KeyError:
            print(f"[{get_current_time()}] WARNING: Invalid LLM Response! ({response['message']['content']})")
            return None

        