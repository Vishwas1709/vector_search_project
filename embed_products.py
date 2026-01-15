import pandas as pd
import json
import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("products.csv")

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["product_name"])

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vishwas@2003",
    database="vector_db"
)
cursor = db.cursor()

for i, row in df.iterrows():
    vector = X[i].toarray().tolist()[0]
    query = "INSERT INTO products_vectors (product_id, product_name, vector) VALUES (%s, %s, %s)"
    cursor.execute(query, (int(row['product_id']), row['product_name'], json.dumps(vector)))

db.commit()
cursor.close()
db.close()

print("Embedding generation and DB insert completed!")
