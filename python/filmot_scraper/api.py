from fastapi import FastAPI
from scraper import fetch_filmot_data

app = FastAPI()

@app.get("/search/")
def search_filmot(query: str, duration: int = 300):
    try:
        results = fetch_filmot_data(query, duration)
        return {"status": "success", "data": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}