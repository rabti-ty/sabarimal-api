import argparse
import shortuuid
from datetime import datetime
import pytz
from utils import get_redis_key, get_master_client
import time

def getPrefix():
    prefix = ''
    IST = pytz.timezone('Asia/Kolkata')
    year = datetime.now(IST).year
    month = datetime.now(IST).month
    if month == 1:
        prefix = 'A'
    elif month == 2:
        prefix = 'B'
    elif month == 3:
        prefix = 'C'
    elif month == 4:
        prefix = 'D'
    elif month == 5:
        prefix = 'E'
    elif month == 6:
        prefix = 'F'
    elif month == 7:
        prefix = 'G'
    elif month == 8:
        prefix = 'H'
    elif month == 9:
        prefix = 'I'
    elif month == 10:
        prefix = 'J'
    elif month == 11:
        prefix = 'K'
    elif month == 12:
        prefix = 'L'

    yprefix = year - 2023
    prefix = prefix+str(yprefix)
    return prefix

def getPassNo():
    x = shortuuid.ShortUUID().random(length=8) 
    prefix = getPrefix()
    pass_no = prefix+x
    return pass_no

if __name__ == "__main__":
    startTime = time.time()
    parser = argparse.ArgumentParser()  
    parser.add_argument("-y", "--year", help = "Year for which the pass no is to be generated", type=int, choices=range(2023,2026), required = True)
    parser.add_argument("-m", "--month", help = "Month for which the pass no is to be generated [1-12]", type=int, required = True, choices=range(1,12))
    parser.add_argument("-c", "--count", help = "Number of pass numbers to be generated[1-100000]", type=int, required = True)
    args = parser.parse_args()
 
    # Parsing the arguments
    year = args.year
    month = args.month
    pass_count = args.count   

    redis_key_universal_set = get_redis_key('up',[str(year),str(month)],'m',':',1)
    redis_key_remaining_set = get_redis_key('rp',[str(year),str(month)],'m',':',1)
    print(f"Redis key is {redis_key_universal_set}")
    print(f"Redis key is {redis_key_remaining_set}")
    master_redis_client = get_master_client()

    for i in range(0,pass_count):
        pass_no = getPassNo()
        print(f"Pass No is {pass_no}")
        add_resp = master_redis_client.sadd(redis_key_universal_set,pass_no)
        print(f"Resposnse : {add_resp}")
        if int(add_resp) == 1:
            master_redis_client.sadd(redis_key_remaining_set,pass_no)

    executionTime = (time.time() - startTime)
    IST = pytz.timezone('Asia/Kolkata')
    end_timestamp = datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S')
    print(f"Ceate Pass No Service took {round(executionTime/60,2)} min to add {pass_count} pass numbers")
