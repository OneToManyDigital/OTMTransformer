import pytest
import pandas as pd
from pandas import Series, DataFrame
from otm_transformer.model.company import CharacValue
from otm_transformer.transformCpy import getCharacValueFromBenefits, extractSocialData
from otm_transformer.characConstants import *
# Assuming CharacValue, get_charIdVal, getPositiveVal, and getCharacValueFromBenefits are defined above

def test_getCharacValueFromBenefits_single_benefit():
    benefits = Series(["Jusqu'à 1-2 jours de télétravail"])
    characDic = DataFrame({
        'id': [10, 11, 12],
        'is_multiple': [True, False, False]
    })
    characValDic = DataFrame({
        'id': [CV_12_REMOTE, CV_34_REMOTE, CV_FULL_REMOTE],
        'charac_id': [10, 11, 12],
        'positive_value': [1,-2,4]
    })
    
    expected = [CharacValue(characId=10, characValueId=CV_12_REMOTE, positiveValue=1, isMultiple=True)]
    result = getCharacValueFromBenefits(benefits, characDic, characValDic)
    
    assert result == expected

def test_getCharacValueFromBenefits_multiple_benefits():
    benefits = Series(["Jusqu'à 1-2 jours de télétravail, Horaires de travail flexibles", "Retraite complémentaire"])
    characDic = DataFrame({
        'id': [10, 11, 12, 13],
        'is_multiple': [True, False, False, True]
    })
    characValDic = DataFrame({
        'id': [CV_12_REMOTE, CV_34_REMOTE, CV_FULL_REMOTE, CV_SCHEDULE_FULL_CUSTOM],
        'charac_id': [10, 11, 12, 13],
        'positive_value': [1,-2,4,5]
    })
    
    expected = [
        CharacValue(characId=10, characValueId=CV_12_REMOTE, positiveValue=1, isMultiple=True),
        CharacValue(characId=13, characValueId=CV_SCHEDULE_FULL_CUSTOM, positiveValue=5, isMultiple=True)
    ]
    result = getCharacValueFromBenefits(benefits, characDic, characValDic)
    
    assert result == expected


def test_extractSocialData_single_social():
    socials = "https://instagram.com/externaticc"
    result = extractSocialData(socials)
    expected = [CharacValue(characId=C_SOCIALS, characValueId=CV_SOCIALS_INSTAGRAM, positiveValue=-2, isMultiple=True)]
    assert result == expected

def test_extractSocialData_multiple_socials():
    socials = "https://instagram.com/externatic, https://www.linkedin.com/company/externatic, https://twitter.com/Externatic"
    result = extractSocialData(socials)
    expected = [
        CharacValue(characId=C_SOCIALS, characValueId=CV_SOCIALS_INSTAGRAM, positiveValue=-2, isMultiple=True),
        CharacValue(characId=C_SOCIALS, characValueId=CV_SOCIALS_LINKEDIN, positiveValue=-2, isMultiple=True),
        CharacValue(characId=C_SOCIALS, characValueId=CV_SOCIALS_OTHER, positiveValue=-2, isMultiple=True)
    ]
    assert result == expected