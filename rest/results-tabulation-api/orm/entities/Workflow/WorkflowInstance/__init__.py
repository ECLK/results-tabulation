from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import case
from sqlalchemy.orm import relationship

from app import db
from exception import MethodNotAllowedException
from orm.entities import History, Meta
from orm.entities.Workflow import WorkflowStatusModel, WorkflowActionModel
from orm.entities.Workflow.WorkflowInstance import WorkflowInstanceLog


class WorkflowInstanceModel(db.Model):
    __tablename__ = 'workflowInstance'

    workflowInstanceId = db.Column(db.Integer, db.ForeignKey("history.historyId"), primary_key=True)
    workflowId = db.Column(db.Integer, db.ForeignKey("workflow.workflowId"), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    latestLogId = db.Column(db.Integer, db.ForeignKey("workflowInstanceLog.workflowInstanceLogId"), nullable=True)

    latestLog = relationship(WorkflowInstanceLog.Model, foreign_keys=[latestLogId])

    @hybrid_property
    def actions(self):
        return db.session.query(
            WorkflowActionModel.workflowActionId,
            WorkflowActionModel.actionName,
            WorkflowActionModel.actionType,
            WorkflowActionModel.fromStatus,
            WorkflowActionModel.toStatus,
            case([
                (WorkflowActionModel.fromStatus == self.status, True),
                (WorkflowActionModel.fromStatus != self.status, False),
            ]).label("allowed")
        ).filter(
            WorkflowActionModel.workflowId == self.workflowId
        ).order_by(
            WorkflowActionModel.workflowActionId
        )

    @hybrid_property
    def statuses(self):
        return db.session.query(
            WorkflowStatusModel.workflowStatusId,
            WorkflowStatusModel.status
        ).filter(
            WorkflowStatusModel.workflowId == self.workflowId
        ).order_by(
            WorkflowStatusModel.workflowStatusId
        )

    @classmethod
    def create(cls, workflowId, status):
        workflow_action = cls(
            workflowInstanceId=History.create().historyId,
            workflowId=workflowId,
            status=status
        )
        db.session.add(workflow_action)
        db.session.flush()

        return workflow_action

    def execute_action(self, action: WorkflowActionModel, meta: Meta):
        if self.status != action.fromStatus:
            raise MethodNotAllowedException(message="Workflow action is not allowed.")
        else:
            self.status = action.toStatus
            self.latestLogId = WorkflowInstanceLog.create(
                workflowInstanceId=self.workflowInstanceId,
                status=action.toStatus,
                workflowActionId=action.workflowActionId,
                metaId=meta.metaId
            ).workflowInstanceLogId

            db.session.add(self)
            db.session.flush()

            return self


Model = WorkflowInstanceModel
create = Model.create
