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
    if data.username in fake_users_db or data.username in fake_access_codes:
        # herhangi bir şifre veya kodu kabul et
        role = "counselor" if data.username in fake_users_db else "client"
        token = create_access_token({"sub": data.username, "role": role})
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı veya geçersiz kod")


    # Danışan login (access_code)
    elif data.username in fake_access_codes:
        role = fake_access_codes[data.username]["role"]
        sub = data.username
        # Kod tek kullanımlık ise burada silebilirsin
        del fake_access_codes[data.username]

    else:
        raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı veya geçersiz kod")

    token = create_access_token({
        "sub": sub,
        "role": role
    })

    return {"access_token": token, "token_type": "bearer"}


@app.post("/triage")
def triage(data: TriageRequest):
    return {
        "message": "Ön değerlendirme alındı",
        "stress_level": data.stress_level,
        "confidence": data.confidence
    }


