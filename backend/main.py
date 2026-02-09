from fastapi import FastAPI, HTTPException
from schemas import LoginRequest, Token, TriageRequest
from models import fake_users_db
from auth import create_access_token, verify_password

app = FastAPI(title="AI Destekli Rehberlik Triyaj Sistemi")

@app.get("/")
def root():
    return {"status": "Backend çalışıyor"}

@app.post("/login", response_model=Token)
def login(data: LoginRequest):
    user = fake_users_db.get(data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı")

    if not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Hatalı şifre")

    token = create_access_token({
        "sub": user["username"],
        "role": user["role"]
    })

    return {"access_token": token, "token_type": "bearer"}

@app.post("/triage")
def triage(data: TriageRequest):
    return {
        "message": "Ön değerlendirme alındı",
        "stress_level": data.stress_level,
        "confidence": data.confidence
    }
