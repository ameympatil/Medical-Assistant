from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llm import llm_entity_extraction, llm_rag
from chunking import (
    fetch_munich_wiki,
    chunk_text,
    create_faiss_index,
    similarity_search,
    load_faiss_index
)
import json
import os

app = FastAPI()


class PatientRequest(BaseModel):
    patient_details: str


class Data(BaseModel):
    query: str


@app.get("/")
async def health_check():
    """
    Basic health check endpoint to verify API is running
    """
    return {"status": "healthy", "message": "API is running"}


@app.post("/process-patient")
async def process_patient(request: PatientRequest):
    """
    Endpoint to process patient details using LLM
    """
    try:
        result = llm_entity_extraction(request.patient_details)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/rag")
async def semantic_search(Query: Data):
    """
    Endpoint to process patient details using LLM
    """
    try:
        # Check if FAISS index is present in the directory
        faiss_index_path = "faiss_index"
        if not os.path.exists(faiss_index_path):
            # Fetch Munich Wikipedia content
            wiki_text = fetch_munich_wiki()
            # Chunk the text
            chunks = chunk_text(wiki_text)
            # Create FAISS index
            create_faiss_index(chunks)

        # Load the FAISS index
        faiss_index = load_faiss_index(faiss_index_path)
        context = similarity_search(faiss_index, Query.query)
        result = llm_rag(Query.query,context)
        result_dict = {
            "response":result,
            "similar_context":context
        }
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
