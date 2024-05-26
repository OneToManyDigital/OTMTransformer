import pandas as pd
import pytest
from otm_transformer.llmClient import LLMClient, OpenAICOnfig

@pytest.fixture
def sample_data():
    data = {
        'id': [5, 5, 5, 2, 2, 3],
        'charac_id': [5, 5, 5, 2, 2, 3],
        'name': ["{'fr': 'Congés payés'}" ,"{'fr': 'RTT'}","{'fr': 'Congé sabatique'}", "{'fr': 'Horaire de travail stricte'}", "{'fr': 'Heure d\'arrivée et de départ flexible'}", "{'fr': 'Non flexible'}"]
    }
    df_main = pd.DataFrame(data)
    
    metadata = {
        'id': [5, 2, 3],
        'is_multiple': [True, False, False],
        'field_json_name': ['holidays', 'arranged_schedules', 'working_place'],
        'name' : ['holidays', 'arranged_schedules', 'working_place']
    }
    df_metadata = pd.DataFrame(metadata)
    
    additional_info = {
        'charac_id': [5, 2, 3],
        'additional_info': ['The legal is 30 days per year', '', '']
    }
    df_additional_info = pd.DataFrame(additional_info)
    
    return df_main, df_metadata, df_additional_info

@pytest.fixture
def edge_case_data():
    data = {
        'id': [5, 5, 2],
        'charac_id': [5, 5, 2],
        'name': ["{'fr': 'Congés payés'}" ,"{'fr': 'RTT'}", "{'fr': 'Horaire de travail stricte'}"]
    }
    df_main = pd.DataFrame(data)
    
    metadata = {
        'id': [5, 2],
        'is_multiple': [True, False],
        'field_json_name': ['holidays', 'arranged_schedules'],
        'name' : ['holidays', 'arranged_schedules']
    }
    df_metadata = pd.DataFrame(metadata)
    
    additional_info = {
        'charac_id': [5, 2],
        'additional_info': ['', '']
    }
    df_additional_info = pd.DataFrame(additional_info)
    
    return df_main, df_metadata, df_additional_info

@pytest.fixture
def csv_case_data():

    # Load characDic
    characDic = pd.read_csv('./tests/dic_charac.csv', low_memory=False)
    # Load characValDic
    characValDic = pd.read_csv('./tests/dic_charac_value.csv', low_memory=False)
    additional_info = {
        'charac_id': [1],
        'additional_info': ['The legal is 30 days per year'
                        ]
    }
    df_additional_info = pd.DataFrame(additional_info)
    
    return characValDic, characDic, df_additional_info

def test_construct_string_simple(sample_data):
    df_main, df_metadata, df_additional_info = sample_data
    output = LLMClient(OpenAICOnfig("Random"),df_metadata,df_main, df_additional_info)
    
    expected_output = (
        '- "arranged_schedules" < "Horaire de travail stricte" | "Heure d\'arrivée et de départ flexible" | null >\n'
        '- "working_place" < "Non flexible" | null >\n'
        '- "holidays" Arrays of < "Congés payés" | "RTT" | "Congé sabatique" | null > (The legal is 30 days per year)'
    )

    # Strip trailing whitespace for comparison
    output_stripped = '\n'.join(line.rstrip() for line in output.json_model.split('\n'))
    expected_output_stripped = '\n'.join(line.rstrip() for line in expected_output.split('\n'))
    
    assert output_stripped == expected_output_stripped

def test_construct_string_edge_case(edge_case_data):
    df_main, df_metadata, df_additional_info = edge_case_data
    output = LLMClient(OpenAICOnfig("Random"),df_metadata,df_main, df_additional_info)
    
    expected_output = (
        '- "arranged_schedules" < "Horaire de travail stricte" | null >\n'
        '- "holidays" Arrays of < "Congés payés" | "RTT" | null >' 
    )
    
    # Strip trailing whitespace for comparison
    output_stripped = '\n'.join(line.rstrip() for line in output.json_model.split('\n'))
    expected_output_stripped = '\n'.join(line.rstrip() for line in expected_output.split('\n'))
    
    assert output_stripped == expected_output_stripped

def test_construct_string_csv_data_case(csv_case_data):
    df_main, df_metadata, df_additional_info = csv_case_data
    output = LLMClient(OpenAICOnfig("Random"),df_metadata,df_main, df_additional_info)
    
    expected_output = (
         '- "arranged_schedules" < "Horaire de travail stricte" | null >\n'
        '- "holidays" Arrays of < "Congés payés" | "RTT" | null >'
    
    )
    
    # Strip trailing whitespace for comparison
    output_stripped = '\n'.join(line.rstrip() for line in output.json_model.split('\n'))
    expected_output_stripped = '\n'.join(line.rstrip() for line in expected_output.split('\n'))
    
    assert output_stripped == """- "arranged_schedules" < "Heure d'arrivée et de départ flexible" | "Flexibilité totale des horaires" | "Horaire de travail stricte" | null >
- "holidays" Arrays of < "Congés payés" | "RTT" | "Congé sabatique" | "Jours de bénévolat offers" | "Congé vacances illimitées" | "Congés payés supplémentaires" | null >
- "working_place" < "Non flexible" | "Télétravail uniquement de chez soi" | "Télétravail de n'importe où" | null >
- "parental_leave" Arrays of < "Congé pour enfants malades" | "Congé paternité prolongé" | "Congé maternité prolongé" | "Prime de naissance" | "Congé interruption spontannée de grosse" | "Aide à la garde d'enfants" | "Crèche" | "Programme de retour de congé parental" | null >
- "training" Arrays of < "Formations en ligne" | "Mentorat" | "Financement des certifications" | "Programme de formation continue" | null >
- "coaching_mentorat" < "Aucun coaching/mentorat" | "Session de coaching / mentorat à la demande" | "Session de coaching / mentorat régulièrement" | null >
- "team_building" Arrays of < "Afterwork" | "Séminaires et voyages" | "Déjeuner d'équipe" | null >
- "work_office_life" Arrays of < "Restaurant d'entreprise" | "Cuisine pour les employés" | "Collations à volonté" | "Animaux acceptés" | "Salle d'allaitement" | "Sport" | null >
- "complementary_health" < "Mutuelle légale" | "Prise en charge de la mutuelle au dessus du légal" | " Prise en charge à 100% de la mutuelle" | null >
- "health_benefits" Arrays of < "Congé maladie" | "Solution de prévention santé mentale" | "Abonnement en salle de sport" | "Compte épargne santé" | "Pension d'invalidité court terme" | "Assurance dentaire" | "Assurance optique" | null >
- "restaurant_card" < "Non" | "Moins de 8€" | "Entre 8€ et 10€" | "Supérieur à 10€" | null >
- "transport" Arrays of < "Remboursement à 100% des transport public" | "Parking" | "Parking à vélo" | "Allocations de télétravail" | "Plan de mobilité durable" | "Location de vélo" | "Voiture de fonction" | null >
- "company_smartphone" < "Non" | "Oui" | "Oui + Choix du mobile" | null >
- "computer_choice" < "Non" | "Oui" | null >
- "bonus_interest" Arrays of < "Intéressement et participation" | "Plan d'epargne entreprise (PEE)" | "Aide au déménagement" | "Prime de cooptation" | "Plan d'achat d'action" | null >
- "inclusiveness" Arrays of < "Recrutement encourageant la diversité" | "Équipe dédiée à la diversité" | "Manifeste sur la diversité" | "Formation sur les biais inconscients" | "Accès aux personnes à mobilité réduite" | null >"""


def test_with_prompt(sample_data):
    df_main, df_metadata, df_additional_info = sample_data
    output = LLMClient(OpenAICOnfig("Random"),df_metadata,df_main, df_additional_info)
    
    prompt = output.formatPrompt(LLMClient.TEMPLATE_DETAILS_PROMPT,"toto")
    assert prompt == """You are now French AI Extractor.You are processing company description.

Do not mix up  training days (jours de formation) , holidays (congés) and telecommuting (télétravail). 

Extract specified values from the source text. 
Return answer as JSON object with following fields. Don't add extract comment. Respect the possible value,  if not specify in text put null value:
- "arranged_schedules" < "Horaire de travail stricte" | "Heure d\'arrivée et de départ flexible" | null >
- "working_place" < "Non flexible" | null >
- "holidays" Arrays of < "Congés payés" | "RTT" | "Congé sabatique" | null > (The legal is 30 days per year)

Do not infer any data based on previous training, strictly use only source text given below as input.
========
toto
========
"""