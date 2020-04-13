from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from app import db
from orm.entities import Proof, Meta
from orm.entities.History import HistoryVersion
from orm.entities.Workflow import WorkflowActionModel


class WorkflowInstanceLogModel(db.Model):
    __tablename__ = 'workflowInstanceLog'

    workflowInstanceLogId = db.Column(db.Integer, db.ForeignKey("history_version.historyVersionId"), primary_key=True)
    workflowInstanceId = db.Column(db.Integer, db.ForeignKey("workflowInstance.workflowInstanceId"), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    workflowActionId = db.Column(db.Integer, db.ForeignKey("workflowAction.workflowActionId"), nullable=False)
    metaId = db.Column(db.Integer, db.ForeignKey("meta.metaId"), nullable=True)
    proofId = db.Column(db.Integer, db.ForeignKey("proof.proofId"), nullable=True)

    action = relationship(WorkflowActionModel, foreign_keys=[workflowActionId])
    proof = relationship(Proof.Model, foreign_keys=[proofId])
    meta = relationship(Meta.Model, foreign_keys=[metaId])
    historyVersion = relationship(HistoryVersion.Model, foreign_keys=[workflowInstanceLogId])

    metaDataList = association_proxy("meta", "metaDataList")
    createdBy = association_proxy("historyVersion", "createdBy")
    createdAt = association_proxy("historyVersion", "createdAt")

    @classmethod
    def create(cls, workflowInstanceId, status, workflowActionId, metaId, proofId):
        workflow_log = cls(
            workflowInstanceLogId=HistoryVersion.create(historyId=workflowInstanceId).historyVersionId,
            workflowInstanceId=workflowInstanceId,
            status=status,
            workflowActionId=workflowActionId,
            metaId=metaId,
            proofId=proofId
        )
        db.session.add(workflow_log)
        db.session.flush()

        return workflow_log


Model = WorkflowInstanceLogModel
create = Model.create
