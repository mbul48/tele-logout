import json

tokens = input("Token: ")
ids = input("CHAT ID: ")
def append_to_json(filename, new_data):
  """
  Appends new data to a JSON file.

  Args:
      filename (str): The path to the JSON file.
      new_data (dict): The data you want to append.
  """

  try:
    with open(filename, 'r+') as file:
      # Load existing data (if any)
      try:
        data = json.load(file)
      except json.JSONDecodeError:
        data = []  # Empty list if file is empty or invalid JSON

      # Ensure data is a list (can be modified for other structures)
      if not isinstance(data, list):
          raise TypeError("Existing data must be a list for appending")

      # Append new data
      data.append(new_data)

      # Seek to the beginning of the file
      file.seek(0)

      # Dump the modified data back to the file
      json.dump(data, file, indent=4)  # Add indentation for readability (optional)

  except FileNotFoundError:
    # Create a new file and write the data as a list
    with open(filename, 'w') as file:
      json.dump([new_data], file, indent=4)

# Example usage
new_data = {"token": tokens, "id": ids}

append_to_json("target-logout.json", new_data)
