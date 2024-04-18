from importlib.metadata import version
import math
import re
import uuid
from . import __version__
from .llmClient import LLMClient
from pandas import  DataFrame, Series
from .model.company import Company,CharacValue
import logging
import json

LOGGER = logging.getLogger(__name__)


def transform(companyName: str, companies: DataFrame, sectorDic : DataFrame, subSectorsScrapperDic: DataFrame, 
              companySizeDic : DataFrame, departmentDic: DataFrame, jobList: DataFrame, characDic: DataFrame, characValDic: DataFrame) -> Company :
   
   # call llm to extract data :
   clientLLM = LLMClient(apiKey="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")

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

      benefits = row['benefits']
      goodToKnow = row['goodToKnow']

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

   jobs =jobList[jobList['company'] ==  companyName ]
   if len(jobs) > 0:
      LOGGER.info(f'Jobs found for {companyName} : {len(jobs)}')
      # exrtract remote from var 
      remotePos = computeRemote(jobs)
      characValueList.append(CharacValue(characId=1, characValueId=remotePos, positiveValue =999))

      for index, row in jobs.iterrows():
         jobText = row['description']
         json = clientLLM.extractDataDetails(jobText)
         if json is not None:          
            newList =  mapToCharacValue(json, characDic,characValDic)
            if newList is not None:
               characValueList.extend(newList)

   characValueList=mergeCharacValue(characValueList)

   result = Company(id = str(uuid.uuid4()), name=companyName,sectors = sectors, subSectors=subSectors, departmens=None, depaCharacValues=characValueList,size= sizeId ,version=__version__)
   LOGGER.info(f'End to extract data for company {companyName} with company {result}' )
   return result


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
            res.append(CharacValue(characId=elt.id, characValueId=eltVal.id, positiveValue =eltVal.positive_value))
   except:
      LOGGER.info(f'Not a json format: {json_str}')
   return res

def mergeCharacValue(characValueList : list[CharacValue]):
   unique_charac_values = {}
   for charac_value in characValueList:
      if charac_value.characId not in unique_charac_values:
         unique_charac_values[charac_value.characId] = charac_value
      else:
         existing_charac_value = unique_charac_values[charac_value.characId]
         if charac_value.positiveValue > existing_charac_value.positiveValue:
               unique_charac_values[charac_value.characId] = charac_value
   return list(unique_charac_values.values())

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
   """
   (1,'Présentielle'),
   (2,'Télétravail occasionnel (rendez-vous médicaux, attente d''une livraison) ou de circonstances exceptionnelles')
   (101,'Télétravail partiel ou hybride strictement inférieur à 2j par semaine')
   (102,'Télétravail partiel ou hybride supérieur ou égale à 2j par semaine)
   """
   
   resIsRemote = False
   detailRemote= []
   for index, row in jobs.iterrows():
      isRemote = row['is_remote']
      if isRemote is True:
         resIsRemote = True
      details = row['remote_details']
      if type(details) == str:
         detailRemote.append(details)
   
   if resIsRemote and len(detailRemote) == 0:
      return 102
   elif len(detailRemote) > 0:
      LOGGER.info(f'found details remote {detailRemote}')
      if 'Télétravail total' in detailRemote:
         return 102
      elif 'Télétravail fréquent' in detailRemote:
         return 101
      elif 'Télétravail occasionnel' in detailRemote:
         return 2
      else:
         return 1
   else:
      return 1
   