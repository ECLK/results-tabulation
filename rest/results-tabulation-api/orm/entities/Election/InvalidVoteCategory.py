from app import db
from sqlalchemy.orm import relationship


class InvalidVoteCategoryModel(db.Model):
    __tablename__ = 'election_invalidVoteCategory'
    invalidVoteCategoryId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"))
    categoryDescription = db.Column(db.String(300), nullable=False)
    invalidVoteCategoryType = db.Column(db.String(50), nullable=True)

    election = relationship("ElectionModel", foreign_keys=[electionId])

    __table_args__ = (
        db.UniqueConstraint('electionId', 'categoryDescription', name='InvalidCategoryPerElection'),
    )

    def __init__(self, electionId, categoryDescription, invalidVoteCategoryType):
        super(InvalidVoteCategoryModel, self).__init__(
            electionId=electionId,
            categoryDescription=categoryDescription,
            invalidVoteCategoryType=invalidVoteCategoryType
        )

        db.session.add(self)
        db.session.flush()


Model = InvalidVoteCategoryModel


def get_all(electionId=None, categoryDescription=None, invalidVoteCategoryType=None):
    query = Model.query

    if electionId is not None:
        query = query.filter(Model.electionId == electionId)

    if categoryDescription is not None:
        query = query.filter(Model.categoryDescription == categoryDescription)

    if invalidVoteCategoryType is not None:
        query = query.filter(Model.invalidVoteCategoryType == invalidVoteCategoryType)

    return query


def get_by_id(electionId, partyId):
    result = Model.query.filter(
        Model.electionId == electionId,
        Model.partyId == partyId
    ).one_or_none()

    return result


def create(electionId, categoryDescription, invalidVoteCategoryType=None):
    result = Model(
        electionId=electionId,
        categoryDescription=categoryDescription,
        invalidVoteCategoryType=invalidVoteCategoryType
    )

    return result
