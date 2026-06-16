import streamlit as st
import requests

st.set_page_config(page_title="Quantum Shadow Self", layout="centered")

st.title("🌌 Quantum Shadow Self")
st.subheader("당신이 선택하지 않은 다중우주의 '나'를 관찰합니다.")
st.markdown("""
> 당신의 현재 삶, MBTI, 후회, 그리고 숨겨진 욕망을 입력하면  
> 다중우주에서 **다른 선택을 한 대체 자아(Shadow Self)** 를 도출합니다.  
>
> 이것은 단순한 심리테스트가 아닙니다.  
> **융 심리학의 그림자 이론 + 다중우주 해석 + 양자적 관찰**을 결합한  
> 자기성찰 추천 시스템입니다.
""")

with st.expander("💡 이 시스템으로 무엇을 얻을 수 있나요?"):
    st.markdown("""
    **1. 숨겨진 가능성을 구체적으로 마주하는 경험**  
    막연하게만 생각하던 '다른 삶'을 이름, 능력, 삶의 이야기, 약점까지 구체적으로 보여줍니다.

    **2. 그림자(Shadow)와의 대화**  
    융 심리학의 Shadow(억압된 자아, 포기한 부분, 숨긴 욕망)를 다중우주라는 설정으로 안전하게 만납니다.

    **3. 추상적인 성찰 → 구체적인 행동으로 연결**  
    철학적 통찰 + 오늘 당장 실행 가능한 행동을 함께 제공합니다.

    **4. 미래를 설계하는 훈련**  
    여러 번 반복하면 내가 어떤 선택을 반복하는지, 어떤 후회가 가장 강한지 패턴이 보입니다.

    **5. 감정적·심리적 카타르시스**  
    후회와 미련을 객관화하고, 자기 긍정감과 자기연민을 동시에 경험합니다.
    """)

st.divider()

MBTI_LIST = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
             "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]

with st.form("quantum_form"):
    st.markdown("### 🔮 관찰 데이터 입력")

    st.markdown("**① 나의 MBTI**")
    st.caption("당신의 MBTI를 선택하세요. 분신의 방향과 솔루션이 MBTI 특성에 맞게 설계됩니다.")
    mbti = st.selectbox("", MBTI_LIST)

    st.markdown("**② 현재 삶에서 당신을 지배하는 키워드**")
    st.caption("지금 가장 많은 에너지를 쏟고 있는 것을 자유롭게 적어주세요. ex) 취업 준비, 돈, 창작, 관계...")
    focus = st.text_input("", placeholder="지금 내 삶의 중심은?")

    st.markdown("**③ 가장 짙게 남아있는 미련**")
    st.caption("지금도 가끔 떠오르는 '그때 그랬더라면...' 하는 순간을 선택하세요.")
    regret = st.selectbox(" ", ["가지 못한 길", "포기한 관계", "타협한 신념"])

    st.markdown("**④ 양자 관찰 강도**")
    st.caption("1: 살짝 다른 나 / 5~7: 꽤 다른 나 / 8~10: 완전히 다른 차원의 위험한 나")
    intensity = st.slider("관찰 강도", 1, 10, 5)

    submitted = st.form_submit_button("차원 균열 열기 ⚡")

if submitted:
    if not focus:
        st.warning("⚠️ 삶의 키워드를 입력해주세요!")
    else:
        API_URL = "http://backend:8000/quantum-leap"
        with st.spinner("다중우주의 파동을 탐색 중입니다..."):
            try:
                response = requests.post(API_URL, json={
                    "focus": focus,
                    "regret": regret,
                    "intensity": intensity,
                    "mbti": mbti
                }, timeout=30)

                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ 관찰 완료. 당신의 대체 자아를 발견했습니다.")
                    st.divider()

                    # ── 1. 현실의 나 ──────────────────────────────
                    st.markdown("## 🪞 현실의 나 — 관찰 시작점")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f"**🧬 MBTI:** `{result.get('mbti', '')}`")
                        st.markdown(f"**🧭 삶의 유형:** `{result.get('focus_type', '')}`")
                        st.markdown(f"**🎯 삶의 키워드:** {focus}")
                    with col_b:
                        st.markdown(f"**💭 가장 큰 미련:** {regret}")
                        st.markdown(f"**⚡ 관찰 강도:** {intensity}/10")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("#### 💪 나의 강점")
                        st.success(result.get("mbti_strengths", ""))
                    with col2:
                        st.markdown("#### ⚠️ 나의 약점")
                        st.error(result.get("mbti_weaknesses", ""))
                    st.caption("💡 Shadow Self는 이 약점을 극복한 대신, 강점을 잃어버린 존재입니다.")

                    st.divider()

                    # ── 2. Shadow Self 프로필 ─────────────────────
                    st.markdown("## 👤 Shadow Self — 다중우주의 또 다른 나")
                    st.caption("당신이 다른 선택을 했을 때 존재했을 대체 자아입니다.")
                    st.info(f"**{result['shadow_profile']}**")

                    col3, col4 = st.columns(2)
                    with col3:
                        st.markdown("### 🌟 초월적 강점")
                        st.success(result['super_power'])
                        st.caption("현실의 나의 약점을 극복하며 얻어낸 능력입니다.")
                    with col4:
                        st.markdown("### 💀 치명적 약점")
                        st.error(result['fatal_flaw'])
                        st.caption("현실의 나의 강점을 포기한 대가입니다.")

                    st.markdown("### 📖 그 세계에서의 삶")
                    st.write(result.get("life_story", ""))

                    st.divider()

                    # ── Entanglement Message ──────────────────────
                    st.markdown("## 💌 Entanglement Message")
                    st.caption("평행우주의 당신이 현실의 당신에게 보내는 유일한 신호입니다.")
                    st.markdown(f"> ### *{result['entanglement_message']}*")

                    st.divider()

                    # ── 3. Bridge Ritual ──────────────────────────
                    st.markdown("## 🌉 Bridge Ritual — 분신의 힘을 현실로")
                    st.caption(f"당신의 MBTI({mbti}) 약점을 극복하기 위한 지금 당장 실행 가능한 행동입니다.")
                    rituals = [l.strip() for l in result.get("bridge_ritual", "").split("\n") if l.strip()]
                    for i, ritual in enumerate(rituals, 1):
                        st.markdown(f"""
                        <div style='background:#d4edda; color:#155724; padding:16px; border-radius:10px;
                        margin-bottom:10px; border-left:4px solid #28a745;'>
                        <b>Step {i}</b><br>{ritual}
                        </div>""", unsafe_allow_html=True)

                    st.markdown("### 🎯 지금 당장 해볼 수 있는 것들")
                    st.caption("추상적인 성찰에서 끝나지 않고, 오늘의 구체적인 행동으로 연결합니다.")
                    actions = [l.strip() for l in result.get("action_guide", "").split("\n") if l.strip()]
                    for action in actions:
                        st.markdown(f"""
                        <div style='background:#cce5ff; color:#004085; padding:14px; border-radius:10px;
                        margin-bottom:8px; border-left:4px solid #4a9eff;'>
                        ✅ {action}
                        </div>""", unsafe_allow_html=True)

                    st.divider()

                    # ── 4. 미래 설계 ──────────────────────────────
                    st.markdown("## 🗺️ 미래 설계 훈련")
                    st.caption("한 번으로 끝내지 마세요. 반복할수록 당신의 선택 패턴이 보이기 시작합니다.")
                    futures = [l.strip() for l in result.get("future_design", "").split("\n") if l.strip()]
                    for future in futures:
                        st.markdown(f"""
                        <div style='background:#fff3cd; color:#856404; padding:14px; border-radius:10px;
                        margin-bottom:8px; border-left:4px solid #ffc107;'>
                        🔮 {future}
                        </div>""", unsafe_allow_html=True)
                    st.caption("💡 이 시스템을 매주 한 번씩 사용하면, 3~4주 후 자신의 패턴을 발견하게 됩니다.")

                    st.divider()

                    # ── 5. 감정 카타르시스 ────────────────────────
                    st.markdown("## 🫀 감정적·심리적 카타르시스")
                    st.caption("이 분신을 보며 어떤 감정이 드나요? 그 감정이 바로 당신의 Shadow가 보내는 신호입니다.")
                    catharsis = [l.strip() for l in result.get("catharsis_guide", "").split("\n") if l.strip()]
                    for item in catharsis:
                        st.markdown(f"""
                        <div style='background:#f3e5f5; color:#4a148c; padding:14px; border-radius:10px;
                        margin-bottom:8px; border-left:4px solid #9b59b6;'>
                        💜 {item}
                        </div>""", unsafe_allow_html=True)

                    st.divider()

                    # ── 자기성찰 질문 ─────────────────────────────
                    st.markdown("## 🔍 Shadow와의 대화 — 스스로에게 던지는 질문")
                    st.caption("일기에 써보거나, 조용히 혼자 생각해보세요.")
                    st.markdown(f"""
                    - 🌀 이 Shadow Self의 삶이 **끌리나요, 두렵나요?** 그 감정의 이유는?
                    - 🌀 내가 **"{regret}"**을 미련으로 갖고 있는 진짜 이유는?
                    - 🌀 Shadow Self의 강점 중 **지금 1%라도 내 삶에 가져올 수 있는 것**은?
                    - 🌀 나의 MBTI 약점 **"{result.get('mbti_weaknesses', '')}"** — 이것이 나를 어떻게 제한해왔나?
                    """)

                    st.divider()

                    # ── Quantum Vision ────────────────────────────
                    if "visual_prompt" in result:
                        seed = abs(hash(result["shadow_profile"])) % 1000
                        st.markdown("## 🎨 Quantum Vision")
                        st.image(f"https://picsum.photos/seed/{seed}/600/300",
                                caption="Shadow Self의 세계 (시각화 예시)")
                        st.caption(f"*Visual Prompt: {result['visual_prompt'][:150]}...*")

                    if result.get("intensity_level") == "high":
                        st.divider()
                        st.warning("⚠️ 관찰 강도가 임계치를 초과했습니다. Shadow와의 동기화는 카타르시스를 줄 수 있지만, 현실의 자아를 잃지 않도록 주의하세요.")

                    st.markdown("---")
                    st.markdown("""
                    <div style='text-align:center; color:#888; padding:20px;'>
                    🌌 <i>당신이 선택하지 않은 삶도, 당신의 일부입니다.</i><br>
                    <small>Quantum Shadow Self — 다중우주 자기성찰 추천 엔진</small>
                    </div>""", unsafe_allow_html=True)

                else:
                    st.error(f"차원 통신 실패: {response.status_code}")
            except Exception as e:
                st.error(f"백엔드 연결 실패: {str(e)}")
