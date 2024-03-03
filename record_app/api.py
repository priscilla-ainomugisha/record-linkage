from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from typing import List
from .notebook_logic import clean_data, merge_datasets, search_patients, names_match, Patient
from django.shortcuts import render  # Assuming you're integrating with Django

app = FastAPI()

# Define FastAPI endpoints

@app.post("/clean_data")
def clean_data_endpoint(df1: List[Patient], df2: List[Patient]):
    df1_cleaned = clean_data(df1)
    df2_cleaned = clean_data(df2)

    return {"df1_cleaned": df1_cleaned, "df2_cleaned": df2_cleaned}

@app.post("/merge_datasets")
def merge_datasets_endpoint(df1: List[Patient], df2: List[Patient]):
    df1_cleaned = clean_data(df1)
    df2_cleaned = clean_data(df2)

    merged_dataset = merge_datasets(df1_cleaned, df2_cleaned)

    return {"merged_dataset": merged_dataset}

@app.post("/search_patients")
def search_patients_endpoint(search_name: str, df1: List[Patient], df2: List[Patient]):
    df1_cleaned = clean_data(df1)
    df2_cleaned = clean_data(df2)

    # Define identifier fields
    identifier_fields = [
        {"key": "firstname", "match_prob": 0.90, "unmatch_prob": 0.10},
        {"key": "lastname", "match_prob": 0.95, "unmatch_prob": 0.01},
        {"key": "dob", "match_fn": names_match, "match_prob": 0.90, "unmatch_prob": 0.10},
        {"key": "sex", "match_prob": 0.95, "unmatch_prob": 0.05}
    ]

    result = search_patients(search_name, df1_cleaned, df2_cleaned, identifier_fields)

    return {"result": result}

@app.post("/home", response_class=HTMLResponse)  # Set response class to HTMLResponse
def home(request: Request):
    if request.method == 'GET':
        # Handle POST requests if needed
        pass
    else:
        # Render the index.html template for GET requests
        return render(request, 'index.html')
