import logging
import math
import pandas as pd

LOGGER = logging.getLogger(__name__)

def test_help():
    # loas company scrapper
    companies = pd.read_csv('./tests/cpy_scrapper.csv')
    
    # Load sub sectors 
    sub_sectors = pd.read_csv('./tests/sub_sectors.csv')
    sectorDic=  pd.read_csv('./tests/sub_sector_scrapper_dic.csv')
    
    notFoundSectors =[]
    for index, row in companies.iterrows():
        sectorsInScrapper = row['sector']
        if sectorsInScrapper is None or (type(sectorsInScrapper) != str and math.isnan(sectorsInScrapper)):  
            continue
        values=sectorsInScrapper.split(',')
        for value in values:
            found = sub_sectors[sub_sectors['name'] == value.strip()]
            if len(found) == 0 :
                found = sectorDic[sectorDic['name'] == value.strip()]
                if len(found) == 0: 
                    notFoundSectors.append(value)
    unique_list = []
    seen = set()
    for item in notFoundSectors:
        if item not in seen:
            unique_list.append(item)
            seen.add(item)
    LOGGER.info(unique_list)