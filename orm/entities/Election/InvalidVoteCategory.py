from app import db
from sqlalchemy.orm import relationship
from util import get_paginated_query


class InvalidVoteCategoryModel(db.Model):
    __tablename__ = 'election_invalidVoteCategory'
    invalidVoteCategoryId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"))
    categoryDescription = db.Column(db.String(300), nullable=False)

    election = relationship("ElectionModel", foreign_keys=[electionId])

    __table_args__ = (
        db.UniqueConstraint('electionId', 'categoryDescription', name='InvalidCategoryPerElection'),
    )

    def __init__(self, electionId, categoryDescription):
        super(InvalidVoteCategoryModel, self).__init__(
            electionId=electionId,
            categoryDescription=categoryDescription
        )

        db.session.add(self)
        db.session.commit()


Model = InvalidVoteCategoryModel


def get_all(electionId=None, categoryDescription=None):
    query = Model.query

    if electionId is not None:
        query = query.filter(Model.electionId == electionId)

    if categoryDescription is not None:
        query = query.filter(Model.categoryDescription == categoryDescription)

    result = get_paginated_query(query).all()

    return result


def get_by_id(electionId, partyId):
    result = Model.query.filter(
        Model.electionId == electionId,
        Model.partyId == partyId
    ).one_or_none()

    return result


def create(electionId, categoryDescription):
    result = Model(
        electionId=electionId,
        categoryDescription=categoryDescription
    )

    return result
