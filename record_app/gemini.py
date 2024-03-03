import pandas as pd
from collections import namedtuple

MatchPair = namedtuple('MatchPair', ['record1', 'record2', 'weight'])

class RecordLinkage:
    def __init__(self, df1, df2, blocking_key, comparison_fields, default_match_weight,
                 weight_function=None, threshold=0.5):
        """
        Initializes the record linkage class.

        Args:
            df1 (pandas.DataFrame): The first dataset containing records to be linked.
            df2 (pandas.DataFrame): The second dataset containing records for comparison.
            blocking_key (str): The column name used to group similar records in both dataframes.
            comparison_fields (list[str]): A list of column names to compare for similarity.
            default_match_weight (float): The weight assigned to exact matches (default: 1.0).
            weight_function (callable, optional): A custom function to calculate similarity weights.
                If not provided, a simple comparison-based function will be used.
            threshold (float, optional): The threshold for classifying a pair as a match (default: 0.5).
        """

        self.df1 = df1.copy()  # Avoid modifying original dataframes
        self.df2 = df2.copy()
        self.blocking_key = blocking_key
        self.comparison_fields = comparison_fields
        self.default_match_weight = default_match_weight
        self.weight_function = weight_function or self._default_weight_function
        self.threshold = threshold

        # Create blocking groups for efficient searching
        self.df1_blocks = self.df1.groupby(self.blocking_key)
        self.df2_blocks = self.df2.groupby(self.blocking_key)

    def _default_weight_function(self, record1, record2):
        """Calculates the similarity weight based on exact matches in comparison fields.

        Args:
            record1 (dict): A dictionary representing a record from dataset 1.
            record2 (dict): A dictionary representing a record from dataset 2.

        Returns:
            float: The calculated similarity weight (between 0 and 1).
        """

        num_matches = sum(record1[field] == record2[field] for field in self.comparison_fields)
        num_fields = len(self.comparison_fields)
        return num_matches / num_fields

    def search(self, query_record):
        """Searches for matches for the given query record.

        Args:
            query_record (dict): A dictionary representing the record to search for.

        Returns:
            list[MatchPair]: A list of MatchPair objects containing potential matches and their weights.
        """

        # Block the query record based on the blocking key
        query_block_key = query_record[self.blocking_key]

        # Get the potential candidate records from dataset 2
        candidate_block = self.df2_blocks.get_group(query_block_key)

        # Calculate weights for all candidates
        weighted_candidates = []
        for candidate_record in candidate_block.to_dict('records'):
            # Check for exact match
            if all(query_record[field] == candidate_record[field] for field in self.comparison_fields):
                weight = self.default_match_weight
            else:
                weight = self.weight_function(query_record, candidate_record)

            weighted_candidates.append(MatchPair(query_record, candidate_record, weight))

        # Apply Fellegi-Sunter approach
        return self._fellegi_sunter(weighted_candidates)

    def _fellegi_sunter(self, weighted_candidates):
        """Implements the Fellegi-Sunter probabilistic approach to classify matches.

        Args:
            weighted_candidates (list[MatchPair]): A list of MatchPair objects containing potential matches and their weights.

        Returns:
            list[MatchPair]: A list of MatchPair objects classified as matches (weight >= threshold).
        """

        matches = []
        for candidate in weighted_candidates:
            if candidate.weight >= self.threshold:
                matches.append(candidate)

        return matches

# Example usage (continued)
df1 = pd.DataFrame({'name': ['Alice', 'Bob', 'Charlie', 'David', 'Emma'],
                   'address': ['123 Main St', '456 Elm St', '789 Oak Ave', '1011 Birch Rd', '1213 Maple Ln']})
df2 = pd.DataFrame({'name': ['Alexis', 'Robert', 'Charles', 'Daniel', 'Emma'],
                   'address': ['125 Main St', '458 Elm St', '791 Oak Ave', '1012 Birch Rd', '1215 Maple Ln']})

record_linker = RecordLinkage(df1, df2, blocking_key='name', comparison_fields=['address'],
                              default_match_weight=1.0, threshold=0.7)

query_record = {'name': 'Emma'}
matches = record_linker.search(query_record)

if matches:
    print("Matches:")
    for match in matches:
        print(f"- Record 1: {match.record1}")
        print(f"- Record 2: {match.record2}")
        print(f"- Weight: {match.weight}\n")
else:
    print("No matches found.")
