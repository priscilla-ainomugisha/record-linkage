
# Define functions for notebook logic

from .models import SyntheticFacilityV3,SyntheticHdssV3
import pandas as pd

from django.db import models

class Patient(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    petname = models.CharField(max_length=255)
    dob = models.DateField()
    sex = models.CharField(max_length=10)
    

def clean_data():
    # Fetch data from Django models
    df1_queryset = SyntheticFacilityV3.objects.all()
    df2_queryset = SyntheticHdssV3.objects.all()

    # Convert querysets to pandas DataFrames
    df1 = pd.DataFrame(list(df1_queryset.values()))
    df2 = pd.DataFrame(list(df2_queryset.values()))

    # Cleaning the datasets

    # Edit the formulation of dob
    df1['dob'] = pd.to_datetime(df1['dob'], errors='coerce')

    # Change the format of date in column dob to 9/9/1930
    df1['dob'] = df1['dob'].dt.strftime('%d/%m/%Y')

    # Formatting the visit date
    df1['visitdate'] = pd.to_datetime(df1['visitdate'], errors='coerce')
    df1['visitdate'] = df1['visitdate'].dt.strftime('%d/%m/%Y')

    # Check columns with null values
    null_columns = df1.isnull().any()
    columns_with_nulls = null_columns[null_columns]
    print("Columns with null values")
    print(columns_with_nulls)

    # Remove leading spaces in first name and last name columns
    df1['firstname'] = df1['firstname'].str.strip()
    df1['lastname'] = df1['lastname'].str.strip()

    return df1

def merge_datasets(df1, df2):
    # Merge the two datasets on the common column 'firstname'
    common_dataset = pd.merge(df1, df2, on='firstname', how='inner')

    # Drop duplicates based on the common column
    common_dataset.drop_duplicates(subset='firstname', inplace=True)

    # Reset index
    common_dataset.reset_index(drop=True, inplace=True)

    return common_dataset


"""# Fellegi Sunter

### Probabilistic machine learning approach
"""

import math
from metaphone import doublemetaphone
import pandas as pd



def default_match_fn(a, b):
    """
    Default function for determining if two values are a match.
    """
    if isinstance(a, str) and isinstance(b, str):
        return a.lower() == b.lower()
    else:
        return a == b

def names_match(name_a, name_b):
    """
    Do name_a or name_b share any matching phonetic values via double-metaphone?
    """
    if pd.isna(name_a) or pd.isna(name_b):
        return False  # Handle NaN values, consider them as not matching
    else:
        metaphones_a = doublemetaphone(name_a)
        metaphones_b = doublemetaphone(name_b)
        return any(m_a == m_b for m_a in metaphones_a for m_b in metaphones_b)

identifier_fields = [
    {"key": "firstname", "match_prob": 0.90, "unmatch_prob": 0.10},
    {"key": "lastname", "match_prob": 0.95, "unmatch_prob": 0.01},
    {"key": "petname", "match_fn": names_match, "match_prob": 0.60, "unmatch_prob": 0.20},
    {"key": "dob", "match_fn": names_match, "match_prob": 0.90, "unmatch_prob": 0.10},
    {"key": "sex", "match_prob": 0.95, "unmatch_prob": 0.05}
]

def compare_patients(patient_a, patient_b, identifier_fields):
    # Compare two patients and return a match score using the Fellegi-Sunter method.
    weight = 0

    for field_info in identifier_fields:
        key = field_info["key"]
        field_a_value = getattr(patient_a, key)
        field_b_value = getattr(patient_b, key)

        if field_a_value is None or field_b_value is None:
            continue

        match_fn = field_info.get("match_fn", default_match_fn)
        is_a_match = match_fn(field_a_value, field_b_value)

        match_prob = field_info["match_prob"]
        unmatch_prob = field_info["unmatch_prob"]

        if is_a_match:
            weight += math.log(match_prob / unmatch_prob)
        else:
            weight += math.log((1 - match_prob) / (1 - unmatch_prob))

    return weight



def search_patients(search_name, df1, df2, identifier_fields):
    highest_score = float('-inf')
    lowest_score = float('inf')
    matching_pair = None
    unmatching_pair = None
    similar_data = None

    # Iterate over df1 rows
    for indexA, rowA in df1.iterrows():
        if search_name.lower() in str(rowA['firstname']).lower():
            # Initialize a flag to check if a matching row is found in DataFrame 2
            found_match_in_df2 = False
            
            # Iterate over df2 rows
            for indexB, rowB in df2.iterrows():
                # Check if the first name in df1 matches with a name in df2
                if names_match(rowA['firstname'], rowB['firstname']):
                    found_match_in_df2 = True
                    
                    current_score = compare_patients(rowA, rowB, identifier_fields)
                    
                    if current_score >= 10:
                        if current_score > highest_score:
                            highest_score = current_score
                            matching_pair = (rowA, rowB)
                    elif current_score >= 12.99137731410753:
                        if current_score > highest_score:
                            highest_score = current_score
                            matching_pair = (rowA, rowB)
                    else:
                        lowest_score = current_score
                        unmatching_pair = (rowA, rowB)
                    break  # Break the loop once a match is found in df2

            # If no matching row is found in df2, consider it as an unmatching pair
            if not found_match_in_df2:
                lowest_score = -4.831508628198819
                unmatching_pair = (rowA, None)  # None for the matching row in df2

    search_results = {
        "similar_data": similar_data,
        "matching_pair": matching_pair,
        "unmatching_pair": unmatching_pair,
        "highest_score": highest_score,
        "lowest_score": lowest_score,
    }

    return search_results

