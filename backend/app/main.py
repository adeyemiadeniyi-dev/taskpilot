from app.api.v1.routes import goals, tasks, planning, agent, automation
from app.database import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

app = FastAPI(
    title="TaskPilot Backend",
    version="0.1.0",
    description="Backend API for TaskPilot - AI-powered task planning and workflow automation.",
)



origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
     "https://taskpilot-frontend.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def verify_db_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise


@app.get("/")
def read_root():
    return {"message": "Welcome to TaskPilot API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}



app.include_router(goals.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(planning.router, prefix="/api/v1")
app.include_router(automation.router, prefix="/api/v1")
app.include_router(agent.router, prefix="/api/v1")

