import pyreadstat

# Replace 'your_file_path.sav' with the path to your .sav file
file_path = "CELMoD Product exposure n=143 2.sav"

# Load only the metadata of the .sav file
_, meta = pyreadstat.read_sav(file_path)

# Get the column names (header)
headers = meta.column_names

# Print the headers
print(headers)
