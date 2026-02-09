from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TriageRequest(BaseModel):
    stress_level: str
    confidence: float
