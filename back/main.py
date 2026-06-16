import os
import re
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq

app = FastAPI(title="Quantum Shadow Self")

API_KEY = os.environ.get("GROQ_API_KEY")
print(f"API KEY Loaded: {API_KEY[:10]}...")

client = Groq(api_key=API_KEY)

def remove_foreign_chars(text: str) -> str:
    # 한자 제거 (CJK Unified Ideographs)
    text = re.sub(r'[\u4e00-\u9fff]', '', text)
    # 일본어 히라가나/카타카나 제거
    text = re.sub(r'[\u3040-\u30ff]', '', text)
    # 러시아어/키릴 문자 제거
    text = re.sub(r'[\u0400-\u04ff]', '', text)
    # 아랍어 제거
    text = re.sub(r'[\u0600-\u06ff]', '', text)
    # 연속 공백 정리
    text = re.sub(r' +', ' ', text).strip()
    return text

def clean_result(result: dict) -> dict:
    text_fields = ["shadow_profile", "super_power", "fatal_flaw", "life_story",
                   "entanglement_message", "bridge_ritual", "action_guide",
                   "future_design", "catharsis_guide"]
    for field in text_fields:
        if field in result:
            result[field] = remove_foreign_chars(result[field])
    return result

MBTI_DATA = {
    "INTJ": {
        "strengths": "전략적 사고, 독립심, 높은 목표 의식, 체계적 계획력",
        "weaknesses": "감정 표현 어려움, 지나친 완벽주의, 타인 의견 무시, 사회적 고립",
        "shadow_direction": "감정에 솔직하고 즉흥적인 자유로운 예술가 또는 공감 능력이 뛰어난 상담사"
    },
    "INTP": {
        "strengths": "논리적 분석력, 창의적 사고, 객관성, 지적 호기심",
        "weaknesses": "우유부단함, 감정 둔감, 실행력 부족, 사회적 어색함",
        "shadow_direction": "행동력 넘치는 기업가 또는 감성적인 예술가"
    },
    "ENTJ": {
        "strengths": "리더십, 결단력, 전략적 사고, 추진력",
        "weaknesses": "독선적, 감정 무시, 지나친 지배욕, 타인 배려 부족",
        "shadow_direction": "조용히 타인을 돌보는 봉사자 또는 감성적 창작자"
    },
    "ENTP": {
        "strengths": "창의력, 논쟁 능력, 적응력, 영감을 주는 능력",
        "weaknesses": "집중력 부족, 끈기 없음, 규칙 무시, 감정 경시",
        "shadow_direction": "한 가지에 깊이 몰두하는 장인 또는 규율적인 군인"
    },
    "INFJ": {
        "strengths": "깊은 공감 능력, 통찰력, 이상주의, 헌신적",
        "weaknesses": "번아웃 취약, 완벽주의, 갈등 회피, 자기희생 과다",
        "shadow_direction": "냉철한 현실주의자 또는 자기 이익을 챙기는 전략가"
    },
    "INFP": {
        "strengths": "따스한 마음, 자유로운 영혼, 창의성, 강한 가치관",
        "weaknesses": "우유부단함, 지나친 착함(호구), 비현실적 이상, 자기비판 과다",
        "shadow_direction": "냉정하고 결단력 있는 사업가 또는 규율 중심의 현실주의자"
    },
    "ENFJ": {
        "strengths": "카리스마, 공감 능력, 리더십, 타인 동기부여",
        "weaknesses": "타인 의존, 자기 감정 억압, 지나친 간섭, 거절 못함",
        "shadow_direction": "철저히 자신만을 위해 사는 고독한 철학자 또는 냉혹한 분석가"
    },
    "ENFP": {
        "strengths": "열정, 창의성, 사교성, 영감을 주는 능력",
        "weaknesses": "집중력 부족, 계획성 없음, 감정 기복, 끈기 부족",
        "shadow_direction": "철저한 계획가 또는 냉정한 데이터 과학자"
    },
    "ISTJ": {
        "strengths": "책임감, 신뢰성, 체계적, 인내심",
        "weaknesses": "변화 거부, 융통성 없음, 감정 표현 서툼, 지나친 보수성",
        "shadow_direction": "자유로운 예술가 또는 규칙을 파괴하는 혁명가"
    },
    "ISFJ": {
        "strengths": "헌신적, 배려심, 신뢰성, 세심함",
        "weaknesses": "자기주장 부족, 변화 두려움, 과도한 희생, 인정 욕구",
        "shadow_direction": "자기 욕망에 솔직한 야심가 또는 독립적인 탐험가"
    },
    "ESTJ": {
        "strengths": "조직력, 리더십, 신뢰성, 실행력",
        "weaknesses": "융통성 없음, 감정 무시, 지나친 통제욕, 독선적",
        "shadow_direction": "감성적인 예술가 또는 자유로운 방랑자"
    },
    "ESFJ": {
        "strengths": "사교성, 배려심, 협력, 충성심",
        "weaknesses": "타인 눈치, 갈등 회피, 자기 희생, 비판에 민감",
        "shadow_direction": "타인의 시선을 무시하는 독불장군 또는 냉정한 분석가"
    },
    "ISTP": {
        "strengths": "문제 해결력, 논리적, 독립심, 위기 대처 능력",
        "weaknesses": "감정 표현 어려움, 무관심해 보임, 충동적, 장기 계획 부족",
        "shadow_direction": "감성적인 상담사 또는 장기적 비전을 가진 전략가"
    },
    "ISFP": {
        "strengths": "예술적 감각, 온화함, 현재에 충실, 공감 능력",
        "weaknesses": "자기주장 약함, 갈등 회피, 계획성 부족, 비판에 예민",
        "shadow_direction": "강한 자기주장의 리더 또는 냉철한 현실주의 전략가"
    },
    "ESTP": {
        "strengths": "행동력, 적응력, 현실 감각, 사교성",
        "weaknesses": "충동적, 장기 계획 부족, 규칙 무시, 감정 경시",
        "shadow_direction": "깊이 사유하는 철학자 또는 체계적인 연구자"
    },
    "ESFP": {
        "strengths": "활발함, 즉흥성, 긍정 에너지, 사교성",
        "weaknesses": "집중력 부족, 계획성 없음, 깊이 없는 관계, 현실 회피",
        "shadow_direction": "고독 속에서 깊이 사유하는 철학자 또는 체계적 전략가"
    }
}

def ai_classify(focus: str) -> tuple[str, str]:
    classify_prompt = f"""
    다음 텍스트를 4가지 유형 중 하나로 분류하세요: "{focus}"
    1. 물질 추구형 - 돈, 재산, 성공, 지위, 유명인, 부자, 재벌 관련
    2. 관계 중심형 - 사랑, 관계, 가족, 사람 관련
    3. 창작 추구형 - 예술, 창작, 표현, 글쓰기 관련
    4. 자유 추구형 - 자유, 여행, 독립, 모험 관련
    반드시 JSON으로만 응답: {{"type": "물질 추구형", "direction": "예술가, 철학자, 방랑자 중 하나"}}
    """
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": classify_prompt}],
        response_format={"type": "json_object"},
        max_tokens=100
    )
    data = json.loads(res.choices[0].message.content)
    return data["type"], data["direction"]

def classify_focus(focus: str) -> tuple[str, str]:
    material_keywords = ["돈", "취업", "직장", "연봉", "건물", "투자",
                        "재테크", "부동산", "월급", "스펙", "자격증",
                        "부자", "건물주", "삼성", "이재용", "재벌", "주식",
                        "억대", "자산", "경제", "금융", "수익", "매출"]
    relation_keywords = ["관계", "사랑", "연애", "가족", "친구", "결혼",
                        "이별", "사람", "연인", "부모", "형제", "남친",
                        "여친", "짝사랑", "외로움", "인간관계"]
    creative_keywords = ["창작", "예술", "음악", "글", "그림", "디자인",
                        "영상", "작가", "창업", "개발", "코딩", "프로그래밍",
                        "유튜브", "콘텐츠", "작곡", "연기"]
    freedom_keywords = ["자유", "여행", "모험", "탈출", "독립", "방랑",
                       "휴식", "쉬고싶", "도망", "떠나고", "워홀", "배낭"]
    focus_lower = focus.lower()
    if any(k in focus_lower for k in material_keywords):
        return "물질 추구형", "예술가, 철학자, 방랑자, 비주류 창작자 중 하나"
    elif any(k in focus_lower for k in relation_keywords):
        return "관계 중심형", "고독한 천재, 무감각한 탐험가, 감정을 차단한 전략가 중 하나"
    elif any(k in focus_lower for k in creative_keywords):
        return "창작 추구형", "냉철한 기업가, 데이터 과학자, 군사 전략가 중 하나"
    elif any(k in focus_lower for k in freedom_keywords):
        return "자유 추구형", "안정적 엘리트 관료, 대기업 임원, 규율적 군인 중 하나"
    else:
        print(f"키워드 매칭 실패 → AI 분류: {focus}")
        return ai_classify(focus)

def classify_regret(regret: str) -> str:
    regret_lower = regret.lower()
    if any(k in regret_lower for k in ["포기", "그만", "중단", "접었"]):
        return "당신이 포기한 그 길을 끝까지 밀어붙인 버전의 자아"
    elif any(k in regret_lower for k in ["사람", "관계", "헤어", "이별", "떠나"]):
        return "그 사람과 함께하는 선택을 한 버전의 자아"
    elif any(k in regret_lower for k in ["도전", "창업", "시도", "지원"]):
        return "그 도전을 실행에 옮긴 버전의 자아"
    else:
        return "미련의 반대 방향으로 질주한 버전의 자아"

def classify_intensity(intensity: int) -> str:
    if intensity <= 3:
        return "살짝 다른 나 (Mild): 현실과 비슷하지만 핵심 선택 하나가 다른 조용한 분신"
    elif intensity <= 7:
        return "꽤 다른 나 (Medium): 직업, 생활방식, 가치관이 상당히 다른 분신"
    else:
        return "완전히 다른 차원의 나 (Wild): 현실의 나와 정반대에 가까운 극단적이고 위험한 분신"

def rule_based_fallback(state):
    focus_type, shadow_direction = classify_focus(state.focus)
    mbti_info = MBTI_DATA.get(state.mbti, MBTI_DATA["INFP"])
    return {
        "status": "fallback",
        "focus_type": focus_type,
        "mbti": state.mbti,
        "mbti_strengths": mbti_info["strengths"],
        "mbti_weaknesses": mbti_info["weaknesses"],
        "shadow_profile": f"{shadow_direction} 계열의 대체 자아",
        "super_power": "규칙을 거스르는 직관력",
        "fatal_flaw": f"{state.mbti}의 강점을 잃은 대가",
        "life_story": "선택하지 않은 길에서 살아가는 또 다른 나의 이야기.",
        "entanglement_message": "선택하지 않은 길이 당신을 여전히 부르고 있다.",
        "bridge_ritual": "오늘 하루, 가장 하고 싶었던 것을 딱 10분만 해보세요.\n내일은 한 가지 결정을 즉흥적으로 내려보세요.\n이번 주, 평소 하지 않던 행동을 하나 시도해보세요.",
        "action_guide": "오늘 당장 5분 동안 노트에 내가 진짜 원하는 것을 써보세요.\n작은 것부터 시작하세요. 완벽하지 않아도 됩니다.",
        "future_design": "매주 한 번씩 이 시스템을 사용해보세요. 반복할수록 패턴이 보입니다.",
        "catharsis_guide": "끌린다면: 그것이 당신의 진짜 욕망입니다. 억누르지 말고 들여다보세요.\n두렵다면: 그 두려움 안에 당신이 가장 원하는 것이 숨어있습니다.\n부럽다면: 부러움은 방향을 알려주는 나침반입니다.",
        "visual_prompt": "A mysterious shadow figure standing at a quantum crossroads, dramatic cinematic lighting",
        "intensity_level": "high" if state.intensity >= 8 else "medium" if state.intensity >= 5 else "low"
    }

class QuantumState(BaseModel):
    focus: str
    regret: str
    intensity: int
    mbti: str

@app.post("/quantum-leap")
def generate_shadow_self(state: QuantumState):
    try:
        focus_type, shadow_direction = classify_focus(state.focus)
        regret_context = classify_regret(state.regret)
        intensity_desc = classify_intensity(state.intensity)
        mbti_info = MBTI_DATA.get(state.mbti.upper(), MBTI_DATA["INFP"])

        prompt = f"""
        당신은 다중우주 최고 관찰자 'Quantum Oracle'입니다.

        [절대 규칙] 한국어로만 작성하세요. 한자, 일본어, 러시아어, 기타 외국어 문자를 단 한 글자도 사용하지 마세요. visual_prompt 필드만 예외적으로 영어로 작성합니다.

        [사용자 분석 데이터]
        - MBTI: {state.mbti}
        - MBTI 강점: {mbti_info['strengths']}
        - MBTI 약점: {mbti_info['weaknesses']}
        - 분신 방향 (MBTI 기반): {mbti_info['shadow_direction']}
        - 삶의 초점 유형: {focus_type} (키워드: {state.focus})
        - 분신 방향 (삶 기반): {shadow_direction}
        - 미련 맥락: {regret_context} (미련: {state.regret})
        - 관찰 강도: {intensity_desc} ({state.intensity}/10)

        [생성 규칙]
        - 분신은 MBTI 약점({mbti_info['weaknesses']})을 완전히 극복한 존재입니다.
        - 분신은 MBTI 강점({mbti_info['strengths']})을 잃어버린 대신 다른 능력을 얻었습니다.
        - 관찰 강도 8 이상이면 극단적이고 위험한 분신을 생성하세요.
        - 관찰 강도 3 이하이면 조용히 다른 분신을 생성하세요.

        반드시 아래 JSON 형식으로만 응답하세요:
        {{
            "shadow_profile": "분신의 이름(한국어), 직업, 한줄 설명",
            "super_power": "초월적 강점 1~2문장",
            "fatal_flaw": "치명적 약점 1~2문장",
            "life_story": "그 세계에서의 삶 3~4문장",
            "entanglement_message": "현실의 나에게 주는 날카로운 조언 시적으로",
            "bridge_ritual": "MBTI 약점 극복을 위한 오늘~이번주 실행 가능한 3가지 행동 (줄바꿈으로 구분)",
            "action_guide": "오늘 당장 해볼 수 있는 구체적 행동 2~3가지 (줄바꿈으로 구분)",
            "future_design": "미래 설계 방향 시나리오별 2~3가지 (줄바꿈으로 구분)",
            "catharsis_guide": "끌림/두려움/부러움 감정 유형별 수용 방법 각각 1~2문장 (줄바꿈으로 구분)",
            "visual_prompt": "영어로만 작성하는 이미지 생성 프롬프트 50단어 이상"
        }}
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.9,
            max_tokens=2000
        )

        result = json.loads(response.choices[0].message.content)
        result = clean_result(result)
        result["focus_type"] = focus_type
        result["mbti"] = state.mbti
        result["mbti_strengths"] = mbti_info["strengths"]
        result["mbti_weaknesses"] = mbti_info["weaknesses"]
        result["intensity_level"] = "high" if state.intensity >= 8 else "medium" if state.intensity >= 5 else "low"
        result["status"] = "success"
        return result

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return rule_based_fallback(state)
