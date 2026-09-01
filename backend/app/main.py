import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .database import init_db
from .routers import config, tactics, teams

app = FastAPI(title="HV Myra Matchday Board Backend")

# Initialize database tables on server start
init_db()

# Register API Routers
app.include_router(config.router)
app.include_router(tactics.router)
app.include_router(teams.router)

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))

# Mount public folder for static files
public_dir = os.path.join(FRONTEND_DIR, "public")
if os.path.exists(public_dir):
    app.mount("/public", StaticFiles(directory=public_dir), name="public")

# Serve index.html for UI routes
@app.get("/{catchall:path}")
def serve_ui(catchall: str):
    if catchall.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail="Frontend index.html not found")
