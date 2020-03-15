from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import case

from app import db
from orm.entities import Status
from orm.entities.Status import StatusAction


class WorkflowModel(db.Model):
    __tablename__ = 'workflow'

    workflowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workflowName = db.Column(db.String(100), nullable=False)
    firstStatusId = db.Column(db.Integer, db.ForeignKey("status.statusId"), nullable=False)
    lastStatusId = db.Column(db.Integer, db.ForeignKey("status.statusId"), nullable=False)

    @hybrid_property
    def actions(self):
        return db.session.query(
            StatusAction.Model.statusActionId,
            StatusAction.Model.statusActionName,
            StatusAction.Model.statusActionType,
            StatusAction.Model.fromStatusId,
            StatusAction.Model.toStatusId,
            case([
                (StatusAction.Model.fromStatusId == self.workflowCurrentStatusId, True),
                (StatusAction.Model.fromStatusId != self.workflowCurrentStatusId, False),
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
    def create(cls, workflowName, statuses, actions, firstStatusId, lastStatusId):
        workflow: WorkflowModel = cls(workflowName=workflowName, firstStatusId=firstStatusId, lastStatusId=lastStatusId)
        db.session.add(workflow)
        db.session.flush()

        for status_list in statuses:
            for status in status_list:
                workflow.add_status(status.statusId)

        for action in actions:
            workflow.add_status_action(
                statusActionId=StatusAction.create(
                    statusActionName=action["name"],
                    statusActionType=action["type"],
                    fromStatusId=action["fromStatus"].statusId,
                    toStatusId=action["toStatus"].statusId
                ).statusActionId
            )

        return workflow

    def add_status(self, statusId):
        workflow_status = WorkflowStatusModel.create(
            workflowId=self.workflowId,
            statusId=statusId
        )

        return workflow_status

    def add_status_action(self, statusActionId):
        workflow_status = WorkflowStatusActionModel.create(
            workflowId=self.workflowId,
            statusActionId=statusActionId
        )

        return workflow_status

    def get_new_instance(self):
        from orm.entities.Workflow import WorkflowInstance

        workflow_instance = WorkflowInstance.create(workflowId=self.workflowId, statusId=self.firstStatusId)

        return workflow_instance


class WorkflowStatusModel(db.Model):
    __tablename__ = 'workflowStatus'

    workflowStatusId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workflowId = db.Column(db.Integer, db.ForeignKey("workflow.workflowId"), nullable=False)
    statusId = db.Column(db.Integer, db.ForeignKey("status.statusId"), nullable=False)

    @classmethod
    def create(cls, workflowId, statusId):
        workflow_status = cls(
            workflowId=workflowId,
            statusId=statusId
        )
        db.session.add(workflow_status)
        db.session.flush()

        return workflow_status


class WorkflowStatusActionModel(db.Model):
    __tablename__ = 'workflowStatusAction'

    workflowStatusActionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workflowId = db.Column(db.Integer, db.ForeignKey("workflow.workflowId"), nullable=False)
    statusActionId = db.Column(db.Integer, db.ForeignKey("statusAction.statusActionId"), nullable=False)

    @classmethod
    def create(cls, workflowId, statusActionId):
        workflow_status_action = cls(
            workflowId=workflowId,
            statusActionId=statusActionId
        )
        db.session.add(workflow_status_action)
        db.session.flush()

        return workflow_status_action


Model = WorkflowModel
create = Model.create
