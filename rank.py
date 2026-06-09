import json
import csv

TARGET_SKILLS = [
    "NLP",
    "Fine-tuning LLMs",
    "Vector Databases",
    "FAISS",
    "Pinecone",
    "Weaviate",
    "Elasticsearch",
    "Retrieval",
    "Embeddings",
    "Python"
]

def calculate_score(candidate):

    score = 0
    reasons = []

    profile = candidate.get("profile", {})
    skills = candidate.get("skills", [])
    signals = candidate.get("redrob_signals", {})
    education = candidate.get("education", [])

    # EXPERIENCE SCORE (20)

    exp = profile.get("years_of_experience", 0)

    if 5 <= exp <= 9:
        score += 20
        reasons.append("Ideal experience")

    elif exp >= 3:
        score += 10

    # SKILLS SCORE (50)

    skill_names = [s.get("name", "") for s in skills]

    matched = 0

    for target in TARGET_SKILLS:
        if target in skill_names:
            matched += 1

    skill_score = min(matched * 5, 50)

    score += skill_score

    if matched:
        reasons.append(f"{matched} relevant AI skills")

    # BEHAVIOR SCORE (20)

    if signals.get("open_to_work_flag"):
        score += 5

    score += min(signals.get("github_activity_score", 0), 5)

    score += min(
        signals.get("interview_completion_rate", 0) * 5,
        5
    )

    score += min(
        signals.get("recruiter_response_rate", 0) * 5,
        5
    )

    # EDUCATION SCORE (10)

    if education:

        edu = education[0]

        degree = str(edu.get("degree", "")).lower()

        if "b.tech" in degree or "b.e" in degree:
            score += 5

        if "computer" in str(
            edu.get("field_of_study", "")
        ).lower():
            score += 5

    return score, "; ".join(reasons)


results = []

with open(
    "candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        candidate = json.loads(line)

        score, reason = calculate_score(candidate)

        results.append({
            "candidate_id":
            candidate["candidate_id"],
            "score": round(score, 2),
            "reasoning": reason
        })

results.sort(
    key=lambda x: x["score"],
    reverse=True
)

top100 = results[:100]

for rank, row in enumerate(top100, start=1):
    row["rank"] = rank

with open(
    "submission.csv",
    "w",
    newline="",
    encoding="utf-8"
) as csvfile:

    writer = csv.DictWriter(
        csvfile,
        fieldnames=[
            "candidate_id",
            "rank",
            "score",
            "reasoning"
        ]
    )

    writer.writeheader()

    writer.writerows(top100)

print("Top 100 candidates generated!")
print("submission.csv created successfully!")