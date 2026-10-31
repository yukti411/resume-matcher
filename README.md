# Resume Matcher

Compares a resume with a job description and shows a match score, matched skills, and missing skills.

## Tech Stack
Python, FastAPI, scikit-learn (TF-IDF, cosine similarity), React (Vite), MySQL

## How it works
1. User pastes resume and job description in React.
2. React sends a POST request to the FastAPI `/analyze` endpoint.
3. Backend computes the TF-IDF cosine similarity score and compares skill sets.
4. Result is saved in MySQL and shown in the UI. History is available at `/history`.

## Run locally
Backend:
    cd backend
    venv\Scripts\activate
    uvicorn main:app --reload

Frontend:
    cd frontend
    npm install
    npm run dev

## Future improvements
Sentence embeddings for meaning-based matching, PDF resume upload, user login.