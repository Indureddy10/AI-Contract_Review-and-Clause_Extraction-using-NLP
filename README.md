
# **AI Contract Review System**

An NLP-based tool that lets users upload legal documents and automatically extracts raw text, identifies key clauses, and generates a concise summary.
## **Objective**

Automate contract review and reduce manual effort using NLP.

## **Features**

* Upload PDF/DOCX/TXT
* Extract text
* Summarize content
* Detect key clauses (Termination, Indemnification, etc.)
* Extract entities (Dates, Organizations, Money)
* Store results in PostgreSQL
* JWT Authentication

## **Run with Docker**

```bash
docker-compose build
docker-compose up
```

**Backend:** [http://localhost:5000](http://localhost:5000)
**Frontend:** [http://localhost:3000](http://localhost:3000)

## **Run Backend Without Docker**

```bash
cd Backend
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python app.py
```
## **API**

```
POST /api/doc/upload
POST /api/doc/process/<doc_id>
GET  /api/doc/result/<doc_id>
POST /api/auth/login
