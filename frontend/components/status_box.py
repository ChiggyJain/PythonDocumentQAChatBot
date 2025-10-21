

from nicegui import ui

class StatusBox:

    # constrcutor
    def __init__(self):
        self.container = None
        self.current_status = None

    
    # render status container
    def render(self):
        self.container = ui.label("").style('color: blue; font-weight: bold;')
    
    # update status message
    def set_status(self, stage: str):
        self.current_status = stage
        if self.container:
            self.container.text = stage

    # show error
    def set_error(self, message: str):
        if self.container:
            self.container.style('color: red; font-weight: bold;')
            self.container.text = f"Error: {message}"

    
    # clear status
    def clear_status(self):
        self.current_status = None
        if self.container:
            self.container.text = ""
            self.container.style('color: blue; font-weight: bold;')
