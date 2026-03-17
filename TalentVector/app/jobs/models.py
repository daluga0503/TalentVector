from mongoengine import Document, StringField, FloatField, ListField, DateTimeField
from datetime import datetime
from enum import Enum

# class Seniority(Enum):
#    JUNIOR = 'junior'
#    MID = 'mid'
#    SENIOR = 'senior'
#    ARCHITECTURE = 'architecture'
#    LEAD = 'lead'

class JobOffer(Document):
    title = StringField(required=True)
    company = StringField(required=True)
    location = StringField()
    movility = StringField() 
    salary = StringField()
    description = StringField()
    url = StringField(required=True, unique=True)
    skills = ListField(StringField())
    seniority = StringField()
    # seniority = StringField(choices = [(s.value, s.value) for s in Seniority], default=Seniority.JUNIOR.value)
    type_contract = StringField()
    created_at = DateTimeField(default=datetime.now())

    meta = {
        "collection": "job_offers",
        "indexes": [
            "title",
            "company",
            "salary",
            "location",
            "skills",
            "seniority",
        ]
    }



