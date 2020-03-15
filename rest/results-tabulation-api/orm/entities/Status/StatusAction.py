from app import db


class StatusActionModel(db.Model):
    __tablename__ = 'statusAction'

    statusActionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    statusActionName = db.Column(db.String(100), default="", nullable=False)
    statusActionType = db.Column(db.String(100), default="", nullable=False)
    fromStatusId = db.Column(db.Integer, db.ForeignKey("status.statusId"), nullable=False)
    toStatusId = db.Column(db.Integer, db.ForeignKey("status.statusId"), nullable=False)

    @classmethod
    def create(cls, statusActionName, statusActionType, fromStatusId, toStatusId):
        status_action = cls(
            statusActionName=statusActionName,
            statusActionType=statusActionType,
            fromStatusId=fromStatusId,
            toStatusId=toStatusId
        )

        db.session.add(status_action)
        db.session.flush()

        return status_action


Model = StatusActionModel
create = Model.create
