from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
import pandas as pd
import io
import json

from enrichment import clean_and_enrich_leads
from scoring import score_lead, segment

app = FastAPI()


@app.post("/enrich")
async def enrich(file: UploadFile = File(...)):
    # 1. Load CSV from upload
    df = pd.read_csv(file.file)

    # 2. Clean + enrich leads
    df = clean_and_enrich_leads(df)

    # 3. Optional ICP scoring (safe if no ICP provided later)
    try:
        with open("icp.json") as f:
            icp = json.load(f)

        df["ICP_Score"] = df.apply(lambda r: score_lead(r, icp), axis=1)
        df["Segment"] = df["ICP_Score"].apply(segment)

    except FileNotFoundError:
        df["ICP_Score"] = None
        df["Segment"] = None

    # 4. Return enriched CSV
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)

    return Response(
        content=buffer.getvalue(),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=enriched.csv"
        }
    )


@app.get("/health")
def health():
    return {"status": "alive"}
