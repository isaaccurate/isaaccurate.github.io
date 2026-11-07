---
title: Excavate
description: "A retrieval-augmented generation (RAG) tool deployed on AWS Lambda. It combines keyword and vector search over selected Obsidian notes and generates answers with citations to the source notes and sections."
category: NLP / Information Retrieval
order: 3
stack: [Python, FastAPI, "Hybrid Search (BM25 + FAISS)", AWS Lambda, DynamoDB]
visual: language
visual_label: NOTE RETRIEVAL WORKFLOW
flow: "Notes → Search → Cited Answer"
repository: https://github.com/isaaccurate/Excavate
---
