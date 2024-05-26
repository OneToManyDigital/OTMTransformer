C_REMOTE=1  # Politique de télétravail
CV_NO_REMOTE=1  # Présentielle
CV_OCC_REMOTE=2 # Télétravail occasionnel (rendez-vous médicaux, attente d''une livraison) ou de circonstances exceptionnelles
CV_FULL_REMOTE=104 # Télétravail à 100%
CV_12_REMOTE=103 # 1-2 jours de télétravail
CV_34_REMOTE=105 # 3-4 jours de télétravail
CV_4_REMOTE=106 # Semaine de 4 jours

C_SCHEDULE=2 
CV_SCHEDULE_STRICT=4 # Horaire de travail stricte
CV_SCHEDULE_PART_CUSTOM=5 # Heure d''arrivée et de départ flexible
CV_SCHEDULE_FULL_CUSTOM=6 # Flexibilité totale des horaires

C_HOLIDAY=3
CV_HOLIDAY_CP=301 # Congés payés
CV_HOLIDAY_RTT=302 # RTT
CV_HOLIDAY_CS=303 # Congé sabatique
CV_HOLIDAY_BENEVOLA=304 # Jours de bénévolat offers
CV_HOLIDAY_CP_ILIMIT=305 # Congé vacances illimitées
CV_HOLIDAY_CP_ADDITIONAL=306 # Congés payés supplémentaires


C_REMOTE_PLACE=4 #
CV_REMOTE_PLACE_EVERYWHERE=402 # Télétravail de n''importe où

C_PARENTALITY=5
CV_PARENTALITY_CP_CHILD=501 # Congé pour enfants malades
CV_PARENTALITY_CP_DAD=502 # Congé paternité prolongé
CV_PARENTALITY_CP_MOM=503 # Congé maternité prolongé
CV_PARENTALITY_BORN=504 # Prime de naissance
CV_PARENTALITY_STOP=505 # Congé interruption spontannée de grosse
CV_PARENTALITY_KEEP=506 # Aide à la garde d''enfants
CV_PARENTALITY_CRECHE=507 # Crèche
CV_PARENTALITY_BACK=508 # Programme de retour de congé parental

C_TRAINING=6
CV_TRAINING_ONLINE=603 # Formations en ligne
CV_TRAINING_CERTIIF=605 # Financement des certifications
CV_TRAINING_CONTINUE=16 # Programme de formation continue
CV_TRAINING_MENTORAT=604 # Mentorat

C_TEAM_BUILD=9
CV_TEAM_BUILD_AFTERWOK=902 # Afterwork
CV_TEAM_BUILD_LUNCH=900 # Déjeuner d''équipe
CV_TEAM_BUILD_TRIP=903 # Séminaires et voyages

C_WOFFICE_LIFE=10 
CV_WOFFICE_LIFE_RESTO=1002  # Restaurant d''entreprise
CV_WOFFICE_LIFE_KITCHEN=1003  # Cuisine pour les employés
CV_WOFFICE_LIFE_VOLONTE=1004  # Collations à volonté
CV_WOFFICE_LIFE_PETS=1005  # Animaux acceptés
CV_WOFFICE_LIFE_ALLAITEMENT=1006  # Salle d''allaitement
CV_WOFFICE_LIFE_SPORT=1007  # Sport

C_HEATH_BEN=13
CV_HEATH_BEN_CP=1200 # Congé maladie
CV_HEATH_BEN_HEAD=1201 # Solution de prévention santé mentale
CV_HEATH_BEN_SPORT=1202 # Abonnement en salle de sport
CV_HEATH_BEN_CES=1203 # Compte épargne santé
CV_HEATH_BEN_INVA=1204 # Pension d''invalidité court terme
CV_HEATH_BEN_TEETH=1205 # Assurance dentaire
CV_HEATH_BEN_EYE=1206 # Assurance optique


C_TICKET_RESTO=14
CV_TICKET_RESTO_UNDER_8=35 # Moins de 8€

C_TRANSPORT=15
CV_TRANSPORT_IND_REM=1403 # Remboursement à 100% des transport public
CV_TRANSPORT_IND_PARK=1404 # Parking
CV_TRANSPORT_IND_PARK_BIKE=1405 # Parking à vélo
CV_TRANSPORT_IND_HOMEWORKING=1406 # Allocations de télétravail
CV_TRANSPORT_IND_MOB_DUR=1407 # Plan de mobilité durable
CV_TRANSPORT_IND_LOC_BIKER=1408 # Location de vélo
CV_TRANSPORT_IND_CAR=1409 # Voiture de fonction


C_SALARY=19
CV_SALARY_LOWER=47 # Inférieur à la moyenne
CV_SALARY_MEAN=48 # Dans la moyenne
CV_SALARY_UPPER=49 # Supérieur à la moyenne

C_AVAN_FINANC=20
CV_AVAN_FINANC_INT_PART=50  # Intéressement et participation
CV_AVAN_FINANC_PEE=1902  # Plan d''epargne entreprise (PEE)
CV_AVAN_FINANC_MOVE=1903  # Aide au déménagement
CV_AVAN_FINANC_COOPT=1904  # Prime de cooptation
CV_AVAN_FINANC_ACHAT_ACT=1905  # Plan d''achat d''action

C_SOCIALS=22
CV_SOCIALS_BLOG=2100
CV_SOCIALS_LINKEDIN=2101
CV_SOCIALS_INSTAGRAM=2102
CV_SOCIALS_TIKTOK=2103
CV_SOCIALS_PRESSE=2104
CV_SOCIALS_TELE=2105
CV_SOCIALS_WTJ=2106
CV_SOCIALS_INDEED=2107
CV_SOCIALS_OTHER=2108

C_DIV=23
CV_DIV_ENC=2200 # Recrutement encourageant la diversité
CV_DIV_TEAM=2201 #  Équipe dédiée à la diversité
CV_DIV_MANIFEST=2202 # Manifeste sur la diversité
CV_DIV_TRAINING=2203 # Formation sur les biais inconscients
CV_DIV_ACCESS=2204 # Accès aux personnes à mobilité réduite


benefit_to_charIdVal = {
    "Jusqu'à 1-2 jours de télétravail": CV_12_REMOTE,
    "Jusqu'à 3-4 jours de télétravail": CV_34_REMOTE,
    "Ouvert au télétravail total": CV_FULL_REMOTE,
    "100% en télétravail": CV_FULL_REMOTE,
    "Horaires de travail flexibles": CV_SCHEDULE_FULL_CUSTOM,
    "Temps partiel possible": CV_SCHEDULE_PART_CUSTOM,
    "Semaine de 4 jours": CV_4_REMOTE,
    "Télétravail de n’importe où": CV_REMOTE_PLACE_EVERYWHERE,
    "Tickets restaurant": CV_TICKET_RESTO_UNDER_8,
    "Congé sabbatique": CV_HOLIDAY_CS,
    "Congé vacances illimitées": CV_HOLIDAY_CP_ILIMIT,
    "Jours de bénévolat offerts": CV_HOLIDAY_BENEVOLA,
    "Congés payés supplémentaires": CV_HOLIDAY_CP_ADDITIONAL,
    "RTT": CV_HOLIDAY_RTT,
    "Congés payés": CV_HOLIDAY_CP,
    "Intéressement & participation": CV_AVAN_FINANC_INT_PART,
    "Plan d’épargne entreprise (PEE)": CV_AVAN_FINANC_PEE,
    "Plan d’actionnariat salarié": CV_AVAN_FINANC_ACHAT_ACT,
    "Plan d’achat d’actions": CV_AVAN_FINANC_ACHAT_ACT,
    "Prime de cooptation": CV_AVAN_FINANC_COOPT,
    "Afterworks": CV_TEAM_BUILD_AFTERWOK,
    "Déjeuners d’équipe": CV_TEAM_BUILD_LUNCH,
    "Team building": CV_TEAM_BUILD_TRIP,
    "Financement des certifications": CV_TRAINING_CERTIIF,
    "Formation en leadership": CV_TRAINING_CONTINUE,
    "Plan de développement": CV_TRAINING_CONTINUE,
    "Formations sur le temps de travail": CV_TRAINING_CONTINUE,
    "Séminaires & formations professionnelles": CV_TRAINING_CONTINUE,
    "Formations en ligne": CV_TRAINING_ONLINE,
    "Mentorat": CV_TRAINING_MENTORAT,
    "Congé maternité prolongé": CV_PARENTALITY_CP_MOM,
    "Congé paternité prolongé": CV_PARENTALITY_CP_DAD,
    "Congés pour enfant malade": CV_PARENTALITY_CP_CHILD,
    "Crèche": CV_PARENTALITY_CRECHE,
    "Programme de retour de congé parental": CV_PARENTALITY_BACK,
    "Congés interruption spontanée de grossesse": CV_PARENTALITY_STOP,
    "Aide à la garde d’enfant": CV_PARENTALITY_KEEP,
    "Prime de naissance": CV_PARENTALITY_BORN,
    "Allocation de télétravail": CV_TRANSPORT_IND_HOMEWORKING,
    "Budget sport": CV_WOFFICE_LIFE_SPORT,
    "Salle de sport dans les locaux": CV_WOFFICE_LIFE_SPORT,
    "Cours de fitness virtuels": CV_WOFFICE_LIFE_SPORT,
    "Restaurant d’entreprise / Cuisine pour les employés": CV_WOFFICE_LIFE_RESTO,
    "Collations à volonté": CV_WOFFICE_LIFE_VOLONTE,
    "Salle d’allaitement": CV_WOFFICE_LIFE_ALLAITEMENT,
    "Animaux acceptés": CV_WOFFICE_LIFE_PETS,
    "Recrutement encourageant la diversité": CV_DIV_ENC,
    "Équipe dédiée à la Diversité & inclusivité": CV_DIV_TEAM,
    "Accès aux personnes à mobilité réduite": CV_DIV_ACCESS,
    "Formation sur les biais inconscients": CV_DIV_TRAINING,
    "Manifeste sur la diversité": CV_DIV_MANIFEST,
    "Open space": None,
    "Salle de jeux ou club de loisirs": None,
    "Politique d'égalité salariale": None,
    "Employee Resource Groups (ERG)": None,
    "Célébration des fêtes annuelles / Calendrier des fêtes": None,
    "Aide au déménagement": CV_AVAN_FINANC_MOVE,
    "Abondement des dons caritatifs": None,
    "Incentives à long terme": None,
    "Partenariat avec des associations": None,
    "Tenue décontractée": None,
    "Politique de transparence": None,
    "Bénévolat en région": None,
    "Remboursement des frais de scolarité": None,
    "Avantages liés à l’adoption": None,
    "Journées famille en entreprise": None,
    "Ressources pour le soutien familial": None,
    "Avantages liés à la fertilité": None,
    "Congé de solidarité familiale": None,
    "Happy hours": None,
    "Mutuelle santé": None,
    "Solution de prévention santé mentale": CV_HEATH_BEN_HEAD,
    "Congés maladie": CV_HEATH_BEN_CP,
    "Maintien du salaire à 100% dès le premier jour d’arrêt maladie": None,
    "Assurance optique": CV_HEATH_BEN_EYE,
    "Assurance dentaire": CV_HEATH_BEN_TEETH,
    "Pension d'invalidité long terme": None,
    "Pension d'invalidité court terme": CV_HEATH_BEN_INVA,
    "Assurance vie": None,
    "Compte épargne santé": CV_HEATH_BEN_CES,
    "Health Reimbursement Account (HRA)": None,
    "Assurance animaux": None,
    "Compte de dépenses flexible (FSA)": None,
    "FSA avec contribution de l'employeur": None,
    "Prévoyance": None,
    "Plan d’épargne pour la retraite collectif (PERCO)": None,
    "Retraite complémentaire": None,
    "Plan de retraite anticipée": None,
    "401(K)": None,
    "Équivalent 401(K)": None,
    "Remboursement des transports publics": CV_TRANSPORT_IND_REM,
    "Parking à vélo": CV_TRANSPORT_IND_PARK_BIKE,
    "Parking": CV_TRANSPORT_IND_PARK,
    "Plan de mobilité durable": CV_TRANSPORT_IND_MOB_DUR,
    "Allocation de télétravail": CV_TRANSPORT_IND_HOMEWORKING,
    "Covoiturage": None,
    "Aides pour les trajets domicile-travail": None,
    "Location de vélos": CV_TRANSPORT_IND_LOC_BIKER,
}

def get_charIdVal(benefit):
    return benefit_to_charIdVal.get(benefit, None)

url_mapping = {
   'blog': CV_SOCIALS_BLOG,
    'linkedin': CV_SOCIALS_LINKEDIN,
    'instagram': CV_SOCIALS_INSTAGRAM,
    'tiktok': CV_SOCIALS_TIKTOK,
    'presse': CV_SOCIALS_PRESSE,
    'télé': CV_SOCIALS_TELE,
    'welcometothejungle': CV_SOCIALS_WTJ,
    'indeed': CV_SOCIALS_INDEED,
    'autres': CV_SOCIALS_OTHER,
}

def get_url_mapping(url):
    for key, value in url_mapping.items():
        if key in url:
            return value
    return 2108
