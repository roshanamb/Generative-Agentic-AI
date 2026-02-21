## Create Virtual environment for Python

**Run these commands (PowerShell) for Package installation :**

```powershell
1. cd "C:\RK\repos\Generative & Agentic AI"
2. python -m venv .venv
3. .\.venv\Scripts\Activate    # PowerShell: source the activation script
4. python -m pip install --upgrade pip
5. pip freeze > .\requirements.txt    [It will create requirement.txt file for you]
5. pip install -r .\requirements.txt
```

**Run Uvicorn ASGI (Asynchronous Server Gateway Interface) web server for Python :**

```powershell
1. fastapi dev filename.py [server.py]
```
