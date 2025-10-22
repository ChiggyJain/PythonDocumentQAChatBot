
import httpx
import asyncio
from nicegui import ui


class ChatBox:


    def __init__(self, userId:str, userSessionId:str):
        """Initialize chat storage and UI references."""
        self.userId = userId
        self.userSessionId = userSessionId
        self.chat_messages = []   # List of tuples: (sender, message)
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



    def add_user_message(self, message: str):
        """Add a user message to the chat."""
        self.chat_messages.append(('user', message))
        with self.container:
            ui.label(f'You: {message}').classes('text-green-700 font-semibold')
        self._scroll_to_bottom()
        

    def add_ai_message_chunk(self, token: str):
        """Add streaming AI message chunks (token by token)."""
        # print(f"self.chat_messages: {self.chat_messages}\n")
        # First AI message
        if not self.chat_messages or self.chat_messages[-1][0].lower() != 'ai':
            self.chat_messages.append(('ai', token))
            with self.container:
                self.last_ai_label = ui.label(f'AI: {token}').classes('text-blue-600 font-semibold')
        else:
            # Append to last AI message with proper spacing
            last_text = self.chat_messages[-1][1]
            # Add a space if last char is not whitespace and token starts with alphanumeric
            if last_text and not last_text[-1].isspace() and len(token)>0 and token[0].isalnum():
                token = " " + token
            # Update chat message history
            self.chat_messages[-1] = ('ai', last_text + token)
            # Update the UI label dynamically
            if hasattr(self, 'last_ai_label') and self.last_ai_label is not None:
                self.last_ai_label.text = f'AI: {self.chat_messages[-1][1]}'
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
        self.chat_messages = []
        if self.container:
            self.container.clear()


    async def send_prompt_to_backend(self, prompt: str, userId:str,  userSessionId:str):
        """
        Sends prompt to FastAPI backend streaming endpoint
        and updates chat container token by token.
        """
        self.add_user_message(prompt) # show user message
        url = 'http://127.0.0.1:8000/api/v1/chat/ask'
        async with httpx.AsyncClient(timeout=None) as client:
            try:
                # POST request with JSON payload
                async with client.stream("POST", url, json={"prompt": prompt, "userId": userId, "session_id": userSessionId}) as response:
                    if response.status_code != 200:
                        self.add_ai_message_chunk(f"[ERROR] {response.text}")
                        return
                    # Stream tokens from backend
                    async for line in response.aiter_lines():
                        if line.startswith("data:"):
                            token = line.replace("data:", "").strip()
                            self.add_ai_message_chunk(token)
            except Exception as e:
                self.add_ai_message_chunk(f"[ERROR] send_prompt_to_backend backend call failed: {str(e)}")