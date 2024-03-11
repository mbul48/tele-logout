import json

token = input("Token: ")
id = input("Chad id: ")
def append_to_json(filename, new_data):

  try:
    with open(filename, 'r+') as file:
      try:
        data = json.load(file)
      except json.JSONDecodeError:
        data = []

      if not isinstance(data, list):
          raise TypeError("Existing data must be a list for appending")
      
      data.append(new_data)
      file.seek(0)
      json.dump(data, file, indent=4)

  except FileNotFoundError:
    with open(filename, 'w') as file:
      json.dump([new_data], file, indent=4)


new_data = {"token": token, "id": id}
append_to_json("target_logout.json", new_data)
