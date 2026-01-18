import requests
from bs4 import BeautifulSoup

#Headers so our request can be recognized as a valid browser
headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

#make get request to webpage
url = "https://www.cnbc.com/world/?region=world"
response = requests.get(url, headers=headers)

if response.status_code == 200:
	soup = BeautifulSoup(response.content, 'html.parser')
	
	with open("../data/raw_data/web_data.html", "w", encoding = "utf-8") as file:
		file.write(str(soup.prettify()))
	
	print("web data written out")

else:
	print("Failed")


