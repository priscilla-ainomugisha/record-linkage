from django.shortcuts import render, redirect
from background_task import background
from django.http import HttpResponse
from .notebook_logic import search_patients
from django.db import models
import pandas as pd

from .fellegi import FellegiSunterModel
from .chat import RecordLinkage

from .models import SyntheticFacilityV3, SyntheticHdssV3

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Facility_staff, Hdss_staff
from record_app.hdss_backend import HdssStaffAuthenticationBackend
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facility_staff_login')  # Redirect to login page after successful registration
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def home(request):
    return render(request, 'index.html')

def facility_staff_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_facility')  # Redirect to facility staff dashboard
        else:
            # Authentication failed, handle it appropriately
            return render(request, 'facility_login.html', {'error_message': 'Invalid username or password'})
    else:
        # If request method is not POST, render the login form
        return render(request, 'facility_login.html')

def hdss_staff_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_hdss')  # Redirect to HDSS staff dashboard
    return render(request, 'hdss_login.html')

def dashboard_facility(request):
    if request.user.is_authenticated:
        return render(request, 'search_form.html')
    else:
        return redirect('facility_staff_login')

def dashboard_hdss(request):
    if request.user.is_authenticated:
        return render(request, 'search_form.html')
    else:
        return redirect('hdss_staff_login')


def logout(request):
    return render(request, 'index.html')

@background(schedule=1)
def perform_record_linkage(search_name):
    # Fetch data from Django models
    df1_queryset = SyntheticFacilityV3.objects.all()
    df2_queryset = SyntheticHdssV3.objects.all()

    # Convert querysets to pandas DataFrames
    df1 = pd.DataFrame(list(df1_queryset.values()))
    df2 = pd.DataFrame(list(df2_queryset.values()))
         
    search_patients(search_name, df1, df2, identifier_fields)

def clean_data(df1,df2):
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

    # Check columns with null values
    null_columns = df1.isnull().any()
    columns_with_nulls = null_columns[null_columns]
    print("Columns with null values")
    print(columns_with_nulls)

    # Drop columns with null values
    df2 = df2.drop(columns=['nationalid'])

    # Remove leading spaces in first name and last name columns
    df1['firstname'] = df1['firstname'].str.strip()
    df1['lastname'] = df1['lastname'].str.strip()

    # Cleaning the datasets

    # Edit the formulation of dob
    df2['dob'] = pd.to_datetime(df2['dob'], errors='coerce')

    # Change the format of date in column dob to 9/9/1930
    df2['dob'] = df2['dob'].dt.strftime('%d/%m/%Y')

    # Formatting the visit date
    df1['visitdate'] = pd.to_datetime(df1['visitdate'], errors='coerce')
    df1['visitdate'] = df1['visitdate'].dt.strftime('%d/%m/%Y')

    # Check columns with null values
    null_columns = df1.isnull().any()
    columns_with_nulls = null_columns[null_columns]
    print("Columns with null values")
    print(columns_with_nulls)

    # Remove leading spaces in first name and last name columns
    df2['firstname'] = df2['firstname'].str.strip()
    df2['lastname'] = df2['lastname'].str.strip()

    return df1,df2
    

def clean_hdss_data(df1,df2):
    # Fetch data from Django models
    df1_queryset = SyntheticHdssV3.objects.all()
    df2_queryset = SyntheticFacilityV3.objects.all()

    # Convert querysets to pandas DataFrames
    df1 = pd.DataFrame(list(df1_queryset.values()))
    df2 = pd.DataFrame(list(df2_queryset.values()))

    # Cleaning the datasets

    # Edit the formulation of dob
    df1['dob'] = pd.to_datetime(df1['dob'], errors='coerce')

    # Change the format of date in column dob to 9/9/1930
    df1['dob'] = df1['dob'].dt.strftime('%d/%m/%Y')

    # Check columns with null values
    null_columns = df1.isnull().any()
    columns_with_nulls = null_columns[null_columns]
    print("Columns with null values")
    print(columns_with_nulls)

    # Drop columns with null values
    df1 = df1.drop(columns=['nationalid'])

    # Remove leading spaces in first name and last name columns
    df1['firstname'] = df1['firstname'].str.strip()
    df1['lastname'] = df1['lastname'].str.strip()

    # Cleaning the datasets

    # Edit the formulation of dob
    df2['dob'] = pd.to_datetime(df2['dob'], errors='coerce')

    # Change the format of date in column dob to 9/9/1930
    df2['dob'] = df2['dob'].dt.strftime('%d/%m/%Y')

    # Formatting the visit date
    df2['visitdate'] = pd.to_datetime(df2['visitdate'], errors='coerce')
    df2['visitdate'] = df2['visitdate'].dt.strftime('%d/%m/%Y')

    # Check columns with null values
    null_columns = df1.isnull().any()
    columns_with_nulls = null_columns[null_columns]
    print("Columns with null values")
    print(columns_with_nulls)

    # Remove leading spaces in first name and last name columns
    df2['firstname'] = df2['firstname'].str.strip()
    df2['lastname'] = df2['lastname'].str.strip()

    return df1,df2
    

def merge_datasets(df1, df2):
    # Merge the two datasets on the common column 'firstname'
    common_dataset = pd.merge(df1, df2, on='firstname', how='inner')

    # Drop duplicates based on the common column
    common_dataset.drop_duplicates(subset='firstname', inplace=True)

    # Reset index
    common_dataset.reset_index(drop=True, inplace=True)

    return common_dataset

# Fellegi Sunter

### Probabilistic machine learning approach

import math
from metaphone import doublemetaphone

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
]  # Example identifier fields

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

from django.shortcuts import render

def search_view(request):
    if request.method == 'POST':
        # Handle POST request
        search_name = request.POST.get('search_name')
        
        # Fetch data from Django models
        df1_queryset = SyntheticFacilityV3.objects.all()
        df2_queryset = SyntheticHdssV3.objects.all()

        # Convert querysets to pandas DataFrames
        df1 = pd.DataFrame(list(df1_queryset.values()))
        df2 = pd.DataFrame(list(df2_queryset.values()))
        
        # Clean the data for each dataset
        df1_cleaned = clean_data(df1)
        df2_cleaned = clean_data(df2)

        # Call the search_patients function with the cleaned DataFrames and required arguments
        search_results = search_patients(search_name, df1_cleaned, df2_cleaned, identifier_fields)
        
        
        return render(request, 'search_results.html', {'search_results': search_results})
            

    else:
        # Handle GET request
        return render(request, 'search_form.html')


def fellegi_view(request):
    if request.method == 'POST':
        # Handle POST request
        search_name = request.POST.get('search_name')
        # Fetch data from Django models
        df1_queryset = SyntheticFacilityV3.objects.all()
        df2_queryset = SyntheticHdssV3.objects.all()

        # Convert querysets to pandas DataFrames
        df1 = pd.DataFrame(list(df1_queryset.values()))
        df2 = pd.DataFrame(list(df2_queryset.values()))

        # Clean data 
        cleaned_df1 = clean_data(df1)
        cleaned_df2 = clean_data(df2)


        # Create an instance of FellegiSunterModel with identifier fields
        identifier_fields = [
            {"key": "firstname","match_fn": names_match, "match_prob": 0.90, "unmatch_prob": 0.10},
            {"key": "lastname","match_fn": names_match, "match_prob": 0.95, "unmatch_prob": 0.01},
            {"key": "petname", "match_fn": names_match, "match_prob": 0.60, "unmatch_prob": 0.20},
            {"key": "dob", "match_prob": 0.90, "unmatch_prob": 0.10},
            {"key": "sex", "match_prob": 0.95, "unmatch_prob": 0.05}
            # Add other identifier fields as needed
        ]
        model = FellegiSunterModel(identifier_fields)


        search_results = model.search_patients(search_name, cleaned_df1, cleaned_df2)

        # Pass search results to template or process further
        return render(request, 'fellegi_results.html', {'search_results': search_results})
    
    else:
        # Handle GET request
        return render(request, 'search_form.html')



    global record_linker
    if record_linker is None:
        # Fetch data from Django models
        df1_queryset = SyntheticFacilityV3.objects.all()
        df2_queryset = SyntheticHdssV3.objects.all()

        # Convert querysets to pandas DataFrames
        df1 = pd.DataFrame(list(df1_queryset.values()))
        df2 = pd.DataFrame(list(df2_queryset.values()))

        # Clean data and merge datasets
        cleaned_df1 = clean_data(df1)
        cleaned_df2 = clean_data(df2)

        # Ensure 'firstname' is a column in DataFrames
        if 'firstname' not in cleaned_df1.columns or 'firstname' not in cleaned_df2.columns:
            raise ValueError("firstname column is missing in one of the DataFrames")

        # Instantiate RecordLinkage with the correct column name
        record_linker = RecordLinkage(cleaned_df1, cleaned_df2, 'firstname')

        # Perform record linkage and get matches
        matches = record_linker.match_records()
        
        # Calculate and store weights
        record_linker.calculate_weights(matches)
        # Assuming you have a method for storing weights
        record_linker.store_weights("weights.csv",weights)


'''def chat_view(request):
    if request.method == 'POST':
        search_name = request.POST.get('search_name')
        df1_queryset = SyntheticFacilityV3.objects.all()
        df2_queryset = SyntheticHdssV3.objects.all()

        df1 = pd.DataFrame(list(df1_queryset.values()))
        df2 = pd.DataFrame(list(df2_queryset.values()))

        cleaned_df1 = clean_data(df1)
        cleaned_df2 = clean_data(df2)

        if 'firstname' not in cleaned_df1.columns or 'firstname' not in cleaned_df2.columns:
            return HttpResponse("firstname column is missing in one of the DataFrames")

        # Create blocks for both dataframes
        blocks_df1 = create_blocks(cleaned_df1)
        blocks_df2 = create_blocks(cleaned_df2)

        # Instantiate RecordLinkage outside the loop
        record_linker = RecordLinkage(cleaned_df1, cleaned_df2, 'firstname')

        search_results = []
        for block_key, block_indices_df1 in blocks_df1.items():
            block_indices_df2 = blocks_df2.get(block_key, [])
            for index_df1 in block_indices_df1:
                for index_df2 in block_indices_df2:
                    match = record_linker.match_records(index_df1, index_df2)
                    if match and (search_name.lower() in str(cleaned_df1.iloc[index_df1]['firstname']).lower() or search_name.lower() in str(cleaned_df2.iloc[index_df2]['firstname']).lower()):
                        search_results.append((cleaned_df1.iloc[index_df1], cleaned_df2.iloc[index_df2]))

        return render(request, 'chat_results.html', {'search_results': search_results})
    return render(request, 'search_form.html')
'''
def chat_view(request):
    if request.method == 'POST':
        # Handle POST request
        search_name = request.POST.get('search_name')
        # Fetch data from Django models
        df1_queryset = SyntheticFacilityV3.objects.all()[:20]
        df2_queryset = SyntheticHdssV3.objects.all()[:20]

        # Convert querysets to pandas DataFrames
        df1 = pd.DataFrame(list(df1_queryset.values()))
        df2 = pd.DataFrame(list(df2_queryset.values()))

        # Clean data and merge datasets
        cleaned_df1,cleaned_df2 = clean_data(df1,df2)


        # Ensure 'firstname' is a column in DataFrames
        if 'firstname' not in cleaned_df1.columns or 'firstname' not in cleaned_df2.columns:
            return HttpResponse("firstname column is missing in one of the DataFrames")

        print("Cleaned DataFrame 1 (FacilityHdssV3):")
        print(cleaned_df1)
        print("Cleaned DataFrame 2 (SyntheticHdssV3):")
        print(cleaned_df2)

        # Instantiate RecordLinkage with the correct column name
        record_linker = RecordLinkage(cleaned_df1, cleaned_df2, 'firstname')

        # Perform record linkage and get matches
        matches = record_linker.match_records()

        # Filter search results based on search query
        search_results = [(cleaned_df1.iloc[i], cleaned_df2.iloc[j]) for i, j in matches if search_name.lower() in str(cleaned_df1.iloc[i]['firstname']).lower() or search_name.lower() in str(cleaned_df2.iloc[j]['firstname']).lower()]
        
        return render(request, 'chat_results.html', {'search_results': search_results})
    return render(request, 'search_form.html')

def hdss_view(request):
    if request.method == 'POST':
        # Handle POST request
        search_name2 = request.POST.get('search_name')
        # Fetch data from Django models
        df1_querysett = SyntheticHdssV3.objects.all()[:20]
        df2_querysett = SyntheticFacilityV3.objects.all()[:20]

        # Convert querysets to pandas DataFrames
        dfa = pd.DataFrame(list(df1_querysett.values()))
        dfb = pd.DataFrame(list(df2_querysett.values()))

        # Clean data and merge datasets
        cleaned_dfa,cleaned_dfb  = clean_hdss_data(dfa,dfb)

        # Ensure 'firstname' is a column in DataFrames
        if 'firstname' not in cleaned_dfa.columns or 'firstname' not in cleaned_dfb.columns:
            return HttpResponse("firstname column is missing in one of the DataFrames")

        # Debugging: Print cleaned DataFrame A
        print("Cleaned DataFrame A (SyntheticHdssV3):")
        print(cleaned_dfa.head(20))

        print("Cleaned DataFrame A (FacilityHdssV3):")
        print(cleaned_dfb.head(20))

        # Instantiate RecordLinkage with the correct column name
        record_linker2 = RecordLinkage(cleaned_dfa, cleaned_dfb, 'firstname')

        # Perform record linkage and get matches
        matches2 = record_linker2.match_records()

        # Filter search results based on search query
        search_results2 = [(cleaned_dfa.iloc[i], cleaned_dfb.iloc[j]) for i, j in matches2 if search_name2.lower() in str(cleaned_dfa.iloc[i]['firstname']).lower() or search_name2.lower() in str(cleaned_dfb.iloc[j]['firstname']).lower()]
        
        # Debugging: Print search query and search results
        print("Search Query:", search_name2)
        print("Search Results2:", search_results2)
        
        return render(request, 'hdss_results.html', {'search_results2': search_results2, 'search_name2': search_name2})
    return render(request, 'search_form2.html')
