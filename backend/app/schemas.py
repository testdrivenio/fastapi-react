from pydantic import BaseModel, Field

class CreateImprovementRequest(BaseModel):
    highlight: str