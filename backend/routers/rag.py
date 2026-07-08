from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.rag import (
    ResumeRequest, ResumeResponse,
    JobSearchRequest, SemanticSearchResponse, SemanticSearchResult,
    JobMatchRequest, JobMatchResponse, JobMatchResult,
    RagSearchRequest, RagSearchResponse,
    EmbedResponse
)
from service.qdrant_service import embed_all_jobs, search_jobs, match_jobs_for_profile
from service.rag_service import rag_job_search
from service.resume_service import analyse_resume

router = APIRouter(prefix="/rag", tags=["RAG"])

@router.post("/embed-jobs", response_model=EmbedResponse, status_code=status.HTTP_200_OK)
def embed_jobs_endpoint(db: Session = Depends(get_db)):
    try:
        count = embed_all_jobs(db)
        return EmbedResponse(message="Jobs embedded successfully", count=count)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to embed jobs: {str(e)}"
        )

@router.post("/search", response_model=SemanticSearchResponse, status_code=status.HTTP_200_OK)
def semantic_search_endpoint(request: JobSearchRequest):
    try:
        results = search_jobs(request.query)
        mapped_results = [
            SemanticSearchResult(
                job_id=r["job_id"],
                title=r["title"],
                description=r["description"],
                salary=r["salary"],
                score=r["score"]
            )
            for r in results
        ]
        return SemanticSearchResponse(results=mapped_results)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Semantic search failed: {str(e)}"
        )

@router.post("/job-match", response_model=JobMatchResponse, status_code=status.HTTP_200_OK)
def match_jobs_endpoint(request: JobMatchRequest):
    try:
        results = match_jobs_for_profile(skills=request.skills, experience=request.experience)
        mapped_matches = [
            JobMatchResult(
                job_id=r["job_id"],
                title=r["title"],
                description=r["description"],
                salary=r["salary"],
                match_score=r["score"]
            )
            for r in results
        ]
        return JobMatchResponse(matches=mapped_matches)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Job matching failed: {str(e)}"
        )

@router.post("/ask", response_model=RagSearchResponse, status_code=status.HTTP_200_OK)
def rag_query_endpoint(request: RagSearchRequest):
    try:
        answer = rag_job_search(request.question)
        return RagSearchResponse(answer=answer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"RAG search query failed: {str(e)}"
        )

@router.post("/analyse-resume", response_model=ResumeResponse, status_code=status.HTTP_200_OK)
def analyse_resume_endpoint(request: ResumeRequest):
    try:
        analysis = analyse_resume(request.resume_text)
        return ResumeResponse(analysis=analysis)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Resume analysis failed: {str(e)}"
        )
