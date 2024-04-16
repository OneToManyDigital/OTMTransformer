
import logging
from otm_transformer import transformCpy
import pandas as pd

LOGGER = logging.getLogger(__name__)

def test_help():
    # loas company scrapper
    companies = pd.read_csv('./tests/cpy_scrapper.csv')
    
    # Load sub sectors 
    sub_sectors = pd.read_csv('./tests/sub_sectors.csv')
    
    # Load company_size 
    company_size = pd.read_csv('./tests/cpy_size_dic.csv')
    
    # Load sub sector scrapper 
    sub_sectors_scrapper = pd.read_csv('./tests/sub_sector_scrapper_dic.csv')
    
    # Load sub sector scrapper 
    jobs_list = pd.read_csv('./tests/jobs_list.csv', low_memory=False)
    # Load characDic
    characDic = pd.read_csv('./tests/dic_charac.csv', low_memory=False)
    # Load characValDic
    characValDic = pd.read_csv('./tests/dic_charac_value.csv', low_memory=False)
    
    data =companies.sample(1).iloc[0]
    LOGGER.info(data)
    res = transformCpy.transform(data['name'], companies,sub_sectors, sub_sectors_scrapper,company_size , None, jobs_list, characDic, characValDic)
    assert res is not None
    assert res.id is not None
    assert res.name== "Sopra Steria"