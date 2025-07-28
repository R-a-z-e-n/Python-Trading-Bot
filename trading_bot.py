from binance.client import Client
from binance.exceptions import BinanceAPIException
import logging
import json
from typing import Dict, Optional
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler()
    ]
)

class BasicBot:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.client = Client(api_key, api_secret, testnet=testnet)
        if testnet:
            self.client.API_URL = 'https://testnet.binancefuture.com'
        
        
        self.logger = logging.getLogger(__name__)
        
    def _log_api_response(self, action: str, response: Dict) -> None:
        """Log API responses"""
        self.logger.info(f"{action} Response: {json.dumps(response, indent=2)}")

    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict:
        """Place a market order"""
        try:
            self.logger.info(f"Placing market {side} order for {quantity} {symbol}")
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            self._log_api_response('Market Order', order)
            return order
        except BinanceAPIException as e:
            self.logger.error(f"Market order failed: {str(e)}")
            raise

    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> Dict:
        """Place a limit order"""
        try:
            self.logger.info(f"Placing limit {side} order for {quantity} {symbol} at {price}")
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                timeInForce='GTC',
                quantity=quantity,
                price=price
            )
            self._log_api_response('Limit Order', order)
            return order
        except BinanceAPIException as e:
            self.logger.error(f"Limit order failed: {str(e)}")
            raise

    def place_stop_limit_order(self, symbol: str, side: str, quantity: float, 
                              price: float, stop_price: float) -> Dict:
        """Place a stop-limit order (Bonus feature)"""
        try:
            self.logger.info(f"Placing stop-limit {side} order for {quantity} {symbol} "
                            f"at {price} with stop at {stop_price}")
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP',
                timeInForce='GTC',
                quantity=quantity,
                price=price,
                stopPrice=stop_price
            )
            self._log_api_response('Stop-Limit Order', order)
            return order
        except BinanceAPIException as e:
            self.logger.error(f"Stop-limit order failed: {str(e)}")
            raise

    def get_order_status(self, symbol: str, order_id: int) -> Dict:
        """Get the status of an order"""
        try:
            status = self.client.futures_get_order(symbol=symbol, orderId=order_id)
            self._log_api_response('Order Status', status)
            return status
        except BinanceAPIException as e:
            self.logger.error(f"Failed to get order status: {str(e)}")
            raise


def main():
    
    API_KEY = 'my_api_key'
    API_SECRET = 'my_api_secret'
    
    bot = BasicBot(API_KEY, API_SECRET, testnet=True)
    
    while True:
        print("\nBinance Futures Trading Bot")
        print("1. Place Market Order")
        print("2. Place Limit Order")
        print("3. Place Stop-Limit Order")
        print("4. Check Order Status")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '5':
            break
            
        symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
        side = input("Enter side (BUY/SELL): ").upper()
        
        try:
            if choice == '1':
                quantity = float(input("Enter quantity: "))
                order = bot.place_market_order(symbol, side, quantity)
                print(f"Order placed successfully: {order['orderId']}")
                
            elif choice == '2':
                quantity = float(input("Enter quantity: "))
                price = float(input("Enter price: "))
                order = bot.place_limit_order(symbol, side, quantity, price)
                print(f"Order placed successfully: {order['orderId']}")
                
            elif choice == '3':
                quantity = float(input("Enter quantity: "))
                price = float(input("Enter price: "))
                stop_price = float(input("Enter stop price: "))
                order = bot.place_stop_limit_order(symbol, side, quantity, price, stop_price)
                print(f"Order placed successfully: {order['orderId']}")
                
            elif choice == '4':
                order_id = int(input("Enter order ID: "))
                status = bot.get_order_status(symbol, order_id)
                print(f"Order status: {status['status']}")
                
        except BinanceAPIException as e:
            print(f"Error: {str(e)}")
        except ValueError as e:
            print(f"Invalid input: {str(e)}")

if __name__ == '__main__':
    main()
