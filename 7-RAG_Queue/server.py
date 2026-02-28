from fastapi import FastAPI, Query
from .client.rq_client import queue 
from .queues.worker import process_query

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the RAG Queue API!"}

@app.post("/chat")
def chat_with_rag(
    query: str = Query(..., description="The user's query to be processed by the RAG system")
):
    # Enqueue the query to be processed by the worker
    job = queue.enqueue(process_query, query)
    return {"status": "queued", "job_id": job.id}  


@app.get("/job-status")
def get_result(job_id: str = Query(..., description="The ID of the job to check the status and retrieve the result")):
    job = queue.fetch_job(job_id)
    if job is None:
        return {"status": "not found"}
    elif job.is_finished:
        return {"status": "finished", "result": job.result}
    elif job.is_failed:
        return {"status": "failed", "error": str(job.exc_info)}
    else:
        return {"status": "in progress"}
