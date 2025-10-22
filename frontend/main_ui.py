
from nicegui import ui
from components.chat_box import ChatBox
from components.upload_box import UploadBox
from components.status_box import StatusBox
import asyncio

## user details after login simmulation
userId = 11
userSessionId = "111"

# initialize shared components
status_box = StatusBox()  # Handles async status updates
chat_box = ChatBox(str(userId), str(userSessionId))  # Handles chat messages & streaming tokens
upload_box = UploadBox(str(userId), str(userSessionId), status_box=status_box, chat_box=chat_box)  # Handles PDF upload


# Arrange UI Layout
with ui.row():  # Horizontal row layout

    with ui.column():  # Left column: Upload + Status
        upload_box.render()  # Render the upload box
        status_box.render()  # Render status area below upload
        
    with ui.column(): # Right column: Chat area
        chat_box.render() # Render chat messages area


# Run the NiceGUI app
ui.run(title='DocumentQAChatBot')


