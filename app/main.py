from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import upload, report, rules
from app.core.scheduler import start_scheduler

app = FastAPI(title="Report Generator Microservice", version="1.0.0")

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(upload.router, prefix="/upload", tags=["File Upload"])
app.include_router(report.router, prefix="/report", tags=["Report Generation"])
app.include_router(rules.router, prefix="/rules", tags=["Transformation Rules"])

@app.on_event("startup")
def startup_event():
    start_scheduler()

@app.get("/")
def root():
    return {"message": "Report Generator Microservice is running"}
