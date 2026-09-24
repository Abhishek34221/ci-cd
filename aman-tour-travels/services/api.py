import os
import requests

FASTAPI_BASE_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

class ApiService:
    @staticmethod
    def register_user(payload):
        try:
            response = requests.post(f"{FASTAPI_BASE_URL}/auth/register", json=payload, timeout=30)
            
            # Check if response has text content
            if not response.text.strip():
                return {"detail": "Server returned an empty response."}, response.status_code
                
            try:
                return response.json(), response.status_code
            except ValueError:
                # Agar response JSON nahi hai (jaise HTML error page)
                return {"detail": response.text}, response.status_code
                
        except requests.exceptions.RequestException as e:
            return {"detail": str(e)}, 503

    @staticmethod
    def login_user(payload):
        try:
            response = requests.post(f"{FASTAPI_BASE_URL}/auth/login", json=payload, timeout=30)
            
            if not response.text.strip():
                return {"detail": "Server returned an empty response."}, response.status_code
                
            try:
                return response.json(), response.status_code
            except ValueError:
                return {"detail": response.text}, response.status_code
                
        except requests.exceptions.RequestException as e:
            return {"detail": str(e)}, 503

    @staticmethod
    def get_users(token):
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.get(f"{FASTAPI_BASE_URL}/users/", headers=headers, timeout=30)
            
            if not response.text.strip():
                return [], response.status_code
                
            try:
                return response.json(), response.status_code
            except ValueError:
                return {"detail": response.text}, response.status_code
                
        except requests.exceptions.RequestException as e:
            return {"detail": str(e)}, 503