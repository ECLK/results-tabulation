from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import case
from sqlalchemy.orm import relationship

from app import db


class WorkflowModel(db.Model):
    __tablename__ = 'workflow'

    workflowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workflowName = db.Column(db.String(100), nullable=False)
    firstStatus = db.Column(db.String(100), nullable=False)
    lastStatus = db.Column(db.String(100), nullable=False)

    actions = relationship("WorkflowActionModel", lazy='subquery')

    @classmethod
    def create(cls, workflowName, statuses, actions, firstStatus, lastStatus):
        workflow: WorkflowModel = cls(workflowName=workflowName, firstStatus=firstStatus, lastStatus=lastStatus)
        db.session.add(workflow)
        db.session.flush()

        for status in statuses:
            WorkflowStatusModel.create(
                workflowId=workflow.workflowId,
                status=status
            )

        for action in actions:
            WorkflowActionModel.create(
                workflowId=workflow.workflowId,
                actionName=action["name"],
                actionType=action["type"],
                fromStatus=action["fromStatus"],
                toStatus=action["toStatus"]
            )

        return workflow

    def get_new_instance(self):
        from orm.entities.Workflow import WorkflowInstance

        workflow_instance = WorkflowInstance.create(workflowId=self.workflowId, status=self.firstStatus)

        return workflow_instance


class WorkflowStatusModel(db.Model):
    __tablename__ = 'workflowStatus'

    workflowStatusId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workflowId = db.Column(db.Integer, db.ForeignKey("workflow.workflowId"), nullable=False)
    status = db.Column(db.String(100), nullable=False)

    @classmethod
    def create(cls, workflowId, status):
        workflow_status = cls(
            workflowId=workflowId,
            status=status
        )
        db.session.add(workflow_status)
        db.session.flush()

        return workflow_status


class WorkflowActionModel(db.Model):
    __tablename__ = 'workflowAction'

    workflowActionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workflowId = db.Column(db.Integer, db.ForeignKey("workflow.workflowId"), nullable=False)
    actionName = db.Column(db.String(100), nullable=False)
    actionType = db.Column(db.String(100), nullable=False)
    fromStatus = db.Column(db.String(100), nullable=False)
    toStatus = db.Column(db.String(100), nullable=False)

    @classmethod
    def create(cls, workflowId, actionName, actionType, fromStatus, toStatus):
        workflow_status_action = cls(
            workflowId=workflowId,
            actionName=actionName,
            actionType=actionType,
            fromStatus=fromStatus,
            toStatus=toStatus
        )
        db.session.add(workflow_status_action)
        db.session.flush()

        return workflow_status_action


Model = WorkflowModel
create = Model.create
