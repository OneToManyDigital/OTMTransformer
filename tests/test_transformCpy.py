
import logging
from otm_transformer import transformCpy
from otm_transformer.llmClient import OpenAICOnfig
import pandas as pd
from deltalake import DeltaTable
import deltalake


LOGGER = logging.getLogger(__name__)

def test_help():

    dt = DeltaTable(
        # Change this to your unique URI from a previous step
        # if you’re using your own AWS credentials.
        's3://datalake-otm/datalake-bucket/jobs',
        storage_options={
            'AWS_ACCESS_KEY_ID': 'TO CHANGE',
            'AWS_SECRET_ACCESS_KEY': 'TO CHANGE',
            'AWS_REGION': 'fr-par',
            'endpoint_url': 'https://s3.fr-par.scw.cloud'
    
        },
        )
    df = dt.to_pandas()
    dt = DeltaTable(
        # Change this to your unique URI from a previous step
        # if you’re using your own AWS credentials.
        's3://datalake-otm/datalake-bucket/company',
        storage_options={
            'AWS_ACCESS_KEY_ID': 'TO CHANGE',
            'AWS_SECRET_ACCESS_KEY': 'TO CHANGE',
            'AWS_REGION': 'fr-par',
            'endpoint_url': 'https://s3.fr-par.scw.cloud'
    
        },
        )
    df_cpy = dt.to_pandas()
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
    # Load salary  scrapper 
    salary_scrapper = pd.read_csv('./tests/salary.csv')
    data =companies.sample(1).iloc[0]
    config = OpenAICOnfig(  apiKey="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", base_url="https://api-inference.huggingface.co/v1", model="mistralai/Mixtral-8x7B-Instruct-v0.1")
 

    res = transformCpy.transform(config, 'Société Générale', df_cpy,sub_sectors, sub_sectors_scrapper,company_size , None, df, characDic, characValDic,salary_scrapper)


    LOGGER.info(res.model_dump(mode='json'))
    assert res is not None
    assert res.id is not None
    assert res.name== "Sopra Steria"