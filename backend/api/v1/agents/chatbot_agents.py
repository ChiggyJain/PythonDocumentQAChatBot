
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from typing import AsyncGenerator
from dotenv import load_dotenv
load_dotenv()
import os


class ChatBotAgent:

    """
    ChatBotAgent wraps Agno's OpenAI integration with session/history support.
    """

    # Initialize OpenAI model via Agno
    def __init__(self, userId:str=None, userSessionId:str=None):
        self.agent: Agent = Agent(
            model=OpenAIChat(),
            name="Document QA Chatbot System Agent",
            user_id=str(12),
            session_id=str(111)
        )
        # Internal user-wise session memory (dictionary: session_id -> messages)
        self.sessions: dict[str, dict[str, list[str]]] = {}
        print(f"self.agent: {self.agent}\n")


    async def get_response(self, prompt:str, userId:str, userSessionId:str) -> AsyncGenerator[str, None]:

        """
        Stream AI response token by token.
        """

        # Initialize session history if not exists
        if userId not in self.sessions:
            self.sessions[userId] = {}
            self.sessions[userId][userSessionId] = []
        elif userSessionId not in self.sessions[userId]:
            self.sessions[userId][userSessionId] = []

        # Append user prompt to history
        self.sessions[userId][userSessionId].append(f"User: {prompt}")

        # Send prompt to Agno agent (async streaming)
        # Agno returns async generator of tokens
        try:
            # async for token in self.agent.stream(prompt):
            async for response_token in self.agent.arun(input=prompt, stream=True):    
                # Yield token to the caller (FastAPI StreamingResponse)
                # print(f"response_token.content: {response_token.content}\n")
                yield response_token.content
                # Also append to session for chat history
                if self.sessions[userId][userSessionId]:
                    last_msg = self.sessions[userId][userSessionId][-1]
                    if last_msg.startswith("AI:"):
                        self.sessions[userId][userSessionId][-1]+= response_token.content
                    else:
                        self.sessions[userId][userSessionId].append(f"AI:{response_token.content}")
        except Exception as e:
            yield f"[ERROR] get_response Agent failed: {str(e)}"


    def get_history(self, userId:str, userSessionId:str) -> list[str]:
        
        """
        Return full chat history for a session.
        """

        if userId not in self.sessions:
            return []
        elif userSessionId not in self.sessions[userId]:
            return []
        else:
            return self.sessions[userId][userSessionId]


    def reset_session(self, userId:str, userSessionId:str):

        """
        Clear session history.
        """

        if userId in self.sessions:
            if userSessionId in self.sessions[userId]:
                self.sessions[userId][userSessionId] = []

        