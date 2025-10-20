import os
import Client
import logging
import requests
from typing import Optional
from dotenv import load_dotenv
from kalshi_python import KalshiClient, Configuration
from kalshi_python.api.portfolio_api import PortfolioApi
from kalshi_python.api.markets_api import MarketsApi
from kalshi_types import Event, Series, EventStatus, Announcement, ExchangeSchedule, ExchangeStatus

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Client:
    def __init__(self):
        config = Configuration(
            host="https://api.elections.kalshi.com/trade-api/v2"
        )
        config.api_key_id = os.getenv('KALSHI_API_KEY_ID')
        with open(os.getenv('KALSHI_PY_PRIVATE_KEY_PEM'), "r") as f:
            config.private_key_pem = f.read()
        self.client = KalshiClient(config)
        logger.info("✅ Kalshi API client initialized successfully")

    def get_portfolio_balance(self) -> Optional[float]:
        """Get current portfolio balance"""
        try:
            balance_response = self.client.get_balance()
            balance = balance_response.balance / 100  # Convert from cents to dollars
            return balance
        except Exception as e:
            logger.error(f"❌ Failed to fetch portfolio balance: {e}")
            return None

    def get_events(self, **kwargs) -> tuple[list[Event], Optional[str]]:
        """Get available events"""
        try:
            events_response = self.client.get_events(**kwargs)
            events = events_response.events or []
            cursor = events_response.cursor
            return events, cursor
        except Exception as e:
            logger.error(f"Failed to fetch events: {e}")
            return [], None

    def get_series(self, **kwargs) -> list[Series]:
        """Get available series"""
        try:
            series_response = self.client.get_series(**kwargs)
            series = series_response.series or []
            logger.info(f"Fetched {len(series)} series")
            return series
        except Exception as e:
            logger.error(f"Failed to fetch series: {e}")
            return []

    def get_markets_for_event(self, event: Event) -> Optional[list]:
        """Get available markets for a specific event"""
        # Only fetch markets for valid event statuses
        valid_statuses = (EventStatus.OPEN, EventStatus.CLOSED, EventStatus.SETTLED, EventStatus.DETERMINED)
        if event.status not in valid_statuses:
            logger.info(f"status: {event.status}")
            return None
        try:
            markets_response = self.client.get_markets(event_ticker=event.event_ticker)
            markets = markets_response.markets
            logger.info(f"Fetched {len(markets)} markets")
            return markets
        except ValueError as e:
            if "must be one of enum values" in str(e):
                logger.warning(f"Validation error for {event.event_ticker} - skipping: {e}")
                return None
            else:
                raise
        except Exception as e:
            logger.error(f"Failed to fetch markets for {event.event_ticker}: {e}")
            return None

    def get_exchange_announcements(self) -> list[Announcement]:
        """Get exchange announcements"""
        try:
            announcements_response = self.client.get_exchange_announcements()
            announcements = announcements_response.announcements or []
            return announcements
        except Exception as e:
            logger.error(f"Failed to fetch announcements: {e}")
            return []

    def get_exchange_schedule(self) -> Optional[ExchangeSchedule]:
        """Get exchange schedule"""
        try:
            schedule_response = self.client.get_exchange_schedule()
            schedule = schedule_response.schedule
            return schedule
        except Exception as e:
            logger.error(f"Failed to fetch schedule: {e}")
            return None

    def get_exchange_status(self) -> Optional[ExchangeStatus]:
        """Get exchange status"""
        try:
            status_response = self.client.get_exchange_status()
            status = status_response
            return status
        except Exception as e:
            logger.error(f"Failed to fetch status: {e}")
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
