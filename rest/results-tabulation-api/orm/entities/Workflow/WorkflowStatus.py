from app import db


class WorkflowStatusModel(db.Model):
    __tablename__ = 'workflowStatus'

    workflowStatusId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workflowId = db.Column(db.Integer, db.ForeignKey("workflow.workflowId"), nullable=False)
    workflowStatusName = db.Column(db.String(100), nullable=False)

    @classmethod
    def create(cls, workflowId, workflowStatusName):
        workflow_status = WorkflowStatusModel(
            workflowId=workflowId,
            workflowStatusName=workflowStatusName
        )

        db.session.add(workflow_status)
        db.session.flush()

        return workflow_status


Model = WorkflowStatusModel
create = Model.create
