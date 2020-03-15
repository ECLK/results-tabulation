from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import case

from app import db
from exception import MethodNotAllowedException
from orm.entities import History, Meta, Status
from orm.entities.Status import StatusAction
from orm.entities.Workflow import WorkflowStatusActionModel, WorkflowStatusModel
from orm.entities.Workflow.WorkflowInstance import WorkflowInstanceLog


class WorkflowInstanceModel(db.Model):
    __tablename__ = 'workflowInstance'

    workflowInstanceId = db.Column(db.Integer, db.ForeignKey("history.historyId"), primary_key=True)
    workflowId = db.Column(db.Integer, db.ForeignKey("workflow.workflowId"), nullable=False)
    statusId = db.Column(db.Integer, db.ForeignKey("status.statusId"), nullable=False)

    @hybrid_property
    def actions(self):
        return db.session.query(
            StatusAction.Model.statusActionId,
            StatusAction.Model.statusActionName,
            StatusAction.Model.statusActionType,
            StatusAction.Model.fromStatusId,
            StatusAction.Model.toStatusId,
            case([
                (StatusAction.Model.fromStatusId == self.statusId, True),
                (StatusAction.Model.fromStatusId != self.statusId, False),
            ]).label("allowed")
        ).filter(
            StatusAction.Model.statusActionId == WorkflowStatusActionModel.statusActionId,
            WorkflowStatusActionModel.workflowId == self.workflowId
        ).order_by(
            WorkflowStatusActionModel.workflowStatusActionId
        )

    @hybrid_property
    def statuses(self):
        return db.session.query(
            Status.Model.statusId,
            Status.Model.statusName
        ).filter(
            Status.Model.statusId == WorkflowStatusModel.statusId,
            WorkflowStatusModel.workflowId == self.workflowId
        ).order_by(
            WorkflowStatusModel.workflowStatusId
        )

    @classmethod
    def create(cls, workflowId, statusId):
        workflow_action = cls(
            workflowInstanceId=History.create().historyId,
            workflowId=workflowId,
            statusId=statusId
        )
        db.session.add(workflow_action)
        db.session.flush()

        return workflow_action

    def execute_action(self, action: StatusAction.Model, meta: Meta):
        if self.statusId != action.fromStatusId:
            raise MethodNotAllowedException(message="Workflow action is not allowed.")
        else:
            self.statusId = action.toStatusId

            db.session.add(self)
            db.session.flush()

            work_flow = WorkflowInstanceLog.create(
                workflowInstanceId=self.workflowInstanceId,
                statusId=action.toStatusId,
                statusActionId=action.statusActionId,
                metaId=meta.metaId
            )

            return work_flow


Model = WorkflowInstanceModel
create = Model.create
