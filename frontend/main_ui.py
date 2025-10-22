
import httpx, asyncio
from nicegui import ui

## logged in user details
userAccessToken = None
userId = None
userSessionId = None

# Create a main page container
main_container = ui.column().classes("items-center justify-center min-h-screen gap-4")



# showing login page
def show_login_page():
    main_container.clear()
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
                   ui.notify("Login successful!", type="positive")
                   show_dashboard_page()
                else:
                    status_label.set_text(loginRspDataObj['messages'][0])
            except Exception as e:
                status_label.set_text(f"Error: {str(e)}")

    ui.button("Login", on_click=on_login_click).classes("w-64 bg-blue-500 text-white")
    ui.label("Demo Credentials: Username: admin1 & Password: admin1").classes("text-sm text-gray-500 mt-2")



def show_dashboard_page():
    from components.chat_box import ChatBox
    from components.upload_box import UploadBox
    from components.status_box import StatusBox
    main_container.clear()
    ui.label("Document QA ChatBot").classes("text-2xl font-bold mb-4")
    status_box = StatusBox()
    chat_box = ChatBox(str(userId), str(userSessionId))
    upload_box = UploadBox(str(userId), str(userSessionId), status_box=status_box, chat_box=chat_box)
    with ui.row():
        with ui.column():
            upload_box.render()
            status_box.render()
        with ui.column():
            chat_box.render()
    def logout():
        global access_token, userId, userSessionId
        access_token = None
        userId =  None
        userSessionId = None
        ui.notify("Logged out", type="info")
        show_login_page()
    ui.button("Logout", on_click=logout).classes("mt-6 bg-red-500 text-white")



# showing main page
@ui.page("/")
def main_page():
    if userId:
        pass
    else:
        show_login_page()


# Run the NiceGUI app
ui.run(title='DocumentQAChatBot')


