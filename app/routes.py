from fastapi import APIRouter, Query
from . import utils  # Adjust the import based on your project structure

router = APIRouter()

@router.get("/getURL")
async def get_url():
    utils.start_interactsh_client_in_background()
    url = await utils.read_payload_url_from_file()
    if url:
        return {"url": url}
    else:
        return {"message": "Failed to retrieve interactsh URL"}

@router.get("/getInteractions")
async def get_interactions(url: str = Query(...),
                           start_timestamp: str = Query(None),
                           end_timestamp: str = Query(None)):
    interactions = await utils.get_interactions_from_file(url, start_timestamp, end_timestamp)
    if interactions:
        return {"interactions": interactions}
    else:
        return {"message": "No interactions found for the specified URL within the given timestamp range"}
