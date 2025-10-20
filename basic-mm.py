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

        for i, s in enumerate(series[:50]):
            print(f"TITLE: {s.title} | SERIES TICKER: {s.ticker}")
            events, cursor = cli.get_events(limit = 200, series_ticker = s.ticker)
            for event in events:
                print(f"\tEVENT: {event.title} | EVENT TICKER: {event.event_ticker}")
                if event.markets:
                    print(len(event.markets))
                else:
                    print("\tNo markets found")
        
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
