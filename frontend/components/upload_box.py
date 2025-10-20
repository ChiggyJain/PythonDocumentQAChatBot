

from nicegui import ui

class UploadBox:

    # constructor
    def __init__(self, status_box):
        self.status_box = status_box
        self.upload_widget = None

    
    # render upload UI
    def render(self):
        self.upload_widget = ui.upload(label='Upload PDF', multiple=False, on_upload=self.on_upload)

    # called when user uploads a file
    def on_upload(self, file):

        # Step 1: Validate file type
        if not file.name.lower().endswith('.pdf'):
            self.status_box.set_error("Only PDF files are allowed.")
            return
        
        # Step 2: Validate file size
        max_size_mb = 5
        file_bytes = file.content.read()
        file_size_mb = len(file_bytes) / (1024 * 1024)
        if file_size_mb / (1024 * 1024) > max_size_mb:
            self.status_box.set_error(f"File too large. Max {max_size_mb} MB.")
            return

        # Step 3: Update status
        self.status_box.set_status("Uploading PDF...")

        # Step 4: Placeholder for sending file to backend
        # You will later integrate FastAPI endpoint call
        self.status_box.set_status("Parsing PDF...")
        
        # After parsing completes, set Done
        self.status_box.set_status("PDF Ready for QA")
