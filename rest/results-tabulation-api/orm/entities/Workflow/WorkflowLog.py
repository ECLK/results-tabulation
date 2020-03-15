from app import db


class WorkflowLogModel(db.Model):
    __tablename__ = 'workflowLog'

    workflowLogId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workflowId = db.Column(db.Integer, db.ForeignKey("workflow.workflowId"), nullable=False)
    workflowLogStatusId = db.Column(db.Integer, db.ForeignKey("workflowStatus.workflowStatusId"), nullable=False)
    workflowLogActionId = db.Column(db.Integer, db.ForeignKey("workflowAction.workflowActionId"), nullable=False)
    metaId = db.Column(db.Integer, db.ForeignKey("meta.metaId"), nullable=True)

    @classmethod
    def create(cls, workflowId, workflowLogStatusId, workflowLogActionId, metaId):
        workflow_log = WorkflowLogModel(
            workflowId=workflowId,
            workflowLogStatusId=workflowLogStatusId,
            workflowLogActionId=workflowLogActionId,
            metaId=metaId
        )

        db.session.add(workflow_log)
        db.session.flush()

        return workflow_log


Model = WorkflowLogModel
create = Model.create
