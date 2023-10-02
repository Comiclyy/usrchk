import requests

response = requests.get(url="https://api.mojang.com/users/profiles/minecraft/balls")
print(response.text)
