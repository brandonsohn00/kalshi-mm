#!/usr/bin/env python3
"""
Kalshi Market Making Bot
Basic initialization and API client setup
"""
import os
import Client
import logging
import requests
from typing import Optional
from tqdm import tqdm
from dotenv import load_dotenv
from kalshi_python import KalshiClient
from kalshi_python.api.portfolio_api import PortfolioApi
from kalshi_python.api.markets_api import MarketsApi
from kalshi_types import Series

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# debugging constants
EVENT = "KXTVSEASONRELEASEACOURTOFTHORNSANDROSES"

def main():
    """Main function to test the market maker initialization"""
    try:
        # Initialize the market maker
        cli = Client.Client()
        series: list[Series] = cli.get_series()

        for i, s in enumerate(series[:1000]):
            events, cursor = cli.get_events(status = 'open', limit = 200, series_ticker = s.ticker, with_nested_markets = True)
            for event in events:
                if event.markets:
                    print(f"TITLE: {s.title} | SERIES TICKER: {s.ticker}")
                    print(f"\tEVENT: {event.title} | EVENT TICKER: {event.event_ticker}")
                    for market in event.markets:
                        print(f"\t\tMARKET: {market.title} | MARKET TICKER: {market.ticker}")
                        print(f"\t\t\tStatus: {market.status}")
                        print(f"\t\t\tYes Bid: {market.yes_bid} | Yes Ask: {market.yes_ask}")
                        print(f"\t\t\tNo Bid: {market.no_bid} | No Ask: {market.no_ask}")
                        print(f"\t\t\tLast Price: {market.last_price}")
                        print(f"\t\t\tVolume: {market.volume} | 24h Volume: {market.volume_24h}")
                        print(f"\t\t\tOpen Time: {market.open_time}")
                        print(f"\t\t\tClose Time: {market.close_time}")
                        print(f"\t\t\tExpiration: {market.expiration_time}")
                        print(f"\t\t\tCan Close Early: {market.can_close_early}")
                        print(f"\t\t\tResult: {market.result}")
                        print()
        
        # markets = cli.get_markets_for_event(event_ticker=EVENT)
        # print(markets)
        # orderbook = cli.get_orderbook(market_ticker=markets[0].ticker)
        # print(orderbook)

        '''
        # Test connection
        if mm.test_connection():
            logger.info("🎉 Market maker initialized successfully!")
            
            # Get basic data
            balance = mm.get_portfolio_balance()
            markets = mm.get_markets(limit=5)  # Get more markets to find one with quotes
            print("Markets:", markets)
        else:
            logger.error("❌ Failed to connect to Kalshi API")
        '''
            
    except Exception as e:
        logger.error(f"❌ Error initializing market maker: {e}")


if __name__ == "__main__":
    main()
