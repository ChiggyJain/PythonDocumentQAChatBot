
from dotenv import load_dotenv
import os
load_dotenv()
import httpx
import asyncio
import json
from nicegui import ui



class ChatBox:


    def __init__(self, userId:str, userSessionId:str):
        """Initialize chat storage and UI references."""
        self.userId = userId
        self.userSessionId = userSessionId
        self.user_session_chat_messages = {}
        self.container = None   # Main chat container (ui.column)
        self.last_ai_label = None  # Keep track of the last AI label for streaming updates
        self.input_box = None
        self.send_button = None  # reference to the send button


    def render(self):
        """Render the main chat container."""
        with ui.column():
            # message area
            self.container = ui.column() \
                .style(
                    'overflow-y: auto; height: 500px; width: 600px; border: 1px solid gray; padding: 10px;'
                ).props('ref="chat_container"')
            # input and send area
            with ui.row().style('width: 600px;'):
                self.input_box = ui.input(placeholder='Type your question...').style('flex-grow: 1')
                self.send_button = ui.button("Send", on_click=self.on_send_click).style('height:42px!important; margin-top:14px!important;')



    async def on_send_click(self):
        """Triggered when Send is clicked"""
        message = self.input_box.value.strip()
        if not message:
            return
        self.input_box.value = ""
        self.add_user_message(self.userId, self.userSessionId, message)
        await self.send_prompt_to_backend(message, self.userId, self.userSessionId)
        


    def disable_input(self):
        """Disable user input & send button."""
        if self.input_box:
            self.input_box.disable()
        if self.send_button:
            self.send_button.disable()


    def enable_input(self):
        """Re-enable user input & send button."""
        if self.input_box:
            self.input_box.enable()
        if self.send_button:
            self.send_button.enable()



    def add_user_message(self, userId:str, userSessionId:str, message:str):
        """Add a user message to the chatbox container."""
        if userId not in self.user_session_chat_messages:
           self.user_session_chat_messages[userId] = {}
        if userSessionId not in self.user_session_chat_messages[userId]:
           self.user_session_chat_messages[userId][userSessionId] = []
        self.user_session_chat_messages[userId][userSessionId].append(('You', message))
        with self.container:
            ui.label(f'You: {message}').classes('text-green-700 font-semibold')
        self._scroll_to_bottom()
        

    def add_ai_message_chunk(self, userId: str, userSessionId: str, token: str):
        """Add streaming AI message chunks (token by token)."""
        # print(f"self.user_session_chat_messages: {self.user_session_chat_messages}\n")
        # First AI message
        if not self.user_session_chat_messages[userId][userSessionId] or self.user_session_chat_messages[userId][userSessionId][-1][0].lower()!='ai':
            self.user_session_chat_messages[userId][userSessionId].append(('AI', token))
            with self.container:
                self.last_ai_label = ui.label(f'AI: {token}').classes('text-blue-600 font-semibold')
        else:
            # Append to last AI message with proper spacing
            last_text = self.user_session_chat_messages[userId][userSessionId][-1][1]
            # Add a space if last char is not whitespace and token starts with alphanumeric
            if last_text and not last_text[-1].isspace() and len(token)>0 and token[0].isalnum():
                token = " " + token
            # Update chat message history
            self.user_session_chat_messages[userId][userSessionId][-1] = ('AI', last_text + token)
            # Update the UI label dynamically
            if hasattr(self, 'last_ai_label') and self.last_ai_label is not None:
                self.last_ai_label.text = f'AI: {self.user_session_chat_messages[userId][userSessionId][-1][1]}'
        self._scroll_to_bottom()


    def _scroll_to_bottom(self):
        """Scroll the container to the bottom using JS."""
        if self.container:
            with self.container:
                ui.run_javascript('''
                    const el = document.querySelector('[ref="chat_container"]');
                    if (el) { el.scrollTop = el.scrollHeight; }
                ''')


    def clear_chat(self):
        """Clear all chat messages and reset the UI."""
        self.user_session_chat_messages = []
        if self.container:
            self.container.clear()


    async def send_prompt_to_backend(self, prompt:str, userId:str,  userSessionId:str):
        """
        Sends prompt to FastAPI backend streaming endpoint
        and updates chat container token by token.
        """
        async with httpx.AsyncClient(timeout=None) as client:
            try:
                url = 'http://127.0.0.1:8000/api/v1/chat/ask'
                if os.getenv("APP_ENV")!="development":
                   url = 'http://backend:8000/api/v1/chat/ask' 
                async with client.stream("POST", url, json={"prompt": prompt, "userId": userId, "userSessionId":userSessionId}) as response:
                    if response.status_code!=200:
                        self.add_ai_message_chunk(userId, userSessionId, f"\nError occured {response.status_code}:{response.text}\n")
                        return
                    async for line in response.aiter_lines():
                        if not line.startswith("data:"):
                            continue
                        token = line.replace("data:", "").strip()
                        if not token:
                            continue
                        if token == "[STREAM_COMPLETED]":
                            # self.add_ai_message_chunk(userId, userSessionId, "\n[Response Completed]\n")
                            # print(f"self.user_session_chat_messages[userId][userSessionId]: {self.user_session_chat_messages[userId][userSessionId]}\n")
                            break
                        try:
                            rsp = json.loads(token)
                            if isinstance(rsp, dict) and "status_code" in rsp:
                                if rsp["status_code"]!=200:
                                    msg = " | ".join(rsp.get("messages", []))
                                    self.add_ai_message_chunk(userId, userSessionId, f"\n{msg}\n")
                                    break
                        except json.JSONDecodeError:
                            self.add_ai_message_chunk(userId, userSessionId, token)    
            except Exception as e:
                self.add_ai_message_chunk(userId, userSessionId, f"\nsend_prompt_to_backend backend call failed: {str(e)}\n")