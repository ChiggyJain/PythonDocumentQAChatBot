
from nicegui import ui
from components.chat_box import ChatBox
from components.upload_box import UploadBox
from components.status_box import StatusBox
import asyncio



# initialize shared components
status_box = StatusBox()  # Handles async status updates
chat_box = ChatBox()  # Handles chat messages & streaming tokens
upload_box = UploadBox(status_box=status_box)  # Handles PDF upload


# Arrange UI Layout
with ui.row():  # Horizontal row layout

    with ui.column():  # Left column: Upload + Status
        upload_box.render()  # Render the upload box
        status_box.render()  # Render status area below upload
        # Add input box to send prompt
        prompt_input = ui.input(placeholder="Type your question here...").classes("w-full")
        send_button = ui.button("Send")

    with ui.column(): # Right column: Chat area
        chat_box.render() # Render chat messages area






# Handle Send button click
def on_send_click():
    prompt = prompt_input.value
    sessionId = "ChiragTest123"
    if prompt.strip() != "":
        asyncio.create_task(chat_box.send_prompt_to_backend(prompt, sessionId))
        prompt_input.value = ""  # clear input

send_button.on("click", on_send_click)
prompt_input.on("submit", on_send_click)  # also allow Enter key


# testing purpose only
# chat_box.add_user_message("Hello, Chatbox System")
# chat_box.add_ai_message_chunk("Hi, Chirag How I Can Help You?")
# status_box.set_error("Something went wrong")



# Run the NiceGUI app
ui.run(title='DocumentQAChatBot')


