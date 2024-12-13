from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llm import llm_entity_extraction, llm_rag
from chunking import (
    fetch_munich_wiki,
    chunk_text,
    create_faiss_index,
    similarity_search,
    load_faiss_index,
)
import json
import os

# Initialize FastAPI application
app = FastAPI()


# Define request model for patient details
class PatientRequest(BaseModel):
    patient_details: str


# Define request model for query data
class Data(BaseModel):
    query: str


@app.get("/")
async def health_check():
    """
    Basic health check endpoint to verify API is running.
    Returns a JSON response indicating the API status.
    """
    return {"status": "healthy", "message": "API is running"}


@app.post("/process-patient")
async def process_patient(request: PatientRequest):
    """Endpoint to process patient details using LLM for entity extraction."""
    try:
        # Extract medical entities from patient details
        result = llm_entity_extraction(request.patient_details)
        # Parse the JSON result
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        # Raise HTTP exception with error details
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/rag")
async def semantic_search(Query: Data):
    """Endpoint Semantic similarity."""
    try:
        # Define the path for the FAISS index
        faiss_index_path = "faiss_index"

        # Check if FAISS index exists, if not, create it
        if not os.path.exists(faiss_index_path):
            # Fetch Munich Wikipedia content
            wiki_text = fetch_munich_wiki()
            # Split the text into chunks
            chunks = chunk_text(wiki_text)
            # Create FAISS index from chunks
            create_faiss_index(chunks)

        # Load the FAISS index
        faiss_index = load_faiss_index(faiss_index_path)
        # Perform similarity search to find relevant context
        context = similarity_search(faiss_index, Query.query)
        # Generate response using LLM with the query and context
        result = llm_rag(Query.query, context)

        # Construct the response dictionary
        result_dict = {"response": result, "similar_context": context}
        return result_dict
    except Exception as e:
        # Raise HTTP exception with error details
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using Uvicorn server
    uvicorn.run(app, host="0.0.0.0", port=8000)
