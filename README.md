# Banking AI Customer Assistant

A Python-based AI assistant that helps bank employees answer customer-policy questions using **Retrieval-Augmented Generation (RAG)**.

The system retrieves relevant information from a fictional banking policy document, sends the retrieved context to an LLM, and returns a structured answer. Sensitive requests are routed to human review using deterministic business rules rather than allowing the LLM to make that decision.

> **Note:** This project uses fictional banking policies and does not make real financial, lending, fraud, or transaction decisions.

---

## Problem

Bank employees may need to repeatedly search internal policy documents to answer customer questions such as:

* What documents are required to change an address?
* How can a customer reset their password?
* What should an employee do when a debit card is lost?
* What should happen when an unauthorized transaction is reported?

Searching documents manually can be slow, while allowing an LLM to answer without policy context can lead to unsupported answers.

This project combines **semantic search + LLMs + deterministic business rules** to create a safer workflow.

---

## How It Works

```text
                Banking Policy PDF
                       |
                       v
                PDF Text Extraction
                       |
                       v
                  Policy Chunking
                       |
                       v
              Sentence Embeddings
                       |
                       v
                  FAISS Index
                       |
                       |
             Employee Question
                       |
                       v
               Semantic Search
                       |
                       v
             Relevant Policy Context
                       |
                       v
                    OpenAI
                       |
                       v
              Structured AI Answer
                       |
                       v
             Human Review Rules
                       |
                       v
                  API Response
```

---

## Key Features

### 1. RAG-based question answering

The system retrieves relevant policy sections before asking the LLM to generate an answer.

This reduces the chance of the model inventing information that is not present in the policy document.

### 2. Semantic search

The project uses:

* `sentence-transformers`
* `all-MiniLM-L6-v2`
* FAISS

Questions are converted into embeddings and compared with policy embeddings to find relevant information.

### 3. Relevance filtering

Search results are filtered using a distance threshold.

Weak matches are rejected instead of automatically being sent to the LLM.

### 4. Structured AI output

The LLM response uses a Pydantic model:

```json
{
  "answer": "Customers need government-issued photo ID, proof of the new address, and a completed address-change form.",
  "source": "Address Change Policy"
}
```

### 5. Deterministic human-review routing

Sensitive cases are handled by Python business rules instead of allowing the LLM to decide whether human review is required.

Examples include:

* Fraud-related requests
* Unauthorized transactions
* Lost or stolen cards
* Duplicate charges
* Information not found in the policy

### 6. API

The application exposes a FastAPI endpoint:

```text
POST /ask
```

Example request:

```json
{
  "question": "What documents are required to change my address?"
}
```

Example response:

```json
{
  "answer": "To change your residential address, provide government-issued photo identification, proof of the new address, and a completed address-change request form.",
  "source": "Address Change Policy",
  "requires_human_review": false
}
```

---

## Example Human Review Case

Request:

```json
{
  "question": "Someone used my card without permission."
}
```

The application identifies this as a sensitive request and routes it for human review.

The AI assistant does not independently determine whether fraud occurred.

---

## Handling Unknown Information

If a question is outside the available policy, the system does not invent an answer.

Example:

```text
Question:
How can I apply for a home loan?

Result:
No relevant policy information was found.
```

This is an important part of the system's design: **not every question should receive an AI-generated answer.**

---

## Evaluation

The project includes a small evaluation dataset containing 10 representative questions.

Current results:

| Metric                  | Result |
| ----------------------- | -----: |
| Policy source retrieval |    90% |
| Human-review routing    |   100% |
| Questions evaluated     |     10 |
| Automated API tests     |    4/4 |

The evaluation intentionally includes unsupported questions and sensitive banking scenarios.

---

## Testing

Run the automated tests:

```bash
PYTHONPATH=. pytest tests/test_rag.py -v
```

Expected result:

```text
4 passed
```

Run the evaluation:

```bash
PYTHONPATH=. python evaluation/evaluate.py
```

---

## Project Structure

```text
banking-ai-customer-assistant/
│
├── app/
│   ├── __init__.py
│   ├── chunker.py
│   ├── document.py
│   ├── embeddings.py
│   ├── llm.py
│   ├── main.py
│   ├── mock_llm.py
│   ├── search.py
│   ├── test_openai.py
│   └── test_pipeline.py
│
├── data/
│   ├── banking_policy.pdf
│   └── banking_policy.txt
│
├── evaluation/
│   ├── evaluate.py
│   └── questions.json
│
├── tests/
│   └── test_rag.py
│
├── create_policy_pdf.py
├── requirements.txt
└── README.md
```

---

## Technologies

* Python
* FastAPI
* OpenAI API
* Sentence Transformers
* FAISS
* Pydantic
* PyMuPDF
* ReportLab
* Pytest

---

## Running the Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure the OpenAI API key

Create a `.env` file:

```text
OPENAI_API_KEY=your_api_key_here
```

Never commit the `.env` file to GitHub.

### 3. Start the API

```bash
uvicorn app.main:app --reload
```

Open the FastAPI documentation:

```text
/docs
```

### 4. Test the API

Use the `/ask` endpoint with a question such as:

```json
{
  "question": "What documents are required to change my address?"
}
```

---

## What I Learned

This project demonstrates practical experience with:

* Building a RAG pipeline from a PDF
* Document extraction and chunking
* Embedding-based semantic search
* FAISS vector search
* LLM integration
* Structured outputs with Pydantic
* FastAPI backend development
* Deterministic business rules
* Human-in-the-loop AI workflows
* Automated testing
* Small-scale AI evaluation
* Handling unsupported questions without hallucinating

---

## Future Improvements

Potential next improvements include:

* Add page numbers to retrieved sources
* Improve retrieval evaluation
* Add a lightweight web interface
* Add document upload support
* Add more evaluation cases
* Add retrieval confidence scoring
* Add logging and monitoring
* Deploy the application
