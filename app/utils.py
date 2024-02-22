import subprocess
import asyncio
import os
import re
from datetime import datetime
from fastapi import HTTPException

interactsh_payload_file_path = 'interactsh_payload.txt'
interactsh_logs_file_path = 'interactsh-logs.txt'

def start_interactsh_client_in_background():
    with open(interactsh_payload_file_path, 'w') as outfile:
        subprocess.Popen(['./interactsh-client', '-ps', '-v', '-o', 'interactsh-logs.txt'], stdout=outfile, stderr=subprocess.STDOUT)

async def read_payload_url_from_file():
    await asyncio.sleep(5)
    if not os.path.exists(interactsh_payload_file_path):
        raise HTTPException(status_code=500, detail="interactsh payload file not found")
    try:
        with open(interactsh_payload_file_path, 'r') as file:
            return file.read().strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading interactsh payload file: {e}")

def parse_timestamp(timestamp_str):
    return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

async def get_interactions_from_file(url: str, start_timestamp: str = None, end_timestamp: str = None):
    if not os.path.exists(interactsh_logs_file_path):
        raise HTTPException(status_code=500, detail="Interactsh log file not found")
    
    start_dt = parse_timestamp(start_timestamp) if start_timestamp else None
    end_dt = parse_timestamp(end_timestamp) if end_timestamp else None

    interactions = []
    identifier = url.split('.')[0]
    with open(interactsh_logs_file_path, 'r') as file:
        for line in file:
            if identifier in line and "Received HTTP interaction from" in line:
                match = re.search(r"\] Received HTTP interaction from ([\d\.]+) at ([\d\- :]+)", line)
                if match:
                    interaction_dt = parse_timestamp(match.group(2))
                    if (not start_dt or interaction_dt >= start_dt) and (not end_dt or interaction_dt <= end_dt):
                        interactions.append(f"Received HTTP interaction from {match.group(1)} at {match.group(2)}")
    return interactions
