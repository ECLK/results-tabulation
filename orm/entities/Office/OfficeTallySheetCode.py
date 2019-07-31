from config import db
from sqlalchemy.orm import relationship
from orm.enums import TallySheetCodeEnum
from orm.entities import Election, Office


class OfficeTallySheetCode(db.Model):
    __tablename__ = 'office_tallysheet'
    officeId = db.Column(db.Integer, db.ForeignKey(Office.Model.__table__.c.office), primary_key=True)
    tallySheetCode = db.Column(db.Enum(TallySheetCodeEnum), primary_key=True)

    office = relationship("OfficeModel", foreign_keys=[officeId])


Model = OfficeTallySheetCode


def create(officeId, tallySheetCode):
    result = Model(
        officeId=officeId,
        tallySheetCode=tallySheetCode
    )
    db.session.add(result)
    db.session.commit()

    return result
