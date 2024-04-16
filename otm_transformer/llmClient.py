import time
from openai import OpenAI
import logging
from .model.company import CharacValue 
import json

LOGGER = logging.getLogger(__name__)

class LLMClient():
    def __init__(self, apiKey , base_url = None ):
        """
        Initializes LLMClient 
        """

        ## default calling hugging face 
        if apiKey is None:
            LOGGER.error("Cannot init LLMClient without api key in param")
        self.api_key = apiKey
        if base_url is None:
            self.base_url = "https://api-inference.huggingface.co/v1"
        else:
            self.base_url = base_url
        self.client = OpenAI(
            base_url=self.base_url,  # replace with your endpoint url
                api_key=apiKey,   # this is also the default, it can be omitted
            )


    TEMPLATE_JOBS_PROMPT= '''
You are now French AI Extractor.You are processing company job position.

Do not mix up  training days (jours de formation) , holidays (congés) and telecommuting (télétravail). 

Extract specified values from the source text. 
Return answer as JSON object with following fields. Don't add extract comment. Respect the possible value,  if not specify in text put null value:
- "holidays" <"Légal" |"Supérieurs au légal" | null> (The legal is 30 days per year )
- "arranged_schedules" <"Horaire stricte"|"Heure d'arrivée et de départ flexible"|"Flexibilité totale des horaires"  | null >
- "working_place" <"Non flexible" |"Flexible"  | null>
- "parental_leave" <"Légal" |"Supérieurs au légal"  | null>
- "training" <"Pas de programme de formation"|"Plan de formation à la demande de l'employé"|"Accès à des bases de données de formation"|"Programme de formation contenue"  | null>
- "coaching_mentorat" <"Aucun coaching/mentorat"|"Session de coaching / mentorat à la demande"|"Session de coaching / mentorat régulièrement"| null>
- "after_work" <"Jamais"|"Afterwork une fois par trimestre" | "Afterwork au moins une fois par mois non payé par l'entreprise" | "Afterwork au moins une fois par mois payé par l'entreprise" | null >
- "team_building" <"Non" |"Déjeuner d'équipe"|"Journée d'équipe" | "Voyages d'équipe" | null>
- "nap_room" <boolean | null>
- "sport" < "Rien n'est proposé aux salariés" | "Salle de sport dans les locaux" | "Carte de sport" | "Fianncement abonnenment de sport" | null>
- "teleworking_allowance" <boolean  | null>
- "complementary_health" <"Légal"|"Au dessus du légal"|"100%" | null >
- "restaurant_card" <"Non" |"Moins de 8€"|"Entre 8€ et 10€"|"Supérieur à 10€" | null > (set to "Less than 8€" if no amount is defined)
- "comapny_car" < "Oui"|"Choix de la voiture"| null>
- "company_smartphone" <"Oui"|"Choix du mobile"| null>
- "computer_choice" <boolean | null>
- "bonus_interest" <boolean | null>

Do not infer any data based on previous training, strictly use only source text given below as input.
========
{description}
========
''' 

    TEMPLATE_DETAILS_PROMPT= '''You are now French AI Extractor.You are processing company description.

Do not mix up  training days (jours de formation) , holidays (congés) and telecommuting (télétravail). 

Extract specified values from the source text. 
Return answer as JSON object with following fields. Don't add extract comment. Respect the possible value,  if not specify in text put null value:
- "holidays" <"Légal" |"Supérieurs au légal" | null> (The legal is 30 days per year )
- "arranged_schedules" <"Horaire stricte"|"Heure d'arrivée et de départ flexible"|"Flexibilité totale des horaires"  | null >
- "working_place" <"Non flexible" |"Flexible"  | null>
- "parental_leave" <"Légal" |"Supérieurs au légal"  | null>
- "training" <"Pas de programme de formation"|"Plan de formation à la demande de l'employé"|"Accès à des bases de données de formation"|"Programme de formation contenue"  | null>
- "coaching_mentorat" <"Aucun coaching/mentorat"|"Session de coaching / mentorat à la demande"|"Session de coaching / mentorat régulièrement"| null>
- "after_work" <"Jamais"|"Afterwork une fois par trimestre" | "Afterwork au moins une fois par mois non payé par l'entreprise" | "Afterwork au moins une fois par mois payé par l'entreprise" | null >
- "team_building" <"Non" |"Déjeuner d'équipe"|"Journée d'équipe" | "Voyages d'équipe" | null>
- "nap_room" <boolean | null>
- "sport" < "Rien n'est proposé aux salariés" | "Salle de sport dans les locaux" | "Carte de sport" | "Fianncement abonnenment de sport" | null>
- "teleworking_allowance" <boolean  | null>
- "complementary_health" <"Légal"|"Au dessus du légal"|"100%" | null >
- "restaurant_card" <"Non" |"Moins de 8€"|"Entre 8€ et 10€"|"Supérieur à 10€" | null > (set to "Less than 8€" if no amount is defined)
- "comapny_car" < "Oui"|"Choix de la voiture"| null>
- "company_smartphone" <"Oui"|"Choix du mobile"| null>
- "computer_choice" <boolean | null>
- "bonus_interest" <boolean | null>

Do not infer any data based on previous training, strictly use only source text given below as input.
========
{description}
========
'''

    def extractDataDetails(self, description):
        return self.extractData(self.TEMPLATE_DETAILS_PROMPT,description) 
    
    def extractDataJobPosition(self, description):
        return self.extractData(self.TEMPLATE_JOBS_PROMPT,description) 

    def extractData(self, promtTemplate: str, description: str): 
        q = promtTemplate.format(description=description)

        retry_delays = [1, 10, 60, 600, 1200, 3600]  # 1 sec, 10 sec, 1 min, 10 min, 20 min, 1 heure

        max_attempts = len(retry_delays)  # Nombre maximal de tentatives

        success = False
        attempt = 1

        while not success and attempt <= max_attempts:
            try:
                # Code à essayer
            # print("Tentative", attempt)
                        
                completion = self.client.chat.completions.create(
                #model="gpt-3.5-turbo", 
                model="mistralai/Mixtral-8x7B-Instruct-v0.1",
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
    
