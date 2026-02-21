from fastapi import FastAPI
from routes.assessment import router as assessment_router

app = FastAPI(title="PathForge AI")

# register routes
app.include_router(assessment_router)

@app.get("/")
def home():
    return {"message": "Backend running successfully"}
