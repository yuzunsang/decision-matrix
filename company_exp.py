import streamlit as st
import pandas as pd

# ✅ 1. 반드시 가장 먼저 호출
st.set_page_config(page_title="회사 결정 도우미", layout="centered")

# ✅ 2. 모바일 브라우저 사용자에게 안내 (앱 내 웹뷰 방지)
if st.session_state.get("mobile_tip_shown") is None:
    st.session_state.mobile_tip_shown = True
    st.warning(
        "⚠️ 모바일에서는 **크롬 앱** 또는 **사파리 앱**에서 열어주세요.\n\n"
        "카카오톡, 인스타그램 등의 앱 내 브라우저에서는 화면이 멈출 수 있습니다."
    )

# ✅ 3. 타이틀 및 설명 (이모지 제거)
st.title("회사 결정 도우미")
st.text("회사 선택을 위한 평가 항목별 점수를 입력하면 자동으로 점수와 순위를 계산해 드립니다")

# ✅ 4. 사용자 입력: 회사 및 평가 항목
company_input = st.text_input("✅ 회사명들을 입력하세요 (쉼표로 구분)", "A회사, B회사, C회사")
criteria_input = st.text_input("✅ 평가 항목들을 입력하세요 (쉼표로 구분)", "연봉, 워라밸, 근무지, 전망, 직무 호감성")

companies = [x.strip() for x in company_input.split(",") if x.strip()]
criteria = [x.strip() for x in criteria_input.split(",") if x.strip()]

# ✅ 5. 평가 로직 실행 조건
if len(companies) >= 2 and len(criteria) >= 2:
    st.divider()
    st.subheader("평가 항목 우선순위 설정 (1순위가 가장 중요)")

    # ✅ 6. 항목별 우선순위 선택 (중복 허용)
    priority = {}
    ranks = list(range(1, len(criteria) + 1))
    for c in criteria:
        rank = st.selectbox(
            f"{c}의 우선순위",
            options=ranks,
            index=ranks.index(1),  # 기본값 1순위
            key=f"priority_{c}"
        )
        priority[c] = rank

    # ✅ 7. 가중치 계산: 낮은 순위일수록 높은 가중치
    weights = {k: len(criteria) - v + 1 for k, v in priority.items()}

    st.divider()
    st.subheader("회사별 항목 점수 입력 (1~5점)")

    score_data = {}
    for company in companies:
        with st.expander(f"{company} 점수 입력"):
            scores = {}
            for c in criteria:
                scores[c] = st.slider(f"{c} 점수", 1, 5, 3, key=f"{company}_{c}")
            score_data[company] = scores

    # ✅ 8. 총점 계산
    final_scores = {
        company: sum(scores[c] * weights[c] for c in criteria)
        for company, scores in score_data.items()
    }

    # ✅ 9. 결과 출력
    result_df = pd.DataFrame([
        {"회사명": name, "총점": score}
        for name, score in final_scores.items()
    ])
    result_df["순위"] = result_df["총점"].rank(ascending=False, method='min').astype(int)
    result_df = result_df.sort_values(by="총점", ascending=False).reset_index(drop=True)

    st.divider()
    st.subheader("최종 결과")
    st.dataframe(result_df, use_container_width=True)

else:
    st.warning("⚠️ 회사명과 평가 항목을 **최소 2개 이상** 입력해주세요.")
