from bs4 import BeautifulSoup
import requests

# URL https://paris.demosphere.net/?selectStartTime=1567288801&endTime=1569880801&limit=10000&showArchiveLinks=1
url = 'https://paris.demosphere.net/?selectStartTime=1567288801&endTime=1569880801&limit=10000&showArchiveLinks=1'
response = request.get(url, timeout=5)
content = BeautifulSoup(response.content,"html.parser")

print(content)
# RESPONSE
# CONTENT