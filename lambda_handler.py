import json
import numpy as np
import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer

def cosine_similarity(a, b):
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def lambda_handler(event, context):
    
    # Validate query input
    query_product = event.get("query")
    if not query_product:
        return {
            "statusCode": 400,
            "message": "Missing required field: 'query'"
        }

    # Local MySQL connection -------------------------------
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishwas@2003",
            database="vector_db"
        )
        cursor = db.cursor(dictionary=True)
    except Exception as e:
        return {
            "statusCode": 500,
            "message": f"Database connection failed: {str(e)}"
        }

    try:
        # Fetch all product records
        cursor.execute("SELECT product_id, product_name FROM products_vectors")
        rows = cursor.fetchall()

        if not rows:
            return {
                "statusCode": 200,
                "results": [],
                "message": "No products found in database."
            }

        # TF-IDF embedding
        names = [row['product_name'] for row in rows] + [query_product]
        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform(names).toarray()

        query_vector = tfidf[-1]
        results = []

        # Cosine similarity calculation
        for i, row in enumerate(rows):
            product_vector = tfidf[i]
            score = cosine_similarity(query_vector, product_vector)
            results.append({
                "product_id": row['product_id'],
                "product_name": row['product_name'],
                "score": float(score)
            })

        # Sort & return top 5
        results = sorted(results, key=lambda x: x["score"], reverse=True)[:5]

        return {
            "statusCode": 200,
            "results": results
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "message": f"Similarity computation error: {str(e)}"
        }

    finally:
        cursor.close()
        db.close()

if __name__ == "__main__":
    result = lambda_handler({"query": "Apple iPhone 14"}, None)
    print(json.dumps(result, indent=2))