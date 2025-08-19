import json

# Data to be written to the JSON file
data = {
    "message": "Welcome"
}

# File path to save the JSON file
file_path = "hello.json"

# Writing data to the JSON file
with open(file_path, 'w') as json_file:
    json.dump(data, json_file)

print(f"Successfully wrote 'Hello' to {file_path}")
