import streamlit as st
import pandas as pd

# ✅ 반드시 가장 먼저 호출되어야 함
st.set_page_config(page_title="회사 결정 도우미", layout="centered")

# ✅ 모바일 안내 메시지 (한 번만 표시)
if st.session_state.get("is_mobile_warning_shown") is None:
    st.session_state.is_mobile_warning_shown = True
    st.info("📱 모바일에서 화면이 깨지거나 오류가 발생한다면, 크롬 또는 최신 브라우저에서 열어주세요.")

# ✅ 타이틀 및 설명
st.title("🏢 회사 결정 도우미")
st.text("회사 선택을 위한 평가 항목별 점수를 입력하면 자동으로 점수와 순위를 계산해 드립니다")

# ✅ 사용자 입력: 회사 및 항목
company_input = st.text_input("✅ 회사명들을 입력하세요 (쉼표로 구분)", "A회사, B회사, C회사")
criteria_input = st.text_input("✅ 평가 항목들을 입력하세요 (쉼표로 구분)", "연봉, 워라밸, 근무지, 전망, 직무 호감성")

companies = [x.strip() for x in company_input.split(",") if x.strip()]
criteria = [x.strip() for x in criteria_input.split(",") if x.strip()]

if len(companies) >= 2 and len(criteria) >= 2:
    st.text("---")
    st.subheader("📊 평가 항목 우선순위 설정 (1순위가 가장 중요)")
    
    priority = {}
    used_values = set()
    for c in criteria:
        rank = st.selectbox(
            f"{c}의 우선순위",
            options=[i for i in range(1, len(criteria) + 1) if i not in used_values],
            key=f"priority_{c}"
        )
        priority[c] = rank
        used_values.add(rank)

    weights = {k: len(criteria) - v + 1 for k, v in priority.items()}

    st.text("---")
    st.subheader("✏️ 회사별 항목 점수 입력 (1~5점)")

    score_data = {}
    for company in companies:
        with st.expander(f"{company} 점수 입력"):
            scores = {}
            for c in criteria:
                scores[c] = st.slider(f"{c} 점수", 1, 5, 3, key=f"{company}_{c}")
            score_data[company] = scores

    # ✅ 점수 계산
    final_scores = {
        company: sum(scores[c] * weights[c] for c in criteria)
        for company, scores in score_data.items()
    }

    # ✅ 결과 정리
    result_df = pd.DataFrame([
        {"회사명": name, "총점": score}
        for name, score in final_scores.items()
    ])
    result_df["순위"] = result_df["총점"].rank(ascending=False, method='min').astype(int)
    result_df = result_df.sort_values(by="총점", ascending=False).reset_index(drop=True)

    st.text("---")
    st.subheader("📈 최종 결과")
    st.dataframe(result_df, use_container_width=True)

else:
    st.warning("⚠️ 회사명과 평가 항목을 최소 2개 이상 입력해주세요.")
