
from nicegui import ui

class ChatBox:

    def __init__(self):
        """Initialize chat storage and UI references."""
        self.chat_messages = []   # List of tuples: (sender, message)
        self.container = None   # Main chat container (ui.column)
        self.last_ai_label = None  # Keep track of the last AI label for streaming updates

    def render(self):
        """Render the main chat container."""
        self.container = ui.column() \
            .style('overflow-y: auto; height: 500px; width: 600px; border: 1px solid gray; padding: 10px;')

    def add_user_message(self, message: str):
        """Add a user message to the chat."""
        self.chat_messages.append(('user', message))
        with self.container:
            ui.label(f'You: {message}').classes('text-green-700 font-semibold')

    def add_ai_message_chunk(self, token: str):
        """Add streaming AI message chunks (token by token)."""
        if not self.chat_messages or (self.chat_messages[-1][0]).lower() != 'ai':
            # Start a new AI message
            self.chat_messages.append(('ai', token))
            with self.container:
                self.last_ai_label = ui.label(f'AI: {token}').classes('text-blue-600 font-semibold')
        else:
            # Append to the last AI message dynamically
            prev_text = self.chat_messages[-1][1] + token
            self.chat_messages[-1] = ('ai', prev_text)
            if self.last_ai_label:
                self.last_ai_label.text = f'AI: {prev_text}'

    def clear_chat(self):
        """Clear all chat messages and reset the UI."""
        self.chat_messages = []
        if self.container:
            self.container.clear()
