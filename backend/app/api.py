from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from .service import get_resume_recommendations, generate_highlight_improvment
from .schemas import CreateImprovementRequest


todos = [
    {
        "id": "1",
        "item": "Read a book."
    },
    {
        "id": "2",
        "item": "Cycle around town."
    }
]


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)

@app.post("/resume/highlights", tags=["resume"])
async def add_and_get_resume_highlights(resume: UploadFile) -> dict:
    return get_resume_recommendations(resume)

@app.post("/resume/improvement", tags=["highlight"])
async def get_resume_highlight_improvement(highlight_details: CreateImprovementRequest) -> dict:
    return generate_highlight_improvment(highlight_details.highlight)

