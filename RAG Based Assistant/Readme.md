# 📚 RAG-Based AI Teaching Assistant

An AI-powered Teaching Assistant built using **Retrieval-Augmented Generation (RAG)** that can answer questions from custom video-based learning content.

This project converts video lectures into searchable knowledge and uses embeddings + LLMs to generate accurate, context-aware responses.

---

## 🚀 Project Overview

This system enables users to interact with their own learning materials by asking questions in natural language. The assistant retrieves relevant content from processed lecture data and generates meaningful answers using an LLM.

---

## ⚙️ Pipeline Architecture

The project follows a structured pipeline:

### 1. 🎥 Data Collection
- Store all lecture videos inside the `videos/` directory.

### 2. 🔊 Audio Extraction
- Convert video files to `.mp3` format using:
  ```bash
  video_to_mp3.py

### 3. 📝 Speech-to-Text Conversion
- Convert .mp3 files into structured .json transcripts:
  ```bash
  mp3_to_json.py

### 4. 🧠 Embedding Generation
- Process JSON transcripts into vector embeddings.
- Store embeddings in a DataFrame and save as a .joblib file:
    ```bash
    embedding_gen.py

### 5. 🤖 RAG-based Question Answering
- Load embeddings into memory.
- Retrieve relevant chunks based on user query.
- Generate contextual responses using an LLM.


### 🧩 Tech Stack
- Python
- NLP & Embeddings
- Vector Similarity (Cosine Similarity)
- Joblib (for storage)
- LLM (via API/local model)
- Speech-to-Text processing

### 💡 Key Features
- Converts video lectures → searchable knowledge base
- Implements Retrieval-Augmented Generation (RAG)
- Efficient semantic search using embeddings
- Context-aware response generation
- Modular and scalable pipeline

### 📌 Use Cases
- Personal AI tutor for course material
- Knowledge assistant for recorded lectures
- Internal training assistant for organizations

### 📊 Future Improvements
- Add UI (Streamlit / Web App)
- Use vector databases (FAISS, Pinecone)
- Improve chunking & retrieval strategies
- Add multi-modal support (PDFs, notes)

### 🏁 Conclusion

- This project demonstrates how RAG can be applied to transform passive learning content into an interactive AI assistant, enabling smarter and more efficient learning experiences.
    

