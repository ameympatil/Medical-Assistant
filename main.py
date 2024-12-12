from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llm import llm_request  # Assuming this is the function in llm.py

app = FastAPI()


class PatientRequest(BaseModel):
    patient_details: str


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
        result = llm_request(request.patient_details)
        # result = "Yess success!!!"
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
