from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy import case

from app import db
from exception import MethodNotAllowedException
from orm.entities import Meta
from orm.entities.Workflow import WorkflowLog, WorkflowStatus, WorkflowAction


class WorkflowModel(db.Model):
    __tablename__ = 'workflow'

    workflowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workflowName = db.Column(db.String(100), nullable=False)
    workflowFirstStatusId = db.Column(db.Integer, db.ForeignKey("workflowStatus.workflowStatusId"), nullable=False)
    workflowLastStatusId = db.Column(db.Integer, db.ForeignKey("workflowStatus.workflowStatusId"), nullable=False)
    workflowCurrentStatusId = db.Column(db.Integer, db.ForeignKey("workflowStatus.workflowStatusId"), nullable=False)

    @hybrid_property
    def actions(self):
        db.session.query(
            WorkflowAction.Model.workflowActionId,
            WorkflowAction.Model.workflowActionName,
            WorkflowAction.Model.workflowActionType,
            case([
                (WorkflowAction.Model.workflowActionFromStatusId == self.workflowCurrentStatusId, True),
                (WorkflowAction.Model.workflowActionFromStatusId != self.workflowCurrentStatusId, False),
            ]).label("allowed")
        ).filter(
            WorkflowAction.Model.workflowId == self.workflowId
        ).order_by(
            WorkflowAction.Model.workflowActionId
        )

    @hybrid_property
    def statuses(self):
        db.session.query(
            WorkflowStatus.Model.workflowStatusId,
            WorkflowStatus.Model.workflowStatusName
        ).filter(
            WorkflowStatus.Model.workflowId == self.workflowId
        ).order_by(
            WorkflowStatus.Model.workflowStatusId
        )

    def __init__(self, workflowName, workflowFirstStatusId, workflowLastStatusId, workflowCurrentStatusId):
        super(WorkflowModel, self).__init__(
            workflowName=workflowName,
            workflowFirstStatusId=workflowFirstStatusId,
            workflowLastStatusId=workflowLastStatusId,
            workflowCurrentStatusId=workflowCurrentStatusId
        )

        db.session.add(self)
        db.session.flush()

    @classmethod
    def create(cls, workflowName, workflowFirstStatusId, workflowLastStatusId, workflowCurrentStatusId):
        workflow = WorkflowModel(
            workflowName=workflowName,
            workflowFirstStatusId=workflowFirstStatusId,
            workflowLastStatusId=workflowLastStatusId,
            workflowCurrentStatusId=workflowCurrentStatusId
        )

        db.session.add(workflow)
        db.session.flush()

    def add_status(self, workflowStatusName):
        workflow_status = WorkflowStatus.create(
            workflowId=self.workflowId,
            workflowStatusName=workflowStatusName
        )

        workflow_status

    def add_action(self, workflowActionName, workflowActionType, workflowActionFromStatusId, workflowActionToStatusId):
        workflow_action = WorkflowAction.create(
            workflowId=self.workflowId,
            workflowActionName=workflowActionName,
            workflowActionType=workflowActionType,
            workflowActionFromStatusId=workflowActionFromStatusId,
            workflowActionToStatusId=workflowActionToStatusId
        )

        return workflow_action

    def add_log(self, workflowLogStatusId, workflowLogActionId, metaId):
        pass

    def _set_current_status_id(self, workflowStatusId):
        self.workflowCurrentStatusId = workflowStatusId

        db.session.add(self)
        db.session.flush()

    def execute_action(self, action: WorkflowAction.Model, meta: Meta):
        if self.workflowCurrentStatusId != action.workflowActionFromStatusId:
            raise MethodNotAllowedException(message="Workflow action is not allowed.")
        else:
            self._set_current_status_id(action.workflowActionToStatusId)

            work_flow = WorkflowLog.create(
                workflowId=self.workflowId,
                workflowLogStatusId=self.workflowCurrentStatusId,
                workflowLogActionId=action.workflowActionId,
                metaId=meta.metaId
            )

            return work_flow


Model = WorkflowModel
create = Model.create
