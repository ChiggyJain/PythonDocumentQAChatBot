
import httpx, asyncio
from nicegui import ui

## logged in user details
userAccessToken = None
userId = None
userSessionId = None

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
                    global access_token, userId, userSessionId
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
                                userSessionId = loginRspDataObj['data']["userId"]
                                ui.notify("Login successful!", type="positive")
                                show_dashboard_page(container)
                            else:
                                status_label.set_text(loginRspDataObj['messages'][0])
                        except Exception as e:
                            status_label.set_text(f"Error: {str(e)}")
                ui.button("Login", on_click=on_login_click).classes("w-64 bg-blue-500 text-white")
                ui.label("Demo Credentials: Username: admin1 & Password: admin1").classes("text-sm text-gray-500 mt-2")




def show_dashboard_page(container):
    from components.chat_box import ChatBox
    from components.upload_box import UploadBox
    from components.status_box import StatusBox

    container.clear()
    with container:
        # Top row: Welcome + Logout
        with ui.row().classes("w-full justify-between items-center mb-4"):
            ui.label(f"Welcome User-ID: {userId} into the Document QA ChatBot System").classes("text-2xl font-bold")
            
            def logout():
                global access_token, userId, userSessionId
                access_token = None
                userId = None
                userSessionId = None
                ui.notify("Logged out", type="info")
                show_login_page(container)
            
            ui.button("Logout", on_click=logout).classes("bg-red-500 text-white")

        # Main content row
        with ui.row().classes("w-full gap-6"):
            # Left Column: Upload + Chat session controls
            with ui.column().classes("gap-4"):
                status_box = StatusBox()
                chat_box = ChatBox(str(userId), str(userSessionId))
                upload_box = UploadBox(str(userId), str(userSessionId), status_box=status_box, chat_box=chat_box)
                upload_box.render()
                status_box.render()
                
                # New Chat Session button
                def new_chat_session():
                    # Clear chat container and re-initialize ChatBox
                    chat_box.container.clear()
                    chat_box.chat_messages.clear()
                    ui.notify("New chat session started!", type="info")
                
                ui.button("New Chat Session", on_click=new_chat_session).classes("w-48 bg-blue-500 text-white")

                # Chat History button
                def show_chat_history():
                    # Here you can implement showing previous messages in a modal or separate container
                    history = "\n".join([f"{sender}: {msg}" for sender, msg in chat_box.chat_messages])
                    ui.dialog().with_content(ui.label(history)).open()
                
                ui.button("Chat History", on_click=show_chat_history).classes("w-48 bg-gray-500 text-white")

            # Right Column: Chat container + Input box + Send button
            with ui.column().classes("gap-2"):
                chat_box = ChatBox(str(userId), str(userSessionId))
                chat_box.render()



# showing main page
@ui.page("/")
def main_page():
    global main_container
    # main_container = ui.column().classes("items-center justify-center min-h-screen gap-4")
    main_container = ui.column()
    show_login_page(main_container)


# Run the NiceGUI app
ui.run(title='DocumentQAChatBot')


