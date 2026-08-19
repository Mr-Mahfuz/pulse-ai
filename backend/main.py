"""
SmartTriage — AI Emergency Patient Prioritization System
FastAPI Backend Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.database import init_db
from backend.ml_model import TriageClassifier
from backend.llm_explainer import LLMExplainer
from backend.routes import patients, triage, audit, speech


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and ML models on startup."""
    print("🏥 SmartTriage starting up...")
    
    # Initialize database
    init_db()
    print("✅ Database initialized")
    
    # Initialize ML classifier
    classifier = TriageClassifier()
    
    # Initialize LLM explainer
    explainer = LLMExplainer()
    
    # Inject dependencies into triage routes
    triage.set_dependencies(classifier, explainer)
    
    print("🚀 SmartTriage backend ready!")
    yield
    print("👋 SmartTriage shutting down...")


app = FastAPI(
    title="SmartTriage API",
    description="AI-Powered Emergency Patient Prioritization System",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow Nuxt frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(patients.router)
app.include_router(triage.router)
app.include_router(audit.router)
app.include_router(speech.router)


@app.get("/")
async def root():
    return {"message": "SmartTriage API is running", "version": "1.0.0"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
