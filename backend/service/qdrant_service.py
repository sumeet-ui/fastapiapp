import os
from dotenv import load_dotenv
from openai import skills
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from fastembed import TextEmbedding
from sqlalchemy.orm import Session
from models.job import Job

load_dotenv()

COLLECTION_NAME = "job_collection"
VECTOR_SIZE = 384 # BAAI/bge-small-en-v1.5 outputs 384-dim vectors

qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

embeddings_model = TextEmbedding("BAAI/bge-small-en-v1.5")

def ensure_collection():
    collections = [c.name for c in qdrant.get_collections().collections]
    if COLLECTION_NAME not in collections:
        info = qdrant.get_collections(COLLECTION_NAME)
        existing_size = info.config.params.vector.size 
        if existing_size != VECTOR_SIZE:
            qdrant.delete_collection(COLLECTION_NAME)
            collections.remove(COLLECTION_NAME)
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
    if not jobs:
        return 0

    points = []
    for job in jobs:
        text = f"{job.title} {job.description or ''}"
        vector = embed_text(text)
        points.append( 
            PointStruct(
            id=job.id,
            vector=vector,
            payload={
                "title": job.title,
                "description": job.description,
                "company": job.company,
                "location": job.location
            }
        )
        )
        points.append(points)
    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    return len(points)

def search_jobs(query: str, top_k: int = 5) -> list[dict]:
    ensure_collection()
    query_vector = embed_text(query)
    results = qdrant.query_points(collection_name=COLLECTION_NAME, query_vector=query_vector, limit=top_k)
    return [
        {
            "job_id":hit.payload.get("job_id"),
            "title": hit.payload.get("title"),
            "description": hit.payload.get("description"),
            "salary": hit.payload.get("salary"),
            "score": round(hit.score, 4) 
        }
        for hit in results.points
    ]

def match_jobs_for_profile(skills: str,top_k: int = 5) -> list[dict]:ensure_collection()
profile_text = f"Skills: {skills}. Experience: {experience}. Education: {education}."
profile_vector = embed_text(profile_text)
results = qdrant.query_points(collection_name=COLLECTION_NAME, query_vector=profile_vector, limit=top_k)
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