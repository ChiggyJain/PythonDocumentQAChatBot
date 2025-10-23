
from dotenv import load_dotenv
import os
load_dotenv()
from nicegui import ui
import httpx
import asyncio

class UploadBox:


    # constructor
    def __init__(self, userId, userSessionId, status_box, chat_box):
        self.userId = userId
        self.userSessionId = userSessionId
        self.status_box = status_box
        self.chat_box = chat_box


    # rendering file uploading box
    def render(self):
        """Render the upload box UI."""
        with ui.card().classes('p-4 w-96'):
            ui.label("Upload PDF Document").classes('text-lg font-semibold mb-2')
            self.upload = ui.upload(on_upload=self.on_upload, multiple=False).props('accept=.pdf')
            ui.label("Allowed file type: PDF only").classes('text-sm text-gray-600')


    # handle the file uploading event
    async def on_upload(self, event):
        """Handle PDF upload event."""
        try:
            self.chat_box.disable_input()
            uploaded_file = event
            filename = uploaded_file.name
            file_bytes = uploaded_file.content.read()
            file_size = len(file_bytes)
            file_size_mb = file_size / (1024 * 1024)
            if not filename.lower().endswith(".pdf"):
                self.status_box.set_error("Only PDF files are allowed.")
                return
            if file_size == 0:
                self.status_box.set_error("File is empty! Please upload a valid PDF.")
                return
            if file_size > (5 * 1024 * 1024):
                self.status_box.set_error("File too large! Maximum allowed size is 5 MB.")
                return
            self.status_box.set_status(f"Uploading {filename} ({file_size_mb:.2f} MB).")
            # Send to backend as multipart/form-data
            url = "http://127.0.0.1:8000/api/v1/pdf/upload"
            if os.getenv("APP_ENV")!="development":
                url = 'http://backend:8000/api/v1/pdf/upload'
            async with httpx.AsyncClient(timeout=None) as client:
                files = {'file': (filename, file_bytes, 'application/pdf')}
                response = await client.post(url, files=files, data={"userId":self.userId, "userSessionId":self.userSessionId})
            if response.status_code == 200:
                res = response.json()
                self.status_box.set_status(f"{res['messages'][0]}")
            else:
                res = response.json()
                self.status_box.set_error(f"{res['messages'][0]}")
        except Exception as e:
            self.status_box.set_error(f"Error: {str(e)}")
        finally:
            self.chat_box.enable_input()
