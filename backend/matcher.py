import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILLS = [
    "java", "python", "javascript", "react", "html", "css", "sql", "mysql",
    "servlets", "jsp", "jdbc", "hibernate", "spring", "spring boot",
    "rest api", "git", "github", "docker", "aws", "dsa", "oop",
    "fastapi", "flask", "node", "mongodb", "junit", "maven"
]

def clean(text):
    text = text.lower()
    return re.sub(r"[^a-z0-9+#\s]", " ", text)

IMPLIES = {"mysql": "sql", "spring boot": "spring", "github": "git"}

def extract_skills(text):
    text = clean(text)
    found = {s for s in SKILLS if re.search(rf"\b{re.escape(s)}\b", text)}
    for skill, implied in IMPLIES.items():
        if skill in found:
            found.add(implied)
    return found

def analyze(resume, jd):
    # 1. Text similarity (TF-IDF + cosine)
    tfidf = TfidfVectorizer(stop_words="english")
    vectors = tfidf.fit_transform([clean(resume), clean(jd)])
    text_score = cosine_similarity(vectors[0], vectors[1])[0][0] * 100

    # 2. Skill comparison
    resume_skills = extract_skills(resume)
    jd_skills = extract_skills(jd)
    matched = resume_skills & jd_skills

    # 3. Skill score = % of JD skills found in resume
    skill_score = (len(matched) / len(jd_skills) * 100) if jd_skills else text_score

    # final: 70% skills + 30% text similarity
    final = 0.7 * skill_score + 0.3 * text_score

    return {
        "score": round(final, 1),
        "matched": sorted(matched),
        "missing": sorted(jd_skills - resume_skills),
    }

if __name__ == "__main__":
    resume = "Java developer with Servlets, JSP, JDBC, Hibernate and MySQL. Know HTML, CSS, JavaScript."
    jd = "Looking for Java developer with Spring Boot, Hibernate, MySQL, REST API and React experience."
    print(analyze(resume, jd))