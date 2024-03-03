from metaphone import doublemetaphone
import math
import pandas as pd

class FellegiSunterModel:
    def __init__(self, identifier_fields):
        self.identifier_fields = identifier_fields

    @staticmethod
    def default_match_fn(a, b):
        """
        Default function for determining if two values are a match.
        """
        if isinstance(a, str) and isinstance(b, str):
            return a.lower() == b.lower()
        else:
            return a == b

    @staticmethod
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

    def compare_patients(self, patient_a, patient_b):
        """
        Compare two patients and return a match score using the Fellegi-Sunter method.
        """
        weight = 0

        for field_info in self.identifier_fields:
            key = field_info["key"]
            field_a_value = patient_a[key]
            field_b_value = patient_b[key]

            if field_a_value is None or field_b_value is None:
                continue

            match_fn = field_info.get("match_fn", self.default_match_fn)
            is_a_match = match_fn(field_a_value, field_b_value)

            match_prob = field_info["match_prob"]
            unmatch_prob = field_info["unmatch_prob"]

            if is_a_match:
                weight += math.log(match_prob / unmatch_prob)
            else:
                weight += math.log((1 - match_prob) / (1 - unmatch_prob))

        return weight

    def search_patients(self, search_name, df1, df2):
        highest_score = float('-inf')
        lowest_score = float('inf')
        matching_pair = None
        unmatching_pair = None
        similar_data = []

        found_match_in_df2 = False  # Initialize before the loop

        # Iterate over df1 rows
        for indexA, rowA in df1.iterrows():
            if search_name.lower() in str(rowA['firstname']).lower():
                # Iterate over df2 rows
                for indexB, rowB in df2.iterrows():
                    if search_name.lower() in str(rowB['firstname']).lower():
                        current_score = self.compare_patients(rowA, rowB)

                        if current_score > highest_score:
                            highest_score = current_score
                            matching_pair = (rowA, rowB)
                        
                        found_match_in_df2 = True
                        break  # Break the loop once a match is found in df2

                # If a matching row is found in df2, break the loop
                if found_match_in_df2:
                    break

        # If no matching row is found in df2, consider it as an unmatching pair
        if not found_match_in_df2:
            unmatching_pair = (rowA, rowB)  # None for the matching row in df2
            matching_pair = (rowA, rowB)  # Return the details of the searched person for unmatching pair


        search_results = {
            "similar_data": similar_data,
            "matching_pair": matching_pair,
            "unmatching_pair": unmatching_pair,
            "highest_score": highest_score,
            "lowest_score": lowest_score,
        }

        return search_results
