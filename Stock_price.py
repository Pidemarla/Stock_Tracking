import json
import boto3
import yfinance as yf

# Set up SNS client
sns_client = boto3.client('sns')
sns_topic_arn = 'arn:aws:sns:us-east-1:084375564922:StockPriceAlerts'  # Replace with your SNS Topic ARN

# Dictionary of stock ticker symbols with their preferred prices (Indian stocks with .NS suffix)
    # Dictionary of stock ticker symbols with their preferred prices
preferred_prices = {
    'AAPL': 320.00,
    'MSFT': 400.00,
    'NVDA': 100.00,
    'AMZN': 170.00
}

def main():
    # Loop through preferred prices and check current prices
    for ticker, preferred_price in preferred_prices.items():
        stock = yf.Ticker(ticker)
        current_price = stock.history(period='1d')['Close'].iloc[0]

        # Check if current price is less than or equal to preferred price
        if current_price <= preferred_price:
            message = f"{ticker}: The stock has come to your preferred zone! Current price: ₹{current_price:.2f}"
            print(message)
            send_notification(message)
def send_notification(message):
    # Publish a message to the SNS topic
    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=message,
        Subject='Stock Price Alert'
    )

if __name__ == '__main__':
    main()
