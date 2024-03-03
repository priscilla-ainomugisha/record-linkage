import pandas as pd
import numpy as np
from itertools import product
from scipy.stats import norm
from metaphone import doublemetaphone
import math

class RecordLinkage:
    def __init__(self, dataset1, dataset2, name_column):
        self.dataset1 = dataset1
        self.dataset2 = dataset2
        self.name_column = name_column
    
    def default_match(self, a, b):
        if isinstance(a, str) and isinstance(b, str):
            return a.lower() == b.lower()
        else:
            return a == b
        
    def names_match(name_a, name_b):
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

    
    def compare_patients(self, patient_a, patient_b, identifier_fields):
        """
        Compare two patients and return a match score using the Fellegi-Sunter method.
        """
        weight = 0
        
        for field_info in identifier_fields:
            key = field_info["key"]
            field_a_value = patient_a.get(key)
            field_b_value = patient_b.get(key)
            
            if field_a_value is None or field_b_value is None:
                continue
            
            match_fn = field_info.get("match_fn", self.default_match)
            is_a_match = match_fn(field_a_value, field_b_value)
            
            match_prob = field_info["match_prob"]
            unmatch_prob = field_info["unmatch_prob"]
            
            if is_a_match:
                weight += math.log(match_prob / unmatch_prob)
            else:
                weight += math.log((1 - match_prob) / (1 - unmatch_prob))
        
        return weight

    

    def create_blocks(self, df):
            blocks = {}
            nan_block = []

            for index, row in df.iterrows():
                first_name = row.get(self.name_column, '')
                if pd.notnull(first_name) and first_name != '':
                    first_letter = first_name[0].upper()
                    if first_letter not in blocks:
                        blocks[first_letter] = []
                    blocks[first_letter].append(index)
                elif first_name == '':
                    nan_block.append(index)
                    print(f"Empty first name found at index {index}.")
                else:
                    nan_block.append(index)
                    print(f"NaN first name found at index {index}.")

            if nan_block:
                blocks['NaN'] = nan_block

            return blocks
    
    
    def match_records_with_blocking(self, dataset1, dataset2, identifier_fields, threshold=10):
        blocks_dfa = self.create_blocks(dataset1)
        blocks_dfb = self.create_blocks(dataset2)

        matches = []

        for letter, indices1 in blocks_dfa.items():
            if letter in blocks_dfb:
                indices2 = blocks_dfb[letter]
                for i, j in product(indices1, indices2):
                    patient_a = dataset1.iloc[i]
                    patient_b = dataset2.iloc[j]
                    weight = self.compare_patients(patient_a, patient_b, identifier_fields)
                    if weight > threshold:
                        matches.append((i, j))
                    

        return matches
