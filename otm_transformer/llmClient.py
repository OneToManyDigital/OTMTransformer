import time
from openai import OpenAI
import logging
import pandas as pd
from pandas import DataFrame
from .characConstants import *

LOGGER = logging.getLogger(__name__)





class OpenAICOnfig():
    def __init__(self, apiKey , organization='org-BOSwCwpi8tnFwhFc3SO6opEy', project='proj_QXiReNihxPYbwgi45LYKqveK', base_url = None , model = "gpt-4o"):
        if apiKey is None:
            LOGGER.error("Cannot init LLMClient without api key in param")
            raise ValueError("The 'Open ai key' parameter is missing or empty")
        self.api_key = apiKey
        if base_url is None:
            self.base_url =  "https://api.openai.com/v1"
        else:
            self.base_url = base_url
        self.model = model
        self.organization = organization
        self.project = project

class LLMClient():
    def __init__(self, config : OpenAICOnfig, characDic: DataFrame, characValDic: DataFrame, df_additional_info):
        """
        Initializes LLMClient 
        """

        ## default calling hugging face 
        self.config = config
        self.client = OpenAI(
            base_url=config.base_url,  # replace with your endpoint url
            api_key=config.api_key,   # this is also the default, it can be omitted
            organization=config.organization,
            project=config.project,
            )
        self.json_model=self.constrcut_json_template(characDic, characValDic, df_additional_info)

    def constrcut_json_template(self, characDic: DataFrame, characValDic: DataFrame, df_additional_info):
        df_merged = pd.merge(characValDic,characDic , left_on='charac_id', right_on='id', how='left')
        df_merged = pd.merge(df_merged, df_additional_info, left_on='charac_id', right_on='charac_id', how='left')
        grouped = df_merged.groupby('charac_id')
        
        # Filter remote and salary not get by llm 
        filter_id_list =[C_REMOTE, C_SALARY ]

        result = []
        for name, group in grouped:
            field_name = group['field_json_name'].iloc[0]
            id = group['id_y'].iloc[0]
            if  pd.notna(field_name) and field_name and id not in filter_id_list :
                values = ' | '.join([f'"{name}"' for name in self.filterName(group['name_x'])])
                additional_info = group['additional_info'].iloc[0]
                array_indicator = "Arrays of " if group['is_multiple'].iloc[0] else ""
                additional_info_str = f"({additional_info})" if pd.notna(additional_info) and additional_info else ""
                result.append(f'- "{field_name}" {array_indicator}< {values} | null > {additional_info_str}')
        
        return '\n'.join(line.rstrip() for line in result )
    
    def filterName(self,names ):
        result = []
        for name in names:
            extractName=name['fr']
            if extractName != 'RAS':
                result.append(extractName)
        return result


    
    TEMPLATE_JOBS_PROMPT= '''
You are now French AI Extractor.You are processing company job position.

Do not mix up  training days (jours de formation) , holidays (congés) and telecommuting (télétravail). 


Extract specified values from the source text. 
Return answer as JSON object with following fields. Don't add extract comment. Respect the possible value,  if not specify in text put null value:
{json_model}


Do not infer any data based on previous training, strictly use only source text given below as input.
========
{description}
========
''' 

    TEMPLATE_DETAILS_PROMPT= '''You are now French AI Extractor.You are processing company description.

Do not mix up  training days (jours de formation) , holidays (congés) and telecommuting (télétravail). 

Extract specified values from the source text. 
Return answer as JSON object with following fields. Don't add extract comment. Respect the possible value,  if not specify in text put null value:
{json_model}

Do not infer any data based on previous training, strictly use only source text given below as input.
========
{description}
========
'''

    def extractDataDetails(self, description):
        return self.extractData(self.TEMPLATE_DETAILS_PROMPT,description) 
    
    def extractDataJobPosition(self, description):
        return self.extractData(self.TEMPLATE_JOBS_PROMPT,description) 

    def formatPrompt(self , promtTemplate: str, description: str):
        return promtTemplate.format(description=description, json_model= self.json_model)
    
    def extractData(self, promtTemplate: str, description: str): 
        q = self.formatPrompt(promtTemplate, description)

        retry_delays = [1, 10, 60, 600, 1200, 3600]  # 1 sec, 10 sec, 1 min, 10 min, 20 min, 1 heure

        max_attempts = len(retry_delays)  # Nombre maximal de tentatives

        success = False
        attempt = 1
        while not success and attempt <= max_attempts:
            try:
                        
                completion = self.client.chat.completions.create(
                model=  self.config.model, 
                messages=[{"role": "user", "content": q}],
                max_tokens=500)
                success = True  # La condition de réussite est remplie

            except Exception as e:
                # Code exécuté en cas d'échec
                LOGGER.error("Échec:", e)
                if attempt < max_attempts:
                    # Utilisation des délais de temporisation spécifiés
                    retry_delay = retry_delays[attempt - 1]
                    LOGGER.info("Nouvelle tentative dans {} secondes.".format(retry_delay))
                    time.sleep(retry_delay)
            finally:
                attempt += 1

        if success:
            LOGGER.debug("Opération réussie !")
        else:
            LOGGER.error("Nombre maximal de tentatives atteint. Opération échouée.")
        return completion.choices[0].message.content
    
