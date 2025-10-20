
from agno.agent import Agent
from agno.models.openai import OpenAI
from typing import AsyncGenerator
from dotenv import load_dotenv
load_dotenv()
import os


class ChatBotAgent:

    """
    ChatBotAgent wraps Agno's OpenAI integration with session/history support.
    """

    # Initialize OpenAI model via Agno
    def __init__(self):
        self.agent: Agent = Agent(
            model=OpenAI(),
            verbose=False
        )
        # Internal session memory (dictionary: session_id -> messages)
        self.sessions: dict[str, list[str]] = {}


    async def get_response(self, prompt: str, session_id: str | None = None) -> AsyncGenerator[str, None]:

        """
        Stream AI response token by token.
        If session_id is provided, maintains conversation history.
        """

        # Assign default session if none provided
        if not session_id:
            session_id = "default_session"

        # Initialize session history if not exists
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        # Append user prompt to history
        self.sessions[session_id].append(f"User: {prompt}")

        # Send prompt to Agno agent (async streaming)
        # Agno returns async generator of tokens
        try:
            async for token in self.agent.stream(prompt):
                # Yield token to the caller (FastAPI StreamingResponse)
                yield token
                # Also append to session for chat history
                if self.sessions[session_id]:
                    last_msg = self.sessions[session_id][-1]
                    if last_msg.startswith("AI:"):
                        self.sessions[session_id][-1] += token
                    else:
                        self.sessions[session_id].append(f"AI:{token}")
        except Exception as e:
            yield f"[ERROR] Agent failed: {str(e)}"


    def get_history(self, session_id: str) -> list[str]:
        
        """
        Return full chat history for a session.
        """

        if session_id not in self.sessions:
            return []
        return self.sessions[session_id]


    def reset_session(self, session_id: str):

        """
        Clear session history.
        """

        if session_id in self.sessions:
            self.sessions[session_id] = []
