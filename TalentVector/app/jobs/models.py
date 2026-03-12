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
    work_mobility = StringField()
    location = StringField()
    salary = FloatField()
    description = StringField()
    url = StringField(required=True)
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



