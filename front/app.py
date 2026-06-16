import streamlit as st
import requests

st.set_page_config(page_title="Quantum Shadow Self", layout="centered")

st.title("🌌 Quantum Shadow Self")
st.subheader("당신이 선택하지 않은 다중우주의 '나'를 관찰합니다.")

with st.form("quantum_form"):
    focus = st.selectbox("현재 삶에서 당신을 지배하는 키워드는?", ["안정/돈", "자아실현/창작", "관계/사랑"])
    regret = st.selectbox("가장 짙게 남아있는 미련은?", ["가지 못한 길", "포기한 관계", "타협한 신념"])
    intensity = st.slider("양자 관찰 강도 (숫자가 높을수록 위험한 분신이 도출됩니다)", 1, 10, 5)
    
    submitted = st.form_submit_button("차원 균열 열기 ⚡")

if submitted:
    # Docker 환경 백엔드 API 호출
    API_URL = "http://backend:8000/quantum-leap"
    
    with st.spinner('다중우주의 파동을 탐색 중입니다...'):
        try:
            response = requests.post(API_URL, json={
                "focus": focus, 
                "regret": regret, 
                "intensity": intensity
            }, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                st.success("✅ 관찰 완료. 당신의 대체 자아를 발견했습니다.")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"### 👤 **{result['shadow_profile']}**")
                    st.markdown(f"**초월적 강점** \n{result['super_power']}")
                with col2:
                    st.markdown(f"**치명적 약점** \n{result['fatal_flaw']}")
                
                st.info(f"**💌 Entanglement Message**\n\n{result['entanglement_message']}")
                
                if result.get("intensity_level") == "high":
                    st.warning("⚠️ 이 분신은 매우 위험합니다. 현실 세계의 자아와 동기화되지 않도록 주의하세요.")
            else:
                st.error(f"차원 통신 실패: {response.status_code}")
        except Exception as e:
            st.error(f"백엔드 연결 실패: {str(e)}")