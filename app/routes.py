from fastapi import APIRouter, HTTPException, Query
import subprocess
import asyncio
import os, re

# Create a router for the interactsh endpoints
router = APIRouter()

# Path to the file where the interactsh-client output will be stored
interactsh_payload_file_path = 'interactsh_payload.txt'

def start_interactsh_client_in_background():
    # Start the interactsh-client with the -ps option in the background
    with open(interactsh_payload_file_path, 'w') as outfile:
        subprocess.Popen(['./interactsh-client', '-ps', '-v', '-o', 'interactsh-logs.txt'], stdout=outfile, stderr=subprocess.STDOUT)

async def read_payload_url_from_file():
    # Wait for the file to be populated
    await asyncio.sleep(5)  # Wait time to ensure the file has been written by the background process
    if not os.path.exists(interactsh_payload_file_path):
        raise HTTPException(status_code=500, detail="interactsh payload file not found")
    try:
        with open(interactsh_payload_file_path, 'r') as file:
            url = file.read().strip()
            return url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading interactsh payload file: {e}")

@router.get("/getURL")
async def get_url():
    start_interactsh_client_in_background()
    # Read the URL from the file after giving some time for the background process to write it
    url = await read_payload_url_from_file()
    if url:
        return {"url": url}
    else:
        raise HTTPException(status_code=500, detail="Failed to retrieve interactsh URL")

# Path to the log file where interactions are stored
interactsh_logs_file_path = 'interactsh-logs.txt'

async def get_interactions_from_file(url: str):
    if not os.path.exists(interactsh_logs_file_path):
        raise HTTPException(status_code=500, detail="Interactsh log file not found")
    try:
        interactions = []
        # Extract the identifier from the URL
        identifier = url.split('.')[0]  # Assuming the URL is in the format: identifier.oast.site
        with open(interactsh_logs_file_path, 'r') as file:
            for line in file:
                # Modify the check to match the line format including the identifier
                if identifier in line and "Received HTTP interaction from" in line:
                    # Parse the IP address and timestamp from the line
                    match = re.search(r"\] Received HTTP interaction from ([\d\.]+) at ([\d\- :]+)", line)
                    if match:
                        interaction = f"Received HTTP interaction from {match.group(1)} at {match.group(2)}"
                        interactions.append(interaction)
        return interactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading interactsh log file: {e}")

@router.get("/getInteractions")
async def get_interactions(url: str = Query(..., description="URL of the testing server to fetch interactions for")):
    interactions = await get_interactions_from_file(url)
    if interactions:
        return {"interactions": interactions}
    else:
        return {"message": "No interactions found for the specified URL"}