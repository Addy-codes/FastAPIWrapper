# from fastapi import APIRouter, HTTPException, Query
# import subprocess
# import asyncio
# import os, re
# from datetime import datetime

# # Create a router for the interactsh endpoints
# router = APIRouter()

# # Path to the file where the interactsh-client output will be stored
# interactsh_payload_file_path = 'interactsh_payload.txt'

# def start_interactsh_client_in_background():
#     # Start the interactsh-client with the -ps option in the background
#     with open(interactsh_payload_file_path, 'w') as outfile:
#         subprocess.Popen(['./interactsh-client', '-ps', '-v', '-o', 'interactsh-logs.txt'], stdout=outfile, stderr=subprocess.STDOUT)

# async def read_payload_url_from_file():
#     # Wait for the file to be populated
#     await asyncio.sleep(5)  # Wait time to ensure the file has been written by the background process
#     if not os.path.exists(interactsh_payload_file_path):
#         raise HTTPException(status_code=500, detail="interactsh payload file not found")
#     try:
#         with open(interactsh_payload_file_path, 'r') as file:
#             url = file.read().strip()
#             return url
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error reading interactsh payload file: {e}")

# @router.get("/getURL")
# async def get_url():
#     start_interactsh_client_in_background()
#     # Read the URL from the file after giving some time for the background process to write it
#     url = await read_payload_url_from_file()
#     if url:
#         return {"url": url}
#     else:
#         raise HTTPException(status_code=500, detail="Failed to retrieve interactsh URL")

# # Path to the log file where interactions are stored
# interactsh_logs_file_path = 'interactsh-logs.txt'

# def parse_timestamp(timestamp_str):
#     # Adjust the format according to how timestamps are formatted in your log files
#     return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

# async def get_interactions_from_file(url: str, start_timestamp: str = None, end_timestamp: str = None):
#     if not os.path.exists(interactsh_logs_file_path):
#         raise HTTPException(status_code=500, detail="Interactsh log file not found")
    
#     start_dt = parse_timestamp(start_timestamp) if start_timestamp else None
#     end_dt = parse_timestamp(end_timestamp) if end_timestamp else None

#     try:
#         interactions = []
#         identifier = url.split('.')[0]
#         with open(interactsh_logs_file_path, 'r') as file:
#             for line in file:
#                 if identifier in line and "Received HTTP interaction from" in line:
#                     match = re.search(r"\] Received HTTP interaction from ([\d\.]+) at ([\d\- :]+)", line)
#                     if match:
#                         interaction_dt = parse_timestamp(match.group(2))
#                         if (not start_dt or interaction_dt >= start_dt) and (not end_dt or interaction_dt <= end_dt):
#                             interaction = f"Received HTTP interaction from {match.group(1)} at {match.group(2)}"
#                             interactions.append(interaction)
#         return interactions
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error reading interactsh log file: {e}")

# @router.get("/getInteractions")
# async def get_interactions(url: str = Query(..., description="URL of the testing server to fetch interactions for"),
#                            start_timestamp: str = Query(None, description="Start of the timestamp range (inclusive)"),
#                            end_timestamp: str = Query(None, description="End of the timestamp range (inclusive)")):
#     interactions = await get_interactions_from_file(url, start_timestamp, end_timestamp)
#     if interactions:
#         return {"interactions": interactions}
#     else:
#         return {"message": "No interactions found for the specified URL within the given timestamp range"}

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
