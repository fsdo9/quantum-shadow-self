import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI(title="Quantum Shadow Self")

# .env 파일에서 불러온 API 키 적용
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    'gemini-1.5-flash',
    generation_config={"response_mime_type": "application/json"}
)

class QuantumState(BaseModel):
    focus: str
    regret: str
    intensity: int

@app.post("/quantum-leap")
def generate_shadow_self(state: QuantumState):
    try:
        prompt = f"""
        당신은 다중우주의 대체 자아(Shadow Self)를 분석하는 양자 심리학자입니다.
        사용자의 현재 상태: 삶의 초점({state.focus}), 가장 큰 미련({state.regret}), 관찰 강도({state.intensity}/10)
        
        이 정보를 바탕으로 평행우주에 존재하는 사용자의 프로필을 창작하세요.
        관찰 강도가 8 이상이면 매우 위험하고 극단적이어야 합니다.
        반드시 아래 JSON 형식으로만 응답하세요:
        {{
            "shadow_profile": "직업 및 상태 요약",
            "super_power": "초월적 강점 (1문장)",
            "fatal_flaw": "치명적 약점 (1문장)",
            "entanglement_message": "현실의 나에게 주는 철학적인 조언 (1문장)"
        }}
        """

        response = model.generate_content(prompt)
        result = json.loads(response.text)
        
        result["intensity_level"] = "high" if state.intensity >= 8 else "medium" if state.intensity >= 5 else "low"
        result["status"] = "success"
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))