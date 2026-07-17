import requests
import json
from config import API_URL, API_KEY, MODEL_NAME, TIMEOUT

def get_ai_answer(system_content: str, user_question: str):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json;charset=utf-8"
    }
    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_question}
    ]
    payload = {
        "model": MODEL_NAME,
        "messages": messages
    }
    # 解决中文latin-1编码报错
    json_str = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    resp = requests.post(
        url=API_URL,
        data=json_str,
        headers=headers,
        timeout=TIMEOUT
    )
    return resp