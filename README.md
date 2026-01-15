# Product Vector Search System

This project implements a vector similarity search system for product names using Python, TF-IDF embeddings, and MySQL, with optional AWS Lambda deployment for serverless similarity search.

---

## Features

- Generates 500 synthetic product names
- Includes edge cases (similar names, typos)
- Converts text to TF-IDF embeddings
- Stores vectors in MySQL as JSON
- Performs cosine similarity search
- Optional AWS Lambda deployment
- Fully runnable locally

---

## Repository Structure

```
.
├── generate_products.py
├── embed_products.py
├── lambda_handler.py
├── create_table.sql
└── README.md
```

---

## 1. Data Generation (`generate_products.py`)

Generates 500 product names from categories such as Electronics, Fashion, and Groceries, including:
- Similar names (e.g., "iPhone 14" vs "iPhone 14 Pro")
- Typos (e.g., "Samzung", "Aple")

Output file: `products.csv`

Example:
| product_id | product_name            |
|-----------:|-------------------------|
| 1          | Apple iPhone 14 Pro     |
| 2          | Samzung Galaxy S21      |

---

## 2. Embedding & Storage (`embed_products.py`)

- Reads `products.csv`
- Converts product names to TF-IDF vectors
- Inserts into MySQL table `products_vectors` as JSON

### Database Schema (`create_table.sql`)

```sql
CREATE TABLE products_vectors (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    vector JSON
);

CREATE INDEX idx_product_name ON products_vectors(product_name);
```

---

## 3. Vector Similarity Search (`lambda_handler.py`)

Implements search using cosine similarity.

### Input Example
```json
{ "query": "Apple iPhone 14" }
```

### Output Example
```json
{
  "statusCode": 200,
  "results": [
    {
      "product_id": 1,
      "product_name": "Apple iPhone 14 Pro",
      "score": 0.91
    }
  ]
}
```

---

## Local Setup

### Install Dependencies

```bash
pip install mysql-connector-python scikit-learn pandas numpy
```

### Create Database and Table

```bash
mysql -u root -p
```

Inside MySQL:

```sql
CREATE DATABASE vector_db;
USE vector_db;
SOURCE create_table.sql;
```

### Generate Product CSV

```bash
python generate_products.py
```

### Generate Embeddings and Insert Data

```bash
python embed_products.py
```

---

## Optional: Local Search Test

Add this at the bottom of `lambda_handler.py`:

```python
if __name__ == "__main__":
    result = lambda_handler({"query": "Apple iPhone 14"}, None)
    import json
    print(json.dumps(result, indent=2))
```

Run:

```bash
python lambda_handler.py
```

---

## AWS Lambda Deployment (Optional)

- Upload `lambda_handler.py` as Lambda function
- Package dependencies using Lambda Layer or ZIP
- Set environment variables:

```
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
```

Test event:

```json
{ "query": "Nike Shoes" }
```

---

## Vector Similarity Logic

### Embedding Method
TF-IDF (token-based vectorization)

### Similarity Metric
Cosine similarity:

```
similarity = (A · B) / (|A| * |B|)
```

---

## Edge Case Handling

| Case | Behavior |
|------|----------|
| Similar names | High similarity |
| Typos | Lower similarity |
| Empty query | Returns statusCode 400 |
| Empty DB | Returns empty list |
| Zero vector | Similarity returns 0 |

---

## Limitations

- TF-IDF does not capture semantic meaning
- Not suitable for large-scale semantic search
- Can be upgraded using Sentence-BERT, OpenAI Embeddings, FAISS, etc.

---

## Deliverables Summary

- generate_products.py
- embed_products.py
- lambda_handler.py
- create_table.sql
- README.md

---

## Conclusion

This project demonstrates:
- Synthetic data generation
- NLP embedding pipeline
- Vector similarity search
- Database-backed ML workflow
- Serverless-ready architecture

Provides a foundation for search & recommendation systems.

