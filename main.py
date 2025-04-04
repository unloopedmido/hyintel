from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from parser import parse_item_bytes
from colors import parse_minecraft_text
import logging
import httpx
import time
import json
import asyncio

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Simple cache implementation for auction data
class AuctionCache:
    def __init__(self):
        self.cache_time = 0
        self.cached_auctions = []

auction_cache = AuctionCache()

@app.get("/", response_class=HTMLResponse)
async def show_auctions(request: Request, query: str = Query(None), rarity: str = Query(None)):
    url = "https://api.hypixel.net/v2/skyblock/auctions"
    
    # Cache invalidation - refresh data if empty or older than 3 mins
    if len(auction_cache.cached_auctions) == 0 or (int(time.time()) - auction_cache.cache_time) > 60 * 3:
        logging.info("Getting new auctions")
        all_auctions = []
        
        try:
            async with httpx.AsyncClient() as client:
                # Get first page to determine total pages
                response = await client.get(f"{url}?page=0")
                response.raise_for_status()
                data = response.json()
                
                all_auctions.extend(data.get("auctions", []))
                total_pages = data.get("totalPages", 0)
                
                # Helper function to fetch a single page of auction data
                async def fetch_page(page_num):
                    try:
                        logging.info(f"Fetching page {page_num}")
                        page_response = await client.get(f"{url}?page={page_num}")
                        page_response.raise_for_status()
                        return page_response.json()
                    except Exception as e:
                        logging.error(f"Error fetching page {page_num}: {e}")
                        return {"auctions": []}
                
                # Fetch all remaining pages concurrently for better performance
                tasks = [fetch_page(page) for page in range(1, total_pages)]
                results = await asyncio.gather(*tasks)
                
                for page_data in results:
                    all_auctions.extend(page_data.get("auctions", []))
                
                # Update the cache with fresh data
                auction_cache.cached_auctions = all_auctions
                auction_cache.cache_time = int(time.time())
        except Exception as e:
            print(f"Error fetching auctions: {e}")
            # Fallback to cached data if available, even if expired
            all_auctions = auction_cache.cached_auctions
    else:
        print("Using cached auctions")
        all_auctions = auction_cache.cached_auctions
    
    # Filter auctions based on search query and BIN status
    # If a query is provided, filter auctions by item name and BIN status
    if query:
        bin_auctions = [a for a in all_auctions if query.lower() in a.get("item_name", "").lower() and a.get("bin")]
    else:
        # Only show BIN (Buy It Now) auctions when no query is provided
        bin_auctions = [a for a in all_auctions if a.get("bin")]
        
    # Additional filtering by item rarity if specified
    if rarity:
        bin_auctions = [a for a in bin_auctions if rarity.lower() == a.get("tier").lower()]
    
    # Enrich auction data with additional information
    for a in bin_auctions:
        # Extract item ID and generate image URL
        a["item_tag"] = json.loads(parse_item_bytes(a["item_bytes"])).get("i")[0]["tag"]["ExtraAttributes"]["id"]
        a["item_image"] = f"https://sky.coflnet.com/static/icon/{a['item_tag']}"
        # Format item lore with proper Minecraft styling
        a["item_lore"] = parse_minecraft_text(a["item_lore"])
        
    # Sort auctions by price (lowest first)
    bin_auctions.sort(key=lambda a: a["starting_bid"])
        
    return templates.TemplateResponse("index.html", {
        "request": request,
        "auctions": bin_auctions,
        "query": query or ""
    })