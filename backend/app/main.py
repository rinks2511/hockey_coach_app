import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routers import auth, config, tactics, teams

app = FastAPI(title="HV Myra Matchday Board Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables on server start
init_db()

# Register API Routers
app.include_router(auth.router)
app.include_router(config.router)
app.include_router(tactics.router)
app.include_router(teams.router)

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))

# Mount public folder for static files
public_dir = os.path.join(FRONTEND_DIR, "public")
if os.path.exists(public_dir):
    app.mount("/public", StaticFiles(directory=public_dir), name="public")

# Serve index.html for UI routes with no-cache headers to guarantee instant updates
@app.get("/{catchall:path}")
def serve_ui(catchall: str):
    if catchall.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(
            index_path,
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
    raise HTTPException(status_code=404, detail="Frontend index.html not found")

