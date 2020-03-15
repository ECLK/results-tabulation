from app import db, ma


class StatusModel(db.Model):
    __tablename__ = 'status'

    statusId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    statusName = db.Column(db.String(100), nullable=False)


    @classmethod
    def create(cls, statusName):
        workflow_status = cls(statusName=statusName)
        db.session.add(workflow_status)
        db.session.flush()

        return workflow_status


Model = StatusModel
create = Model.create
