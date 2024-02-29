import hmac
import hashlib
import requests
import time
import pandas as pd
import time
from decimal import Decimal
from init_params import PARAMS

class BINANCE_API(PARAMS):
    def __init__(self):
        super().__init__()
    # POST ////////////////////////////////////////////////////////////////////
    def get_url_market_query(self, symbol, side, quantity):
        base_url = "https://api.binance.com/api/v3/order"
        timestamp = int(time.time() * 1000)
        query_string = f"symbol={symbol}&side={side}&type=MARKET&quantity={quantity}&timestamp={timestamp}&recvWindow=5000"
        signature = hmac.new(self.api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        return f"{base_url}?{query_string}&signature={signature}"

    def place_market_order(self, symbol, side, qnt):               
        url = self.get_url_market_query(symbol, side, qnt)            
        return requests.post(url, headers={'X-MBX-APIKEY': self.api_key})

    # GET /////////////////////////////////////////////////////////////////////////////////

    def get_exchange_info(self, symbol):
        url = f"https://api.binance.com/api/v3/exchangeInfo?symbol={symbol}"
        try:
            exchange_info = requests.get(url)
            return exchange_info.json()        
        except Exception as ex:
            print(ex)
            return

    def get_current_price(self, symbol):    
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        try:
            response = requests.get(url)
            data = response.json()
            return float(data["price"])
        except Exception as ex:
            print(ex)
            return

    # UTILS /////////////////////////////////////////////////////////////////////////////////////////////////
    def usdt_to_qnt_converter(self, symbol, depo):
        try:        
            symbol_info = self.get_exchange_info(symbol)                     
            symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)     
            lot_size_filter = next((f for f in symbol_data.get('filters', []) if f.get('filterType') == 'LOT_SIZE'), None)
            step_size = str(float(lot_size_filter.get('stepSize')))      
            quantity_precision = Decimal(step_size).normalize().to_eng_string()        
            quantity_precision = len(quantity_precision.split('.')[1])  
            minNotional = float(next((f['minNotional'] for f in symbol_data['filters'] if f['filterType'] == 'NOTIONAL'), None))
            maxNotional = float(next((f['maxNotional'] for f in symbol_data['filters'] if f['filterType'] == 'NOTIONAL'), None))    
            price = self.get_current_price(symbol)
            if depo <= minNotional:
                depo = minNotional               
            elif depo >= maxNotional:
                depo = maxNotional        
            return round(depo / price, quantity_precision), quantity_precision
        except Exception as ex:
            print(ex) 
            return None, None
