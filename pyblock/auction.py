from sys import maxsize
from uuid import UUID
from dataclasses import dataclass, field
from datetime import datetime, timezone

import requests

from .item import Item
from .utils import decode_item_bytes, request_endpoint

@dataclass(init=True, repr=True, eq=True)
class Auction:
    uuid: UUID
    bin: bool
    price: int
    start: datetime
    end: datetime
    item: Item

    @classmethod
    def from_data(cls, auction: dict) -> 'Auction':
        uuid = UUID(auction['uuid'])
        bin = auction.get('bin', False)
        price = auction['starting_bid'] if bin else auction['highest_bid_amount']
        start = datetime.fromtimestamp(auction['start'] / 1000, tz=timezone.utc)
        end = datetime.fromtimestamp(auction['end'] / 1000, tz=timezone.utc)
        item = Item.from_data(auction, decode_item_bytes(auction['item_bytes']))

        return cls(uuid=uuid, bin=bin, price=price, start=start, end=end, item=item)
        
def get_auction(auction_id: UUID) -> Auction | None:
    data = request_endpoint('skyblock/auction', {'uuid': str(auction_id)})
    if len(data['auctions'] == 0): return None
    return Auction.from_data(data['auctions'][0])

def get_auctions(player: UUID | None = None,
                 profile: UUID | None = None,
                 page: int | None = None) -> list[Auction]:
    if player is None and profile is None:
        if page is None:
            auction_list: list[Auction] = []
            page_count = maxsize
            current_page = 0
            while current_page < page_count:
                data = request_endpoint('skyblock/auctions', {'page': current_page})
                auction_list.extend(Auction.from_data(auction) for auction in data['auctions'])
                page_count = data['totalPages']
                current_page += 1
            return auction_list
        data = request_endpoint('skyblock/auctions', {'page': page})
        return [Auction.from_data(auction) for auction in data['auctions']]
    data = request_endpoint('skyblock/auction', {'player': player, 'profile': profile})
    return [Auction.from_data(auction) for auction in data['auctions']]
