import sched
import time
from api_binance import BINANCE_API
from utils import UTILS
import logging, os, inspect
logging.basicConfig(filename='log.log', level=logging.INFO)
current_file = os.path.basename(__file__)

class FATHER(BINANCE_API, UTILS):
    def __init__(self) -> None:
        super().__init__()

    def sell_template(self, symbol, sell_qnt):
        response_data_list = [] 
        sell_success_flag = False             
        for _ in self.iter_list:  
            try:            
                response = None              
                side = 'SELL'                
                response = self.place_market_order(symbol, side, sell_qnt)
                response = response.json()
                response_data_list.append(response)                
                try:
                    if response["status"] == "FILLED": 
                        print('The sell order was fulfilled succesfully!') 
                        sell_success_flag = True                                                        
                        break                                              
                except Exception as ex:                    
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
                print("Some problems with placing the sell order")                 
                time.sleep(0.05)           
            except Exception as ex:                
                logging.exception(
                    f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
        return response_data_list, sell_success_flag
    
    def buy_template(self, symbol, buy_qnt):

        response_data_list = []
        response_success_list = [] 

        for _ in self.iter_list:  
            try:            
                response = None              
                side = 'BUY'                
                response = self.place_market_order(symbol, side, buy_qnt)
                response = response.json()
                response_data_list.append(response)                
                try:
                    if response["status"] == "FILLED": 
                        response_success_list.append(response) 
                        print('The buy order was fulfilled succesfully!')                                  
                    break                                              
                except Exception as ex:
                    # print(ex)                
                    if response["code"] == -1121: 
                        time.sleep(0.1)                           
                        continue
                    break                
            except Exception as ex:
                # print(ex)
                pass
                
        return response_data_list, response_success_list

    def strategy(self):
        import math
        response_data_list, response_success_list = [], []
        buy_qnt, quantity_precision = self.usdt_to_qnt_converter(self.symbol, self.depo)
        print(f"buy_qnt: {buy_qnt}")
        response_data_list, response_success_list = self.buy_template(self.symbol, buy_qnt) 
        self.json_writer(self.symbol, response_data_list)        
        if len(response_success_list) != 0:
            qnt_to_sell_start = math.floor(float(response_success_list[0]["fills"][0]["qty"]) * 10**quantity_precision) / 10**quantity_precision 
            print(f"qnt_to_sell_start: {qnt_to_sell_start}")           
            left_qnt = qnt_to_sell_start
            if self.sell_mode == 'a':
                time.sleep(self.pause)
                response_data_list_item, sell_success_flag = self.sell_template(self.symbol, qnt_to_sell_start)
                response_data_list += response_data_list_item
            elif self.sell_mode == 'm':
                stop_selling = False                
                qnt_percent_pieces_left = 100
                while True:
                    if not stop_selling:
                        qnt_percent_pieces = input(f"Are you sure you want to sell {self.symbol}? If yes, tub a pieces qty. Opposite tub 'n' (%) (e.g.: 100, 75, 50... or n)",)  
                        try:                                      
                            qnt_percent_pieces = int(qnt_percent_pieces.strip())
                            qnt_percent_pieces_left = qnt_percent_pieces_left - qnt_percent_pieces
                            if qnt_percent_pieces_left < 0:
                                qnt_percent_pieces_left = qnt_percent_pieces_left + qnt_percent_pieces
                                print(f'Please enter a valid data. There are {qnt_percent_pieces_left} pieces left to sell')
                                continue                              
                        except:
                            print('Selling session was deprecated. Have a nice day!')
                            break
                        try:
                            stop_selling = qnt_percent_pieces_left == 0        
                            qnt_multipliter = qnt_percent_pieces/100
                            qnt_to_sell = math.floor(qnt_to_sell_start* qnt_multipliter * 10**quantity_precision) / 10**quantity_precision                            
                            print(f"qnt_to_sell: {qnt_to_sell}")
                            response_data_list_item, sell_success_flag = self.sell_template(self.symbol, qnt_to_sell)
                            response_data_list += response_data_list_item  
                            if sell_success_flag:
                               left_qnt = left_qnt - qnt_to_sell  
                            else:
                                qnt_percent_pieces_left = qnt_percent_pieces_left + qnt_percent_pieces
                            print(f"Trere are {qnt_percent_pieces_left} pieces and {left_qnt} qty left to sell")                       
                        except Exception as ex:                
                            logging.exception(
                                f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")                                   
                        continue
                    break
               
            self.json_writer(self.symbol, response_data_list)    
            result_time = self.show_trade_time(response_data_list)
            print(result_time) 
            print(self.SOLI_DEO_GLORIA)           
        else:
            print('Some problems with placing buy market order...')

    def schedule_order_execution(self):
        print('God blass you Nik!')                
        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler.enterabs(time.mktime(time.strptime(self.order_time, "%Y-%m-%d %H:%M:%S")), 1, self.strategy)
        scheduler.run()

def main():   
    father = FATHER()  
    father.schedule_order_execution()  

if __name__=="__main__":
    main()
