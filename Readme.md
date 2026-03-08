## Create Virtual environment for Python

**Run these commands (PowerShell) for Package installation :**

```powershell
1. cd "C:\RK\repos\Generative & Agentic AI"
2. python -m venv .venv
3. .\.venv\Scripts\Activate    # PowerShell: source the activation script
4. python -m pip install --upgrade pip
5. pip install -r .\requirements.txt
6. pip freeze > .\requirements.txt    [It will generate requirement.txt file for youwith all package and version details in virtual environment]
```

**Run Uvicorn ASGI (Asynchronous Server Gateway Interface) web server for Python :**

```powershell
1. fastapi dev filename.py [server.py]

2. python -m 7-RAG_Queue.main [run FastAPI using Uvicorn]
```

**Run Docker compose file:**

```sh
1. Go to folder in which docker-compose.yml file is present and run below command
2. docker compose up -d [d means detach mode. It will run in background]
```

**Run LangChain:**

```sh
1. pip install -qU langchain-community pypdf [install packages for langchain & PDF reader - for loading files]
2. pip install -qU langchain.text_splitter   [package for chunking pages into small paragraphs]
3. pip install -qU langchain_openai          [Package for Embedding Model]
4. pip install -qU langchain-qdrant          [Package for storing into Qdrant Vector DB]
```

**RQ - Redis Queue for Async:**

```sh
1. pip install rq
```

**Run LangGraph**

```sh
1. pip install -U langgraph
```

**Run Memory MEM0 AND Graph Memory (Neo4j)**

```sh
1. pip install mem0ai
2. pip install longchain_neo4j [Graph Memory]
```

**Run Voice to Text (Speech Recognition) package**

```sh
## For Windows system
1. pip install SpeechRecognition
2. pip install SpeechRecognition[audio]   # This is require to access Microphone through PyAudio package
```
