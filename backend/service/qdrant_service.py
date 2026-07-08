import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from fastembed import TextEmbedding
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.job import Job

load_dotenv()

COLLECTION_NAME = "job_collection"
VECTOR_SIZE = 384  # BAAI/bge-small-en-v1.5 outputs 384-dim vectors

try:
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")
    if url and api_key and api_key.strip():
        qdrant = QdrantClient(url=url, api_key=api_key.strip(), timeout=5)
        # Test connection
        qdrant.get_collections()
        print("Connected to Qdrant Cloud successfully.")
    else:
        raise ValueError("Missing Qdrant Cloud config")
except Exception as e:
    print(f"Failed to connect to Qdrant Cloud ({e}), falling back to local persistent Qdrant.")
    try:
        qdrant = QdrantClient(path="qdrant_local_db")
    except Exception as e2:
        print(f"Failed to initialize local persistent Qdrant ({e2}), falling back to in-memory Qdrant.")
        qdrant = QdrantClient(location=":memory:")


embeddings_model = TextEmbedding("BAAI/bge-small-en-v1.5")

def ensure_collection():
    try:
        collections = [c.name for c in qdrant.get_collections().collections]
    except Exception:
        collections = []
    
    if COLLECTION_NAME not in collections:
        qdrant.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
        )

def embed_text(text: str) -> list[float]:
    return next(embeddings_model.embed([text])).tolist()

def embed_all_jobs(db: Session) -> int:
    ensure_collection()
    jobs = db.query(Job).all()
    
async def embed_all_jobs_async(db: AsyncSession) -> int:
    ensure_collection()
    result =await db.execute(select(Job))
    jobs = result.scalars().all()
    if not jobs:
        return 0

    points = []
    for job in jobs:
        text = f"{job.title} {job.description or ''}"
        vector = embed_text(text)
        
        company_name = job.company.name if (job.company and hasattr(job.company, 'name')) else ""
        points.append(
            PointStruct(
                id=job.id,
                vector=vector,
                payload={
                    "job_id": job.id,
                    "title": job.title,
                    "description": job.description,
                    "salary": job.salary,
                    "company": company_name
                }
            )
        )
    if points:
        qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
    return len(points)

def search_jobs(query: str, top_k: int = 5) -> list[dict]:
    ensure_collection()
    query_vector = embed_text(query)
    results = qdrant.query_points(collection_name=COLLECTION_NAME, query=query_vector, limit=top_k)
    return [
        {
            "job_id": hit.payload.get("job_id"),
            "title": hit.payload.get("title"),
            "description": hit.payload.get("description"),
            "salary": hit.payload.get("salary"),
            "score": round(hit.score, 4)
        }
        for hit in results.points
    ]

def match_jobs_for_profile(skills: str, experience: str = "", education: str = "", top_k: int = 5) -> list[dict]:
    ensure_collection()
    profile_text = f"Skills: {skills}. Experience: {experience}. Education: {education}."
    profile_vector = embed_text(profile_text)
    results = qdrant.query_points(collection_name=COLLECTION_NAME, query=profile_vector, limit=top_k)
    return [
        {
            "job_id": hit.payload.get("job_id"),
            "title": hit.payload.get("title"),
            "description": hit.payload.get("description"),
            "salary": hit.payload.get("salary"),
            "score": round(hit.score, 4)
        }
        for hit in results.points
    ]