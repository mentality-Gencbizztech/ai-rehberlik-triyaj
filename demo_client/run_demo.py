import cv2
import mediapipe as mp
import requests
import time

# =====================
# AYARLAR
# =====================
BACKEND_URL = "https://ai-rehberlik-triyaj.onrender.com/triage"  # Render backend URL
GEMINI_API_KEY = "AIzaSyCXmV3DcqF6l9v8zt6NArkkkCLmFEzBbeU"  # Gemini API key (değiştir)

# =====================
# OpenCV & MediaPipe
# =====================
cap = cv2.VideoCapture(0)
mp_face = mp.solutions.face_mesh.FaceMesh()

print("Kamera açıldı. Çıkmak için 'q' tuşuna basın.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Kameradan görüntü alınamadı.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = mp_face.process(rgb_frame)

        # Basit demo: yüz algılanırsa stress medium, yoksa low
        stress_level = "low"
        if results.multi_face_landmarks:
            stress_level = "medium"

        # Backend'e gönder
        payload = {
            "stress_level": stress_level,
            "confidence": 0.7
        }

        try:
            response = requests.post(BACKEND_URL, json=payload)
            print("Backend cevabı:", response.json())
        except Exception as e:
            print("Backend bağlantı hatası:", e)

        # Gemini chatbot demo
        try:
            gemini_payload = {
                "messages": [
                    {"role": "system", "content": "Kullanıcıyı sakinleştir."},
                    {"role": "user", "content": f"Stres seviyesi {stress_level}"}
                ]
            }
            gemini_response = requests.post(
                "https://api.gemini.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {GEMINI_API_KEY}"},
                json=gemini_payload
            )
            print("Gemini cevabı:", gemini_response.json())
        except Exception as e:
            print("Gemini bağlantı hatası:", e)

        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        time.sleep(1)  # Her saniye gönder

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Kamera kapatıldı.")
