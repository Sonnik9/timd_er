import os
from dotenv import load_dotenv
load_dotenv()

class PARAMS():
    def __init__(self) -> None:
        self.init_all()
        # pass
    
    def init_keys(self):        
        self.api_key  = os.getenv(f"BINANCE_API_PUBLIC_KEY", "")
        self.api_secret = os.getenv(f"BINANCE_API_PRIVATE_KEY", "") 

    def init_default_params(self):
        self.SOLI_DEO_GLORIA = 'Soli Deo Gloria!'
        self.symbol = 'ARBUSDT' #usdt only!!!
        self.depo = 20
        self.sell_mode = 'm' # a -- auto, m -- manual
        self.order_time = "2024-03-01 01:18:00" # "2024-02-29 12:00:00", PORTAL 13:00 (UTC)?
        # //////////////////////////////////////////////////////////////////////
        self.false_start_deprecator = 0 
        self.pause = 2
        attempts_number = 3        
        self.iter_list = list(range(1, attempts_number + 1))  

    def init_all(self):
        self.init_keys()
        self.init_default_params()


         