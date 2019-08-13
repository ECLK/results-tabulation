from app import db
# from orm.entities import TallySheet, Office
# from orm.entities.Office import CountingCentre
from sqlalchemy.orm import relationship

from util import get_paginated_query


class ElectionModel(db.Model):
    __tablename__ = 'election'
    electionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parties = relationship("ElectionPartyModel")


Model = ElectionModel


def create():
    result = Model()
    db.session.add(result)
    db.session.commit()

    return result


def get_all():
    query = Model.query

    result = get_paginated_query(query).all()

    return result


def get_by_id(electionId):
    result = Model.query.filter(
        Model.electionId == electionId
    ).one_or_none()

    return result


def create_tally_sheets(electionId, electionType):
    election = get_by_id(electionId=electionId)

    # if electionType == "Precidential":
