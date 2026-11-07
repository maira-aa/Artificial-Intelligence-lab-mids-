
import csv
import json
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from lab_6_task2_chunks import make_chunks

with open("corpus.json", "r", encoding="utf-8") as file:
    documents = json.load(file)

with open("queries.json", "r", encoding="utf-8") as file:
    queries = json.load(file)

model_start = time.time()
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    device="cpu"
)
model_load_time = time.time() - model_start

strategies = ["0", "10", "sentence"]
backends = ["tfidf", "embedding"]

all_results = []
summary_results = []

for strategy in strategies:
    chunks = make_chunks(documents, strategy)
    texts = [chunk["text"] for chunk in chunks]

    for backend in backends:
        encode_start = time.time()

        if backend == "tfidf":
            vectorizer = TfidfVectorizer()
            chunk_vectors = vectorizer.fit_transform(texts)
        else:
            chunk_vectors = model.encode(
                texts,
                normalize_embeddings=True
            )

        encode_time = time.time() - encode_start
        search_time = 0
        query_results = []

        print("\n" + "=" * 65)
        print("Strategy:", strategy, "| Backend:", backend)

        for item in queries:
            question = item["query"]
            expected_doc = item["doc"]
            evidence = item["evidence"]
            split = item["split"]

            query_start = time.time()

            if backend == "tfidf":
                query_vector = vectorizer.transform([question])
                scores = cosine_similarity(
                    query_vector,
                    chunk_vectors
                )[0]
            else:
                query_vector = model.encode(
                    [question],
                    normalize_embeddings=True
                )
                scores = query_vector @ chunk_vectors.T
                scores = scores[0]

            search_time += time.time() - query_start

            top_indices = np.argsort(-scores)[:3]
            relevant_rank = 0

            print("\nQuery:", question)
            print("Split:", split)

            for rank, index in enumerate(top_indices, start=1):
                chunk = chunks[index]
                chunk_text = chunk["text"]

                relevant = bool(
                    expected_doc is not None
                    and chunk["doc"] == expected_doc
                    and evidence is not None
                    and evidence in chunk_text
                )

                if relevant and relevant_rank == 0:
                    relevant_rank = rank

                print(
                    "Rank:", rank,
                    "| ID:", chunk["id"],
                    "| Document:", chunk["doc"],
                    "| Score:", round(float(scores[index]), 4),
                    "| Offsets:", chunk["start"], chunk["end"]
                )
                print("Evidence:", chunk_text)

                all_results.append({
                    "strategy": strategy,
                    "backend": backend,
                    "split": split,
                    "query": question,
                    "rank": rank,
                    "chunk_id": chunk["id"],
                    "document_id": chunk["doc"],
                    "score": round(float(scores[index]), 4),
                    "start": chunk["start"],
                    "end": chunk["end"],
                    "relevant": int(relevant),
                    "retrieved_text": chunk_text
                })

            hit = int(relevant_rank > 0)
            reciprocal_rank = (
                1 / relevant_rank if relevant_rank > 0 else 0
            )

            query_results.append({
                "split": split,
                "answerable": expected_doc is not None,
                "hit": hit,
                "reciprocal_rank": reciprocal_rank,
                "top_score": float(scores[top_indices[0]])
            })

        for split in ["dev", "test"]:
            answerable = [
                result for result in query_results
                if result["split"] == split and result["answerable"]
            ]

            unanswerable = [
                result for result in query_results
                if result["split"] == split and not result["answerable"]
            ]

            hit_at_3 = (
                sum(result["hit"] for result in answerable)
                / len(answerable)
                if answerable else 0
            )

            mrr_at_3 = (
                sum(result["reciprocal_rank"] for result in answerable)
                / len(answerable)
                if answerable else 0
            )

            print("\n", split.upper(), "RESULTS")
            print("Answerable queries:", len(answerable))
            print("Hit@3:", round(hit_at_3, 4))
            print("MRR@3:", round(mrr_at_3, 4))

            if unanswerable:
                print("Unanswerable queries:", len(unanswerable))
                for result in unanswerable:
                    print(
                        "Top score for unanswerable query:",
                        round(result["top_score"], 4)
                    )

            summary_results.append({
                "strategy": strategy,
                "backend": backend,
                "split": split,
                "hit_at_3": round(hit_at_3, 4),
                "mrr_at_3": round(mrr_at_3, 4),
                "chunk_count": len(chunks),
                "encode_time": round(encode_time, 4),
                "search_time": round(search_time, 4),
                "model_load_time": round(model_load_time, 4)
            })

with open("retrieval_log.csv", "w", newline="", encoding="utf-8") as file:
    fields = [
        "strategy", "backend", "split", "query", "rank",
        "chunk_id", "document_id", "score", "start", "end",
        "relevant", "retrieved_text"
    ]
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(all_results)

print("\n" + "=" * 65)
print("FINAL COMPARISON")

for result in summary_results:
    print(result)

print("\nModel loading time:", round(model_load_time, 4), "seconds")
print("Retrieval results saved in retrieval_log.csv")
