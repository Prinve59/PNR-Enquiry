from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pnr_checker import get_pnr_status

app = FastAPI(title="PNR Status API")

class PNRResponse(BaseModel):
    pnr: str
    train_name: str = None
    train_number: str = None
    status: str = None
    station: str = None

@app.get("/")
def root():
    return {"message": "PNR Status API", "usage": "/pnr/{pnr_number}"}

@app.get("/pnr/{pnr_number}", response_model=PNRResponse)
def check_pnr(pnr_number: str):
    try:
        result = get_pnr_status(pnr_number)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
