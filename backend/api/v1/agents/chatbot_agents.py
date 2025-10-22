
import threading
from agno.memory import MemoryManager
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

    _lock = threading.Lock()
    _instance = None
    _agents = {}
    
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance


    def get_or_create_agent(self, userId:str, userSessionId:str):
        if userId not in self._agents:
            self._agents[userId] = {}
        if userSessionId not in self._agents[userId]:
            self._agents[userId][userSessionId] = {"agents" : "", "messages": [], "all_pdf_text" : [], "overall_pdf_text" : ""}
            self._agents[userId][userSessionId]['agents'] = Agent(
                model=OpenAIChat(),
                name=f"Agent-{userId}-{userSessionId}",
                user_id=str(userId),
                session_id=str(userSessionId),
                cache_session=True,
                search_session_history=True
            )
        return self._agents[userId][userSessionId]



    async def get_response(self, prompt:str, userId:str, userSessionId:str) -> AsyncGenerator[str, None]:
        """
        Stream AI response token by token.
        """
        # getting agno-agent instances
        agentInstancesDict = self.get_or_create_agent(userId, userSessionId)
        curAgent = agentInstancesDict['agents']
        # Append user prompt to history
        agentInstancesDict['messages'].append(f"User: {prompt}")
        if agentInstancesDict['overall_pdf_text']!="":
            prompt = f"Answer based on this document:\n{agentInstancesDict['overall_pdf_text']}\n\nQuestion: {prompt}"
        # Send prompt to Agno agent (async streaming)
        # Agno returns async generator of tokens
        try:
            # async for token in curAgent.stream(prompt):
            async for response_token in curAgent.arun(input=prompt, stream=True):    
                # Yield token to the caller (FastAPI StreamingResponse)
                # print(f"response_token.content: {response_token.content}\n")
                yield response_token.content
                # Also append to session for chat history
                if agentInstancesDict['messages']:
                    last_msg = agentInstancesDict['messages'][-1]
                    if last_msg.startswith("AI:"):
                        agentInstancesDict['messages'][-1]+= response_token.content
                    else:
                        agentInstancesDict['messages'].append(f"AI:{response_token.content}")
        except Exception as e:
            yield f"[ERROR] get_response Agent failed: {str(e)}"


    def get_history(self, userId:str, userSessionId:str) -> list[str]:
        
        """
        Return full chat history for a session.
        """

        pass

    def reset_session(self, userId:str, userSessionId:str):

        """
        Clear session history.
        """

        pass
        