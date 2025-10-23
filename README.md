
# DocumentQAChatBot

**DocumentQAChatBot** is a web-based Question-Answering chatbot system built using **Python 3.12**, **FastAPI** backend, **NiceGUI** frontend, and **Agno >=1.5.0** for AI agent integration. The system allows users to have normal chat conversations with an AI model and also perform PDF-based Q&A by uploading PDF documents. All chat sessions are handled in memory per user session; no persistent storage is used.

---

## **Project Features**

### Frontend
- Built on **NiceGUI 2.18.0**.
- **Login Page:** Simulated demo login credentials for authentication.
- **Dashboard Page:**
  - **New Chat Session Button:** Generates a unique session ID for each user. Shows:
    - Chat Box
    - PDF Upload Box
    - Status Box
  - **Show All Chat Session History:** Placeholder implementation ("can be done later").
- **PDF Upload:** Upload PDF files (max 5MB, non-empty, PDF-only) to enable Q&A based on document content.
- **Chat Box:** Allows normal or document-based conversation.
- **Status Box:** Shows system and upload statuses.

### Backend
- Built on **FastAPI** and **Python 3.12**.
- **APIs:**
  1. `/api/v1/login/authenticate_user_login` → Authenticate demo users, return USER-ID.
  2. `/api/v1/chat/ask` → End-user asks a question; returns streaming response token-by-token from Agno agent.
  3. `/api/v1/pdf/upload_pdf` → Handles PDF file upload, parsing, and adds parsed content to the user session for Q&A.
  4. `/api/v1/chat/chat_session_history` → Returns chat history for a given USER-ID + SESSION-ID.
  5. `/api/v1/chat/reset_chat_session_history` → Resets chat session history for a user session.
- **Agno Agent:** Handles AI chat with session and in-memory history.
- **PDF Parsing:** Uses PyMuPDF (`fitz`) to extract text content per page.

---

## **Project Structure**

PythonDocumentQAChatBot/
│
├── backend/
│ ├── api/
│ │ ├── v1/
│ │ │ ├── routes/ # system_health, login, chat, pdf APIs
│ │ │ ├── schemas/ # login, chat, pdf schemas
│ │ │ ├── services/ # pdf_parser_service.py
│ │ │ └── agents/ # chatbot_agents.py (Agno integration)
│ └── utils/ # helper functions
│
├── frontend/
│ ├── main_ui.py # main NiceGUI frontend
│ └── components/ # chat_box, upload_box, status_box
│
├── data/ # uploaded PDFs
├── tests/ # unit & integration tests
├── main.py # FastAPI entry point
├── requirements.txt # Python dependencies
├── Dockerfile_backend_production_machine
├── Dockerfile_frontent_production_machine
├── docker-compose_production_machine.yaml
└── .env.example # Environment sample variables



---

## **Setup Instructions**

### Prerequisites
- Python 3.12
- Docker & Docker Compose (for containerized setup)

Steps to Follows to execute project into the local machine
1. make this [PythonProject] directory from terminal
2. Goto this directory [PythonProject] from terminal
3. Execute this command: git clone https://github.com/ChiggyJain/PythonDocumentQAChatBot.git
4. Goto this directory [PythonDocumentQAChatBot] from terminal
5. Copy the [].env.example] file content into [.env] file and also replace OPENI_API_KEY value.
5. Execute this command from terminal one-by-one:
   a. docker compose -f docker-compose_production_machine.yaml down -v
   b. docker compose -f docker-compose_production_machine.yaml build --no-cache
   c. docker compose -f docker-compose_production_machine.yaml up
6. This url [http://0.0.0.0:8000/docs] is for accessing backend-system APIs documentation and hitting the various apis request.
7. Open this url [http://localhost:8080] in any browser for accessing the frontend-system.
8. Follows these steps to execute test-cases of backend-system docker container services:
    a. Execute this command from your terminal: docker container ps -a
    b. Copy the container-id from the terminal whose name is: documentqa_backend_container
    c. Execute this command from the terminal: 
        i. docker exec -it Put-Here-Docker-Container-Services-ID bash
    d. Exeucte this command for unit testing:
       i. PYTHONPATH=$(pwd) pytest tests/unit --disable-warnings -v -s --maxfail=0 -W ignore::DeprecationWarning
    e. Exeucte this command for integration testing:
       i. PYTHONPATH=$(pwd) pytest tests/integration --disable-warnings -v -s --maxfail=0 -W ignore::DeprecationWarning   

