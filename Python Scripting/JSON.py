import json

employee_data = '''
{
    "people": [
        {
            "name": "Asi",
            "email": ["aboobackerasi198@gmail.com", "aboobackerasi198work@gmail.com"],
            "married": false
        },
        {
            "name": "Nida",
            "email": ["nida@gmail.com", "nida198work@gmail.com"],
            "married": false
        }
    ]
}
'''

data = json.loads(employee_data)
print(data)
print(data["people"][1]["name"])  # Output: Nida
