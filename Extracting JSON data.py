import json

json_data = '{"this":"succeeded","by":"getting","the":"dweets","with":[{"thing":"my_thing_name","created":"2023-06-03T06:03:10.178Z","content":{"value":32}}]}'

# Parse the JSON data
data = json.loads(json_data)

# Access the value
value = data["with"][0]["content"]["value"]

print(value)  # Output: 32
