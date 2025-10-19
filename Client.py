import os
import Client
import logging
import requests
from typing import Optional
from dotenv import load_dotenv
from kalshi_python import KalshiClient
from kalshi_python.api.portfolio_api import PortfolioApi
from kalshi_python.api.markets_api import MarketsApi

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Client:
    def __init__(self, api_key_id: Optional[str] = None, private_key: Optional[str] = None):
        """
        Initialize the Kalshi API client
        
        Args:
            api_key_id: Kalshi API key ID (if not provided, will use environment variables)
            private_key: RSA private key content or path to private key file
        """
        self.api_key_id = api_key_id or os.getenv('KALSHI_API_KEY_ID')
        self.private_key = private_key or os.getenv('KALSHI_PY_PRIVATE_KEY_PEM')
        
        if not self.api_key_id or not self.private_key:
            raise ValueError(
                "API credentials not found. Please set KALSHI_API_KEY_ID and "
                "KALSHI_PY_PRIVATE_KEY_PEM environment variables or pass them directly."
            )
        
        # Initialize the Kalshi client
        try:
            self.client = KalshiClient()
            
            # Check if private_key is a file path or key content
            if os.path.exists(self.private_key):
                # It's a file path
                self.client.set_kalshi_auth(self.api_key_id, self.private_key)
            else:
                # It's key content - save to temporary file
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.pem', delete=False) as temp_file:
                    temp_file.write(self.private_key)
                    temp_key_path = temp_file.name
                
                self.client.set_kalshi_auth(self.api_key_id, temp_key_path)
                # Clean up temp file after auth
                os.unlink(temp_key_path)
            
            logger.info("✅ Kalshi API client initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Kalshi API client: {e}")
            raise

    def get_portfolio_balance(self) -> Optional[float]:
        """Get current portfolio balance"""
        try:
            balance_response = self.client.get_balance()
            balance = balance_response.balance / 100  # Convert from cents to dollars
            logger.info(f"💰 Portfolio balance: ${balance:.2f}")
            return balance
        except Exception as e:
            logger.error(f"❌ Failed to fetch portfolio balance: {e}")
            return None

    # needs to be way scaled out to actually be a useful function
    def get_events(self, limit: int = 100) -> Optional[list]:
        """Get available events"""
        try:
            events_response = self.client.get_events(limit=limit)
            events = events_response.events
            logger.info(f"📊 Fetched {len(events)} events")
            return events
        except Exception as e:
            logger.error(f"❌ Failed to fetch events: {e}")
            return None

    def get_markets_for_event(self, event_ticker: str) -> Optional[list]:
        """Get available markets for a specific event"""
        try:
            markets_response = self.client.get_markets(event_ticker=event_ticker)
            markets = markets_response.markets
            logger.info(f"📊 Fetched {len(markets)} markets")
            return markets
        except Exception as e:
            logger.error(f"❌ Failed to fetch markets: {e}")
            return None

    def get_orderbook(self, market_ticker: str) -> Optional[dict]:
        """Get bid-ask quotes for a specific market"""
        try:
            orderbook_url = f"https://api.elections.kalshi.com/trade-api/v2/markets/{market_ticker}/orderbook"
            orderbook_response = requests.get(orderbook_url)
            orderbook_data = orderbook_response.json()
            return orderbook_data

        except Exception as e:
            logger.error(f"❌ Failed to fetch quotes for {market_ticker}: {e}")
            return None
