# Architecture Diagrams

---

# 1. Overall System Architecture

```mermaid
flowchart LR

subgraph Client
    UI["React Frontend"]
end

subgraph Backend
    API["FastAPI Backend"]
    Auth["Authentication"]
    Chat["Chat API"]
end

subgraph AI
    Retriever["Semantic Retriever"]
    Context["Context Builder"]
    LLM["LLM"]
end

subgraph Workers
    Clone["Repository Cloner"]
    Parser["Parser & Chunker"]
    Embed["Embedding Generator"]
end

subgraph Storage
    PG[("PostgreSQL")]
    Vector[("ChromaDB")]
end

GitHub[("GitHub Repository")]

UI --> API
API --> Auth
API --> Chat

Chat --> Retriever
Retriever --> Vector
Retriever --> Context
Context --> LLM
LLM --> Chat

GitHub --> Clone
Clone --> Parser
Parser --> Embed
Embed --> Vector
Parser --> PG

API --> PG
```

---

# 2. Repository Indexing Pipeline

```mermaid
flowchart LR

Repo["GitHub Repository"]
-->Clone["Clone Repository"]
-->Traverse["Traverse Files"]

Traverse
-->Parser["Parse Source Code"]

Parser
-->Chunk["Chunk Generator"]

Chunk
-->Embedding["Generate Embeddings"]

Embedding
-->Vector[("ChromaDB")]

Parser
-->Metadata[("PostgreSQL Metadata")]
```

---

# 3. RAG Flow

```mermaid
flowchart LR

User["User"]

User
-->Query["Ask Question"]

Query
-->API["FastAPI"]

API
-->Retriever["Semantic Retriever"]

Retriever
-->Vector[("ChromaDB")]

Vector
-->Chunks["Relevant Code Chunks"]

Chunks
-->Context["Context Builder"]

Context
-->LLM["LLM"]

LLM
-->Answer["Grounded Response"]

Answer
-->User
```

---

# 4. Agent Interaction Diagram

```mermaid
flowchart TD

User["Developer"]

User
-->Router["Agent Router"]

Router
-->Search["Search Agent"]
Router
-->Explain["Explain Agent"]
Router
-->Analysis["Analysis Agent"]

Search --> Retriever
Explain --> Retriever
Analysis --> Retriever

Retriever["Retriever"]

Retriever
-->Vector[("Vector DB")]

Vector
-->Context["Context Builder"]

Context
-->LLM["LLM"]

LLM
-->Response["AI Response"]

Response
-->User
```

---

# 5. Database ER Diagram

```mermaid
erDiagram

REPOSITORY ||--o{ FILE : contains
FILE ||--o{ CODE_CHUNK : split_into
CODE_CHUNK ||--|| EMBEDDING : has
REPOSITORY ||--o{ CHAT_SESSION : owns
CHAT_SESSION ||--o{ MESSAGE : contains

REPOSITORY {
    uuid id
    string name
    string github_url
    datetime created_at
}

FILE {
    uuid id
    string path
    string language
    string checksum
}

CODE_CHUNK {
    uuid id
    uuid file_id
    int chunk_index
    text content
}

EMBEDDING {
    uuid id
    vector embedding
    string model
}

CHAT_SESSION {
    uuid id
    uuid repository_id
    datetime created_at
}

MESSAGE {
    uuid id
    uuid session_id
    string role
    text content
}
```

---

# 6. Worker Processing Pipeline

```mermaid
flowchart LR

Job["Repository Submitted"]

Job
-->Clone["Clone Worker"]

Clone
-->Parse["Parser Worker"]

Parse
-->Chunk["Chunk Worker"]

Chunk
-->Embed["Embedding Worker"]

Embed
-->Store["Storage Worker"]

Store
-->PG[("PostgreSQL")]

Store
-->Vector[("ChromaDB")]

Store
-->Ready["Repository Ready for Chat"]
```

---

# 7. System Sequence Diagram

```mermaid
sequenceDiagram

actor User

participant Frontend
participant API
participant Retriever
participant ChromaDB
participant LLM

User->>Frontend: Ask Question

Frontend->>API: POST /chat

API->>Retriever: Retrieve Context

Retriever->>ChromaDB: Similarity Search

ChromaDB-->>Retriever: Relevant Code Chunks

Retriever-->>API: Repository Context

API->>LLM: Prompt + Context

LLM-->>API: Generated Answer

API-->>Frontend: Response

Frontend-->>User: Display Answer
```
