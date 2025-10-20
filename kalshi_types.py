from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class MarketStatus(str, Enum):
    INITIALIZED = "initialized"
    ACTIVE = "active"
    CLOSED = "closed"
    SETTLED = "settled"
    DETERMINED = "determined"
    FINALIZED = "finalized"

class EventStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    SETTLED = "settled"
    DETERMINED = "determined"

@dataclass
class Market:
    ticker: Optional[str] = None
    series_ticker: Optional[str] = None
    event_ticker: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    open_time: Optional[datetime] = None
    close_time: Optional[datetime] = None
    expiration_time: Optional[datetime] = None
    status: Optional[MarketStatus] = None
    yes_bid: Optional[float] = None
    yes_ask: Optional[float] = None
    no_bid: Optional[float] = None
    no_ask: Optional[float] = None
    last_price: Optional[float] = None
    volume: Optional[int] = None
    volume_24h: Optional[int] = None
    result: Optional[str] = None
    can_close_early: Optional[bool] = None
    cap_count: Optional[int] = None

@dataclass
class Event:
    event_ticker: Optional[str] = None
    series_ticker: Optional[str] = None
    sub_title: Optional[str] = None
    title: Optional[str] = None
    status: Optional[EventStatus] = None
    markets: Optional[List[Market]] = None

@dataclass
class Series:
    additional_prohibitions: Optional[List[str]] = None
    category: Optional[str] = None
    contract_terms_url: Optional[str] = None
    contract_url: Optional[str] = None
    fee_multiplier: Optional[int] = None
    fee_type: Optional[str] = None
    frequency: Optional[str] = None
    product_metadata: Optional[Dict[str, Any]] = None
    settlement_sources: Optional[List[Any]] = None
    tags: Optional[List[str]] = None
    ticker: Optional[str] = None
    title: Optional[str] = None

@dataclass
class GetEventsResponse:
    events: Optional[List[Event]] = None
    cursor: Optional[str] = None
