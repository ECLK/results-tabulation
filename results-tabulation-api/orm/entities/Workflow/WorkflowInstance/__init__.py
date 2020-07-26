from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from app import db
from exception import MethodNotAllowedException
from exception.messages import MESSAGE_CODE_WORKFLOW_ACTION_NOT_ALLOWED
from ext.ExtendedElection.WORKFLOW_ACTION_TYPE import WORKFLOW_ACTION_TYPE_REQUEST_CHANGES
from orm.entities import History, Meta, Proof
from orm.entities.Workflow import WorkflowStatusModel, WorkflowActionModel
from orm.entities.Workflow.WorkflowInstance import WorkflowInstanceLog


class WorkflowInstanceModel(db.Model):
    __tablename__ = 'workflowInstance'

    workflowInstanceId = db.Column(db.Integer, db.ForeignKey("history.historyId"), primary_key=True)
    workflowId = db.Column(db.Integer, db.ForeignKey("workflow.workflowId"), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    latestLogId = db.Column(db.Integer, db.ForeignKey("workflowInstanceLog.workflowInstanceLogId"), nullable=True)
    proofId = db.Column(db.Integer, db.ForeignKey("proof.proofId"), nullable=True)

    workflow = relationship("WorkflowModel", foreign_keys=[workflowId], lazy='subquery')
    latestLog = relationship(WorkflowInstanceLog.Model, foreign_keys=[latestLogId], lazy='subquery')
    proof = relationship(Proof.Model, foreign_keys=[proofId], lazy='subquery')

    logs = relationship(
        "WorkflowInstanceLogModel", order_by="desc(WorkflowInstanceLogModel.workflowInstanceLogId)",
        primaryjoin="WorkflowInstanceModel.workflowInstanceId==WorkflowInstanceLogModel.workflowInstanceId")

    @hybrid_property
    def statuses(self):
        return db.session.query(
            WorkflowStatusModel.workflowStatusId,
            WorkflowStatusModel.status
        ).filter(
            WorkflowStatusModel.workflowId == self.workflowId
        ).order_by(
            WorkflowStatusModel.workflowStatusId
        ).all()

    @classmethod
    def create(cls, workflowId, status):
        workflow_action = cls(
            workflowInstanceId=History.create().historyId,
            proofId=Proof.create().proofId,
            workflowId=workflowId,
            status=status
        )
        db.session.add(workflow_action)
        db.session.flush()

        return workflow_action

    def execute_action(self, action: WorkflowActionModel, meta: Meta):
        if self.status != action.fromStatus:
            raise MethodNotAllowedException(message="Workflow action is not allowed.",
                                            code=MESSAGE_CODE_WORKFLOW_ACTION_NOT_ALLOWED)
        else:
            self.status = action.toStatus
            self.latestLogId = WorkflowInstanceLog.create(
                workflowInstanceId=self.workflowInstanceId,
                status=action.toStatus,
                workflowActionId=action.workflowActionId,
                metaId=meta.metaId,
                proofId=self.proofId
            ).workflowInstanceLogId

            self.proof.close()

            # proof is replaced only for WORKFLOW_ACTION_TYPE_REQUEST_CHANGES
            if action.actionType == WORKFLOW_ACTION_TYPE_REQUEST_CHANGES:
                self.proofId = Proof.create().proofId
            # For all the other actions, the proof is cloned.
            else:
                self.proofId = self.proof.clone().proofId

            db.session.add(self)
            db.session.flush()

            return self


Model = WorkflowInstanceModel
create = Model.create
