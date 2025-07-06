import pandas as pd

def get_company_decision_result():
    # 1. 회사 및 항목 입력
    print("회사명을 입력하세요 (쉼표로 구분):")
    company_names = input().strip().split(",")
    company_names = [c.strip() for c in company_names]

    print("평가 항목들을 입력하세요 (쉼표로 구분):")
    criteria = input().strip().split(",")
    criteria = [c.strip() for c in criteria]

    num_criteria = len(criteria)

    # 2. 우선순위 입력
    print("\n각 평가 항목에 대한 우선순위를 입력하세요 (1이 가장 중요, 중복 없이)")
    priority = {}
    for c in criteria:
        rank = int(input(f"{c} 항목의 우선순위 (1~{num_criteria}): "))
        priority[c] = rank

    # 우선순위를 가중치로 변환 (역순: 1순위 → 최고 가중치)
    max_score = num_criteria
    weights = {k: max_score - v + 1 for k, v in priority.items()}

    # 3. 회사별 항목 점수 입력
    print("\n각 회사에 대해 항목별 점수를 1~5 사이로 입력하세요.")
    score_data = {}
    for company in company_names:
        print(f"\n{company} 회사:")
        scores = {}
        for c in criteria:
            s = int(input(f"  {c} 점수 (1~5): "))
            scores[c] = s
        score_data[company] = scores

    # 4. 점수 계산
    final_scores = {}
    for company, scores in score_data.items():
        total = sum(scores[c] * weights[c] for c in criteria)
        final_scores[company] = total

    # 5. 결과 출력
    result_df = pd.DataFrame([
        {"회사명": name, "총점": score}
        for name, score in final_scores.items()
    ])
    result_df["순위"] = result_df["총점"].rank(ascending=False, method='min').astype(int)
    result_df = result_df.sort_values(by="총점", ascending=False).reset_index(drop=True)

    print("\n📊 최종 결과:")
    print(result_df.to_string(index=False))

# 실행
get_company_decision_result()
