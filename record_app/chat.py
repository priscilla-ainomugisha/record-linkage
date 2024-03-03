import pandas as pd
import numpy as np
from itertools import product
from scipy.stats import norm
from metaphone import doublemetaphone

class RecordLinkage:
    def __init__(self, dataset1, dataset2, name_column):
        self.dataset1 = dataset1
        self.dataset2 = dataset2
        self.name_column = name_column
    
    def default_match(self, name1, name2):
        # Implement your default matching logic here
        # For example, you can use exact string matching, edit distance, etc.
        return name1 == name2
    
    def similar_names(self, name1, name2):
        # Implement your logic to check similarity between names
        # For example, you can use edit distance, phonetic encoding, etc.
        # For simplicity, let's use exact string matching as an example
        return name1.lower() == name2.lower()
    
    def calculate_weights(self):
        # Initialize arrays to store weights
        n = min(100, len(self.dataset1))  # Limit to first 100 values
        m = min(100, len(self.dataset2))  # Limit to first 100 values
        weights = np.zeros((n, m))

        # Iterate over each pair of records
        for i, j in product(range(n), range(m)):
            name1 = self.dataset1.iloc[i][self.name_column]
            name2 = self.dataset2.iloc[j][self.name_column]

            # Default match
            if self.default_match(name1, name2):
                weights[i][j] += 1
            
            # Similar names
            if self.similar_names(name1, name2):
                weights[i][j] += 0.5  # Adjust weight as needed
        
        return weights

    

    
    def probabilistic_match(self, weights):
        # Calculate probabilities using Fellegi-Sunter approach
        n = min(100, len(self.dataset1))  # Limit to first 100 values
        m = min(100, len(self.dataset2))  # Limit to first 100 values
        prob_match = np.zeros((n, m))
        prob_nonmatch = np.zeros((n, m))

        for i, j in product(range(n), range(m)):
            # Check if index is within bounds
            if i < len(weights) and j < len(weights[0]):
                weight = weights[i][j]
                prob_match[i][j] = norm.pdf(weight, loc=1, scale=0.1)
                prob_nonmatch[i][j] = norm.pdf(weight, loc=0, scale=0.1)

        return prob_match, prob_nonmatch

    
    def match_records(self, threshold=0.5):
        # Calculate weights
        weights = self.calculate_weights()
        
        # Calculate probabilities
        prob_match, prob_nonmatch = self.probabilistic_match(weights)
        
        # Determine matches based on threshold
        matches = []
        n, m = prob_match.shape
        for i, j in product(range(n), range(m)):
            if prob_match[i][j] > threshold * prob_nonmatch[i][j]:
                matches.append((i, j))
        
        return matches

    def create_blocks(df):
        blocks = {}
        for index, row in df.iterrows():
            first_letter = row['last_name'][0].upper()  # Assuming last_name is a string
            if first_letter not in blocks:
                blocks[first_letter] = []
            blocks[first_letter].append(index)
        return blocks

    