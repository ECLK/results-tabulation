from app import db


class WorkflowActionModel(db.Model):
    __tablename__ = 'workflowAction'

    workflowActionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workflowId = db.Column(db.Integer, db.ForeignKey("workflow.workflowId"), nullable=False)
    workflowActionName = db.Column(db.String(100), default="", nullable=False)
    workflowActionType = db.Column(db.String(100), default="", nullable=False)
    workflowActionFromStatusId = db.Column(db.Integer, db.ForeignKey("workflowStatus.workflowStatusId"), nullable=False)
    workflowActionToStatusId = db.Column(db.Integer, db.ForeignKey("workflowStatus.workflowStatusId"), nullable=False)

    @classmethod
    def create(cls, workflowId, workflowActionName, workflowActionType, workflowActionFromStatusId,
               workflowActionToStatusId):
        workflow_action = WorkflowActionModel(
            workflowId=workflowId,
            workflowActionName=workflowActionName,
            workflowActionType=workflowActionType,
            workflowActionFromStatusId=workflowActionFromStatusId,
            workflowActionToStatusId=workflowActionToStatusId
        )

        db.session.add(workflow_action)
        db.session.flush()

        return workflow_action


Model = WorkflowActionModel
create = Model.create
