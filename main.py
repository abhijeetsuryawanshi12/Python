import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "http://www.alphavantage.co/query"
STOCK_KEY = "0ZQF6S21VFI2PHR0"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_KEY = "99870736948e4a47bcb3e8ea9190dd95"

TWILIO_SID = "AC2aa469d1b1cf9bca379d43459a16ab0f"
TWILIO_AUTH_TOKEN = "18e27baa0eb69ad2a222aee4e84fdf7e"

# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": STOCK_KEY
}

response_stock = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response_stock.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_stock = data_list[0]
yesterday_prize = yesterday_stock["4. close"]
print(yesterday_prize)

# TODO 2. - Get the day before yesterday's closing stock price

day_before_yesterday_stock = data_list[1]
day_before_yesterday_prize = day_before_yesterday_stock["4. close"]
print(day_before_yesterday_prize)


# TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp

pos_diff = float(yesterday_prize) - float(day_before_yesterday_prize)
up_down = None
if pos_diff > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
print(pos_diff)
# TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.

percentage_diff = round((pos_diff/float(yesterday_prize))*100)
print(percentage_diff)

# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").

if(percentage_diff > 5.00):
    print("Get News")

# STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

# TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
# if abs(percentage_diff) > 1:
stock_news_params = {
    "qInTitle": COMPANY_NAME,
    "apikey": NEWS_KEY
}
response_news = requests.get(NEWS_ENDPOINT,params=stock_news_params)
article = response_news.json()["articles"][:3]
print(article)

# TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation

three_articles = article[:3]
print(three_articles)
# STEP 3: Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.

# TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
formatted = [f"{STOCK_NAME} {up_down}{percentage_diff}\nHeadline:{article['title']}. \nBrief:{article['description']}" for article in three_articles]
# TODO 9. - Send each article as a separate message via Twilio.
client = Client(TWILIO_SID,TWILIO_AUTH_TOKEN)
for article in formatted:
    message = client.messages.create(
        body=article,
        from_="+14027266492",
        to="+919307947206"
    )


# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
