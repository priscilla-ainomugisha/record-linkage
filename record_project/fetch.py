from django.db import models
import pandas as pd
from record_app.models import SyntheticFacilityV3, SyntheticHdssV3

# Fetch data from Django models
df1_queryset = SyntheticFacilityV3.objects.all()[:5]
df2_queryset = SyntheticHdssV3.objects.all()[:5]

# Convert querysets to pandas DataFrames
df1 = pd.DataFrame(list(df1_queryset.values()))
df2 = pd.DataFrame(list(df2_queryset.values()))

# Display the dataframes
print("Data from SyntheticFacilityV3:")
print(df1)

print("\nData from SyntheticHdssV3:")
print(df2)
