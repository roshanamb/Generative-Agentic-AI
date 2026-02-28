
from dotenv import load_dotenv
import uvicorn

# Support running as a package (relative import) or as a script (direct run).
try:
    from .server import app
except Exception:
    from server import app

load_dotenv()

def main():
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()