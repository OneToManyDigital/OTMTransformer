from importlib.metadata import version
import math
import re
import uuid
from . import __version__
from .llmClient import LLMClient,OpenAICOnfig
from pandas import  DataFrame, Series
from .model.company import Company,CharacValue
import logging
import json
import pandas as pd
from .characConstants import * 


LOGGER = logging.getLogger(__name__)


def transform(openAiCOnfig : OpenAICOnfig, companyName: str, companies: DataFrame, sectorDic : DataFrame, subSectorsScrapperDic: DataFrame, 
              companySizeDic : DataFrame, departmentDic: DataFrame, jobList: DataFrame, characDic: DataFrame, 
              characValDic: DataFrame, salaryData: DataFrame = pd.DataFrame() ) -> Company :
   
   additional_info = {
        'charac_id': [C_REMOTE, C_TICKET_RESTO],
        'additional_info': ['The legal is 30 days per year', 'set to "Less than 8€" if no amount is defined']
    }
   df_additional_info = pd.DataFrame(additional_info)
    

   # call llm to extract data :
   clientLLM = LLMClient(openAiCOnfig,characDic, characValDic,df_additional_info )

   LOGGER.info(f'Start to extract data for company {companyName}')
   companies['name'] = companies['name'].str.lower()
   companiesFound = companies[companies['name'] == companyName.lower()]
   LOGGER.info(f'Found in company list this associated companies :')
   LOGGER.info(companiesFound)

   if len(companiesFound) ==0:
      return None

   subSectors=[]
   sectors=[]
   sizeId=None
   characValueList = []
   jobs =jobList[jobList['company'] ==  companyName ]
   benefitsFromJobs=jobs[~jobs['benefits'].isna()]


   for index, row in companiesFound.iterrows():
      sectorsInScrapper = row['sector']
      if sectorsInScrapper is None or (type(sectorsInScrapper) != str and math.isnan(sectorsInScrapper)):  
         LOGGER.info(f'No sector define for companies {companyName}')
         continue
      sec, subSec= extractAndMapSectors(sectorsInScrapper, sectorDic,subSectorsScrapperDic)
      if len(sec) > 0:
         sectors.extend(sec)
      if len(subSec) > 0:
         subSectors.extend(subSec)
      
      socials = row['socials']
      if socials and len(socials) > 0:
         newList = extractSocialData(socials)
         if newList is not None:
            characValueList.extend(newList)
      url = row['url']
      if url and len(url) > 0:
         newList = extractSocialData(url)
         if newList is not None:
            characValueList.extend(newList)


      benefits = row['benefits']
      goodToKnow = row['goodToKnow']
      if len(benefitsFromJobs)  == 0:
         if type(benefits) == str:
            json = clientLLM.extractDataDetails(benefits)
            if json is not None: 
               newList =  mapToCharacValue(json, characDic,characValDic)
               if newList is not None:
                  characValueList.extend(newList)
         if type(goodToKnow) == str:
            json = clientLLM.extractDataDetails(goodToKnow)
            if json is not None: 
               newList =  mapToCharacValue(json, characDic,characValDic)
               if newList is not None:
                  characValueList.extend(newList)

   # if no sectors it not usefull for data compute
   if len(subSectors) == 0:
      return None

   sizeId = extractSize(companiesFound['size'], companySizeDic)

   # Remove duplicates rows
   sectors = list(dict.fromkeys(sectors))
   subSectors = list(dict.fromkeys(subSectors))

   remotePos = None
   
   
   if len(jobs) > 0:
      df_no_duplicates = jobs.drop_duplicates(subset=['id'])

      LOGGER.info(f'Jobs found for {companyName} : {len(df_no_duplicates)}')
      # exrtract remote from var 
      remotePos = computeRemote(df_no_duplicates)
      characValueList.append(CharacValue(characId=C_REMOTE, characValueId=remotePos, positiveValue =getPositiveVal(remotePos, characValDic=characValDic), isMultiple=False))

      job_fitlered = df_no_duplicates[df_no_duplicates['min_amount'].isna()]
      if len(salaryData) > 0 and len(job_fitlered) > 0:
         merged_df = pd.merge(salaryData, df_no_duplicates, left_on='jobId', right_on='id',suffixes=("","_j"))
         if len(merged_df)> 0:
            salaryDataList=[]
            for index, row in merged_df.iterrows():
               # compare salary j_min_amount j_max_amount max_val min_val
               if row['min_amount'] > row['min_val'] and  row['max_amount'] > row['max_val']:
                  salaryDataList.append(2)
               elif row['min_amount'] > row['min_val'] and  row['max_amount'] < row['max_val']:
                  salaryDataList.append(1)
               else:
                  salaryDataList.append(0)   
            mean= round(sum(salaryDataList) / len(salaryDataList)) if len(salaryDataList) > 0 else -1
            idCharacId=CV_SALARY_LOWER
            if mean == 2:
               idCharacId=CV_SALARY_UPPER
            elif mean ==1:
               idCharacId=CV_SALARY_MEAN
            characValueList.append(CharacValue(characId=C_SALARY, characValueId=idCharacId, positiveValue =getPositiveVal(idCharacId, characValDic=characValDic), isMultiple=False))

      
      if len(benefitsFromJobs)  == 0:      
         for index, row in df_no_duplicates.iterrows():
            jobText = row['description']
            json = clientLLM.extractDataDetails(jobText)
            if json is not None:          
               newList =  mapToCharacValue(json, characDic,characValDic)
               if newList is not None:
                  characValueList.extend(newList)


   if len(benefitsFromJobs) > 0:
      newList = getCharacValueFromBenefits(benefitsFromJobs['benefits'], characDic,characValDic)
      if newList is not None:
         characValueList.extend(newList)
   
   characValueList=mergeCharacValue(characValueList)

   result = Company(id = str(uuid.uuid4()), name=companyName,sectors = sectors, subSectors=subSectors, departmens=None, depaCharacValues=characValueList,size= sizeId ,version=__version__)
   LOGGER.info(f'End to extract data for company {companyName} with company {result}' )
   return result

def getPositiveVal(data_charac_id: int, characValDic: DataFrame):
   foundCharacVal = characValDic[characValDic['id'] == data_charac_id]
   if  len(foundCharacVal) > 0 :
       return foundCharacVal['positive_value'].values[0]
   else:
      return 999

def mapToCharacValue( json_str: str, characDic: DataFrame, characValDic: DataFrame) -> list[CharacValue]:
   res = []
   try:
      json_str=json_str.replace("```json", "")
      json_str=json_str.replace("```", "")
      json_str=json_str.replace("\\_", "_")

      data = json.loads(json_str)
      for key in data:
         value = data[key]
         if value is None:
            continue
         found = characDic[characDic['field_json_name'] == key]
         foundCharacVal = characValDic[characValDic['name'] == value]
         if len(found) > 0 and len(foundCharacVal) > 0 :
            elt = found.iloc[0]
            eltVal = foundCharacVal.iloc[0]
            res.append(CharacValue(characId=elt.id, characValueId=eltVal.id, positiveValue =eltVal.positive_value, isMultiple=elt.is_multiple))
   except:
      LOGGER.info(f'Not a json format: {json_str}')
   return res

def mergeCharacValue(characValueList : list[CharacValue]):
   unique_charac_values = {}
   multiple_values  : list[CharacValue] = []
   for charac_value in characValueList:
      if charac_value.isMultiple:
         multiple_values.append(charac_value)
      else:
         if charac_value.characId not in unique_charac_values:
            unique_charac_values[charac_value.characId] = charac_value
         else:
            existing_charac_value = unique_charac_values[charac_value.characId]
            if charac_value.positiveValue > existing_charac_value.positiveValue:
                  unique_charac_values[charac_value.characId] = charac_value

   seen = {}
   finalArray = []
   for item in multiple_values:
      characValueId = item.characValueId
      if characValueId not in seen:
         seen[characValueId] = item
         finalArray.append(item)
   listRes = list(unique_charac_values.values())
   listRes.extend(finalArray)
   return  listRes

def extractSize(sizeInScrapper: list[str], companySizeDic : DataFrame ):
   if len(sizeInScrapper) == 0:
      return None
   numbers=[]
   for size in sizeInScrapper:
      if size is None or (type(size) != str and math.isnan(size)):
         continue
      elif type(size) != str:
         numbers.append(size)
      else:
         found = re.findall(r'\d+', size.strip().replace(" ", ""))
         if len(found) > 0:
            numbers.extend(found)

   # if no number set to size 1
   if len(numbers) == 0:
      return 1

   maxNumber = int(max(numbers))
   sizeId = None
   for index, row in companySizeDic.iterrows():
      if (row['min_val'] < maxNumber and row['max_val'] > maxNumber) or ( row['min_val'] < maxNumber and math.isnan(row['max_val'])):
         sizeId = row['id']
   
   return sizeId 


def extractAndMapSectors(sectorsInScrapper: str, sectorDic: DataFrame, subSectorsScrapperDic: DataFrame) :
   values=sectorsInScrapper.split(',')
   sectors =[]
   subSectors =[]
   for value in values:
      found = subSectorsScrapperDic[subSectorsScrapperDic['name'] == value.strip()]
      if len(found) > 0 :
         elt = found.iloc[0]
         subSectors.append(elt.sub_sector_id)
         subSecor = sectorDic[sectorDic['id'] == elt.sub_sector_id]
         sectors.append(subSecor.iloc[0].sector_id)
      else:
         found = sectorDic[sectorDic['name'] == value.strip()]
         if len(found) > 0: 
            elt = found.iloc[0]
            subSectors.append(elt.id)
            sectors.append(elt.sector_id)
         else:
            LOGGER.info(f'Sectors {value} not found')
         
   return sectors, subSectors


def computeRemote(jobs : DataFrame):
   resIsRemote = False
   detailRemote= []
   for index, row in jobs.iterrows():
      isRemote = row['is_remote']
      if isRemote is True:
         resIsRemote = True
      details = row['remote_details']
      if type(details) == str:
         detailRemote.append(details)
   detailRemote = [value for value in detailRemote if value]
   if resIsRemote and len(detailRemote) == 0:
      return CV_12_REMOTE
   elif len(detailRemote) > 0:
      LOGGER.info(f'found details remote {detailRemote}')
      if 'Télétravail total' in detailRemote or 'full' in detailRemote:
         return CV_FULL_REMOTE
      elif 'Télétravail fréquent' in detailRemote or 'frequent' in detailRemote:
         return CV_34_REMOTE
      elif 'Télétravail occasionnel' in detailRemote or 'occasionnel' in detailRemote:
         return CV_OCC_REMOTE
      else:
         return CV_NO_REMOTE
   else:
      return CV_NO_REMOTE

def getCharacValueFromBenefits( benefits :Series,characDic: DataFrame,  characValDic: DataFrame ):

   characValueList=[]
   listAll_benefits=[]
   for benefit in benefits:
      if benefit is None or benefit == '' :
         continue
      splitBenef = benefit.split(",")
      listAll_benefits.extend(splitBenef)
   unique_list = list(set([item.strip() for item in listAll_benefits]))
   for benefit in unique_list:
      benefit=benefit.strip()
      charIdVal= get_charIdVal(benefit)
      if charIdVal:
         foundVal = characValDic[characValDic['id'] == charIdVal]
         if not foundVal.empty:
               found = characDic[characDic['id'] == foundVal['charac_id'].values[0]]
               if not found.empty:
                  characValueList.append(CharacValue(
                     characId=foundVal['charac_id'].values[0], 
                     characValueId=charIdVal, 
                     positiveValue=getPositiveVal(charIdVal, characValDic=characValDic), 
                     isMultiple=found['is_multiple'].values[0]
                  ))   

   return sorted(characValueList, key=lambda x: x.characId)



def extractSocialData( socials: str )-> list[CharacValue]: 
   socialList = socials.split(', ')
   mapped_socials = []
   for url in socialList:
      characValueId=get_url_mapping(url)
      mapped_socials.append(CharacValue(characId=C_SOCIALS, characValueId=characValueId, positiveValue =-2, isMultiple=True))
   return mapped_socials
