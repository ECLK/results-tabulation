from app import db
from orm.entities.History import HistoryVersion


class WorkflowInstanceLogModel(db.Model):
    __tablename__ = 'workflowInstanceLog'

    workflowInstanceLogId = db.Column(db.Integer, db.ForeignKey("history_version.historyVersionId"), primary_key=True)
    workflowInstanceId = db.Column(db.Integer, db.ForeignKey("workflowInstance.workflowInstanceId"), nullable=False)
    statusId = db.Column(db.Integer, db.ForeignKey("status.statusId"), nullable=False)
    statusActionId = db.Column(db.Integer, db.ForeignKey("statusAction.statusActionId"), nullable=False)
    metaId = db.Column(db.Integer, db.ForeignKey("meta.metaId"), nullable=True)

    @classmethod
    def create(cls, workflowInstanceId, statusId, statusActionId, metaId):
        workflow_log = cls(
            workflowInstanceLogId=HistoryVersion.create(historyId=workflowInstanceId).historyVersionId,
            workflowInstanceId=workflowInstanceId,
            statusId=statusId,
            statusActionId=statusActionId,
            metaId=metaId
        )
        db.session.add(workflow_log)
        db.session.flush()

        return workflow_log


Model = WorkflowInstanceLogModel
create = Model.create
