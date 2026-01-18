from bs4 import BeautifulSoup
import csv




#1. Read the web_data.html file into an html parser
print("Reading in html file")
with open("../data/raw_data/web_data.html", "r", encoding="utf-8") as file:
	html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')
print("DEBUG: Checking HTML content")
# print(html_content[:500])
#2: Extract Market banner data, storing in list
print("Filtering for market banner data...")
market_data = []

market_cards = soup.find_all('a', class_='MarketCard-container')

for card in market_cards:
	try:
		symbol_tag = card.find('span', class_='MarketCard-symbol')
		position_tag = card.find('span', class_='MarketCard-stockPosition')
		change_pct_tag = card.find('span', class_='MarketCard-changesPct')
		
		if symbol_tag and position_tag and change_pct_tag:
			market_data.append({
				'symbol': symbol_tag.get_text(strip=True),
				'stock_position': position_tag.get_text(strip=True),
				'change_pct': change_pct_tag.get_text(strip=True)
			})
	except Exception as e:
		print(f"Error parsing market card: {e}")

#3. Save market data to CSV
print("Writing market data to CSV")
with open("../data/processed_data/market_data.csv", "w", encoding="utf-8") as file:
	if market_data: 
		fieldnames = ['symbol', 'stock_position', 'change_pct']
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(market_data)
		print("market_data.csv created successfully")
	else:
		print("No market data found")


#4. Extract latest news data
print("Filtering for latest news list data")
latest_news = []

news_cards = soup.find_all(class_=lambda x: x and 'LatestNews-item' in x)

for card in news_cards:
	try:
		timestamp_tag = card.find(class_=lambda x: x and 'LatestNews-timestamp' in x)
		headline_tag = card.find(class_=lambda x: x and 'LatestNews-headline' in x)
		
		if timestamp_tag and headline_tag:
			latest_news.append({
				'timestamp': timestamp_tag.get_text(strip=True),
				'headline': headline_tag.get_text(strip=True),
				'link': headline_tag.get('href', '')
			})
	except Exception as e:
		print(f"Error parsing: {e}")

#5. Save news data to CSV
print("writing news data to CSV")
with open("../data/processed_data/news_data.csv", "w", encoding="utf-8") as file:
	if latest_news:
		fieldnames = ['timestamp', 'headline', 'link']
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(latest_news)
		print("news_data.csv created successfully")
	else:
		print("No news data found")


