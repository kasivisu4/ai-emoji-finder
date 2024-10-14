from typing import Union
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import os
import pandas as pd

load_dotenv()


import requests

app = FastAPI()

emojis_df = pd.read_csv("emojis.csv", names=["value","key"], header=None)



bearer_token = os.getenv("BEARER_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L12-v2"
headers = {"Authorization": f"Bearer {bearer_token}"}


@app.get("/")
def read_root():
    return {"Hello": "World"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()


@app.get("/search")
def search(description: str):
    # Prepare the request data
    request_data = {
        "inputs": {
            "source_sentence": description,
            "sentences": emojis_df["key"].to_list()
        }
    }

    try:
        # Send the request to the API        	
        predictions = query({
            "inputs": {
            "source_sentence": description,
            "sentences": emojis_df["key"].to_list()
        },
        })
        
        # Ensure predictions is a list of the same length as the number of sentences
        if not isinstance(predictions, list) or len(predictions) != len(emojis_df):
            raise ValueError("Invalid predictions received from the API.")

        # Add predictions to the DataFrame
        emojis_df["predictions"] = predictions
        
        # Get the top 5 values based on predictions
        top_5_indices = emojis_df["predictions"].nlargest(5).index
        resp = emojis_df.loc[top_5_indices, "value"].tolist()  # Convert to list for response
        
        return {"top_values": resp}
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")
    except ValueError as ve:
        raise HTTPException(status_code=500, detail=str(ve))
     

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=True)