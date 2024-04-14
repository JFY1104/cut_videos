import pandas as pd
from io import StringIO

# Your CSV data
# Read the CSV data
df = pd.read_csv("開始結束.csv")

# Group by 'video' and combine 'start' and 'end' values
df_start = df.groupby("video")["start"].apply(list).reset_index()
df_end = df.groupby("video")["end"].apply(list).reset_index()

# Convert the list of 'start' and 'end' values to a string
df_start["start"] = df_start["start"].apply(lambda x: ",".join(map(str, x)))
df_end["end"] = df_end["end"].apply(lambda x: ",".join(map(str, x)))

# Concatenate the 'start' and 'end' dataframes
df = pd.concat([df_start, df_end["end"]], axis=1)

# Write the DataFrame to a new CSV file
df.to_csv("new.csv", index=False)
