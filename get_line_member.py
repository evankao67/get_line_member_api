import requests
import json
import sys
import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger()
# #filehandler = TimedRotatingFileHandler('/data01/etl/script/yulon/logs/yulon_ftp.log', 'D', 1, 60)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# filehandler.setFormatter(formatter)
# logger.addHandler(filehandler)
#local_abs_path ="/data01/etl/brand_data/yulon"

if len(sys.argv) == 2:
    site_id = sys.argv[1]
else:
    #logger.exception('shell input type wrong')
    raise Exception ('shell input type wrong')


def get_line_member(url, payload, headers):
    line_number = 0
    try:
        response = requests.request("GET", url, headers=headers, data=payload).json()
        line_number = line_number + len(response["userIds"])
    except Exception as e:
        print(e)
        logger.exception("get first page data failed", e)
        
    try:  
        while len(response) == 2:
            new_url = url + "start=" + response["next"]
            response = requests.request("GET", new_url, headers=headers, data=payload).json()
            line_number = line_number + len(response["userIds"])
    except Exception as e:
        print(e)
        logger.exception("get next page data failed", e)
        
    return line_number

if __name__ == '__main__':
    try:
        with open('line_channel_access_token_' + site_id + '.json', 'r') as f:
            API_CONFIG = json.loads(f.read())
    except:
        print('config file : line_channel_access_token_' + site_id + '.json not found')
        logger.exception('config file : api_config_' + site_id + '.json not found')
        raise Exception ('config file : line_channel_access_token_' + site_id + '.json not found')
    
    total_number = get_line_member(API_CONFIG["url"], API_CONFIG["payload"], API_CONFIG["headers"])
    print(total_number)
   
