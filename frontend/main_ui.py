

import httpx, asyncio
import uuid
from nicegui import ui


## logged in user details
userId = None

# Create a main page container
main_container = None



# showing login page
def show_login_page(container):
    container.clear()
    with container:
        with ui.row().classes("w-full h-screen flex-1 items-center justify-center"):
            with ui.column().classes("items-center justify-center gap-4 p-6 border rounded shadow-lg"):
                ui.label("Login to Document QA ChatBot System").classes("text-2xl font-bold mb-4")
                username_input = ui.input("Username").classes("w-64 mb-2")
                password_input = ui.input("Password", password=True, password_toggle_button=True).classes("w-64 mb-2")
                status_label = ui.label("").classes("text-red-500")
                async def on_login_click():
                    global userId
                    async with httpx.AsyncClient() as client:
                        try:
                            url = 'http://127.0.0.1:8000/api/v1/login/authenticate_login_user/'
                            resp = await client.post(url, json={
                                "username": username_input.value,
                                "password": password_input.value
                            })
                            loginRspDataObj = resp.json()
                            if loginRspDataObj['status_code'] == 200:
                                userId = loginRspDataObj['data']["userId"]
                                ui.notify("Login successful!", type="positive", position="top")
                                show_dashboard_page(container)
                            else:
                                status_label.set_text(loginRspDataObj['messages'][0])
                        except Exception as e:
                            status_label.set_text(f"Error: {str(e)}")
                ui.button("Login", on_click=on_login_click).classes("w-64 bg-blue-500 text-white")
                ui.html("""
                    <p>Use Below Given Anyone Login Demo Credentials:</p>
                    <ul class="text-sm text-gray-500 mt-2 list-disc pl-5">
                        <li>Username: admin1 | Password: admin1</li>
                        <li>Username: admin2 | Password: admin2</li>
                        <li>Username: admin3 | Password: admin3</li>
                    </ul>
                """).classes("text-sm text-gray-500 mt-2")



# showing dashboard page
def show_dashboard_page(container):
    import uuid
    from components.chat_box import ChatBox
    from components.upload_box import UploadBox
    from components.status_box import StatusBox
    container.clear()
    with container:

        # Row 1: Welcome + Logout
        with ui.row().classes("w-full justify-between items-center mb-4"):
            ui.label(f"Welcome User-ID: {userId} into the Document QA ChatBot System").classes("text-2xl font-bold")

            def logout():
                global userId
                userId = None
                ui.notify("Logged out", type="info", position="top")
                show_login_page(container)

            ui.button("Logout", on_click=logout).classes("bg-red-500 text-white")

        # Row 2: Chat Control Buttons
        with ui.row().classes("w-full justify-center gap-6 mb-6"):

            # Placeholder containers for Upload & ChatBox
            chat_area_container = ui.column()
            upload_area_container = ui.column()
            
            # New Chat Session Button
            def new_chat_session():

                # Clear previous UI if any
                chat_area_container.clear()
                upload_area_container.clear()

                userSessionId = str(uuid.uuid4())
                status_box = StatusBox()
                chat_box = ChatBox(str(userId), str(userSessionId))
                upload_box = UploadBox(str(userId), str(userSessionId), status_box=status_box, chat_box=chat_box)
                
                # Row 3: Left Upload | Right Chatbox
                with ui.row().classes("w-full justify-center gap-8"):
                    with upload_area_container:
                        upload_box.render()
                        status_box.render()

                    with chat_area_container:
                        chat_box.render()

                ui.notify(
                    f"New Chat Session Started (Session-ID: {userSessionId})",
                    type="info", position="top"
                )

            ui.button("New Chat Session", on_click=new_chat_session).classes("w-56 bg-blue-500 text-white")

            # Chat All Session History Button
            def show_chat_all_session_history():
                ui.notify("Show Chat Session History Work is Pending!", type="info", position="top")
                
            ui.button("All Chat Session History", on_click=show_chat_all_session_history).classes("w-56 bg-gray-1000 text-white")




# showing main page
@ui.page("/")
def main_page():
    global main_container
    main_container = ui.column()
    show_login_page(main_container)


# Run the NiceGUI app
ui.run(title='Document-QA-ChatBot-System')


