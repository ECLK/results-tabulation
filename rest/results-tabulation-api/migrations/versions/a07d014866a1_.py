"""Adding workflow model
Revision ID: a07d014866a1
Revises: 3971c2f9c31f
Create Date: 2020-03-12 20:45:36.320151
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from tqdm import tqdm

# revision identifiers, used by Alembic.
revision = 'a07d014866a1'
down_revision = '3971c2f9c31f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'workflow',
        sa.Column('workflowId', sa.Integer(), nullable=False),
        sa.Column('workflowName', sa.String(length=100), nullable=False),
        sa.Column('firstStatus', sa.String(length=100), nullable=False),
        sa.Column('lastStatus', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('workflowId')
    )
    op.create_table(
        'workflowAction',
        sa.Column('workflowActionId', sa.Integer(), nullable=False),
        sa.Column('workflowId', sa.Integer(), nullable=False),
        sa.Column('actionName', sa.String(length=100), nullable=False),
        sa.Column('actionType', sa.String(length=100), nullable=False),
        sa.Column('fromStatus', sa.String(length=100), nullable=False),
        sa.Column('toStatus', sa.String(length=100), nullable=False),
        sa.ForeignKeyConstraint(['workflowId'], ['workflow.workflowId'], "workflowAction_fk_workflowId"),
        sa.PrimaryKeyConstraint('workflowActionId')
    )
    op.create_table(
        'workflowInstance',
        sa.Column('workflowInstanceId', sa.Integer(), nullable=False),
        sa.Column('workflowId', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=100), nullable=False),
        sa.Column('latestLogId', sa.Integer(), nullable=True),
        sa.Column('proofId', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['workflowId'], ['workflow.workflowId'], 'workflowInstance_fk_workflowId'),
        sa.ForeignKeyConstraint(['proofId'], ['proof.proofId'], 'workflowInstance_fk_proofId'),
        sa.ForeignKeyConstraint(['workflowInstanceId'], ['history.historyId'],
                                'workflowInstance_fk_workflowInstanceId'),
        sa.PrimaryKeyConstraint('workflowInstanceId')
    )
    op.create_table(
        'workflowInstanceLog',
        sa.Column('workflowInstanceLogId', sa.Integer(), nullable=False),
        sa.Column('workflowInstanceId', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=100), nullable=False),
        sa.Column('workflowActionId', sa.Integer(), nullable=False),
        sa.Column('metaId', sa.Integer(), nullable=True),
        sa.Column('proofId', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['metaId'], ['meta.metaId'], 'workflowInstanceLog_fk_metaId'),
        sa.ForeignKeyConstraint(['workflowActionId'], ['workflowAction.workflowActionId'],
                                'workflowInstanceLog_fk_workflowActionId'),
        sa.ForeignKeyConstraint(['workflowInstanceId'], ['workflowInstance.workflowInstanceId'],
                                'workflowInstanceLog_fk_workflowInstanceId'),
        sa.ForeignKeyConstraint(['workflowInstanceLogId'], ['history_version.historyVersionId'],
                                'workflowInstanceLog_fk_workflowInstanceLogId'),
        sa.ForeignKeyConstraint(['proofId'], ['proof.proofId'], 'workflowInstanceLog_fk_proofId'),
        sa.PrimaryKeyConstraint('workflowInstanceLogId')
    )
    op.create_table(
        'workflowStatus',
        sa.Column('workflowStatusId', sa.Integer(), nullable=False),
        sa.Column('workflowId', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=100), nullable=False),
        sa.ForeignKeyConstraint(['workflowId'], ['workflow.workflowId'], 'workflowStatus_fk_workflowId'),
        sa.PrimaryKeyConstraint('workflowStatusId')
    )

    op.add_column('tallySheet', sa.Column('workflowInstanceId', sa.Integer(), nullable=True))
    op.create_foreign_key('tallySheet_fk_workflowInstanceId', 'tallySheet', 'workflowInstance', ['workflowInstanceId'],
                          ['workflowInstanceId'])
    op.create_foreign_key('workflowInstance_fk_latestLogId', 'workflowInstance', 'workflowInstanceLog', ['latestLogId'],
                          ['workflowInstanceLogId'])

    ######################################################################
    # Migrate existing tally sheets
    ######################################################################

    Base = declarative_base()
    bind = op.get_bind()
    session = Session(bind=bind)

    PRE_28 = "PRE-28"
    PRE_41 = "PRE-41"
    PRE_30_PD = "PRE-30-PD"
    PRE_30_ED = "PRE-30-ED"
    PRE_21 = "PRE-21"
    PRE_34_CO = "PRE-34-CO"
    PRE_34_I_RO = "PRE-34-I-RO"
    PRE_34_II_RO = "PRE-34-II-RO"
    PRE_34 = "PRE-34"
    PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS = "PRE-ALL-ISLAND-RESULTS-BY-ELECTORAL-DISTRICTS"
    PRE_ALL_ISLAND_RESULTS = "PRE-ALL-ISLAND-RESULTS"
    CE_201_PV = "CE-201-PV"
    PRE_30_PD_PV = "PRE-30-PD-PV"
    CE_201 = "CE-201"
    PRE_34_PD = "PRE-34-PD"
    PRE_34_ED = "PRE-34-ED"
    PRE_34_AI = "PRE-34-AI"

    WORKFLOW_ACTION_TYPE_VIEW = "VIEW"
    WORKFLOW_ACTION_TYPE_SAVE = "SAVE"
    WORKFLOW_ACTION_TYPE_VERIFY = "VERIFY"
    WORKFLOW_ACTION_TYPE_PRINT = "PRINT"
    WORKFLOW_ACTION_TYPE_SUBMIT = "SUBMIT"
    WORKFLOW_ACTION_TYPE_REQUEST_CHANGES = "REQUEST_CHANGES"
    WORKFLOW_ACTION_TYPE_EDIT = "EDIT"
    WORKFLOW_ACTION_TYPE_MOVE_TO_CERTIFY = "MOVE_TO_CERTIFY"
    WORKFLOW_ACTION_TYPE_CERTIFY = "CERTIFY"
    WORKFLOW_ACTION_TYPE_RELEASE = "RELEASE"

    WORKFLOW_STATUS_TYPE_EMPTY = "Empty"
    WORKFLOW_STATUS_TYPE_SAVED = "Saved"
    WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED = "Changed Requested"
    WORKFLOW_STATUS_TYPE_SUBMITTED = "Submitted"
    WORKFLOW_STATUS_TYPE_VERIFIED = "Verified"
    WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY = "Ready to Certify"
    WORKFLOW_STATUS_TYPE_CERTIFIED = "Certified"
    WORKFLOW_STATUS_TYPE_RELEASED = "Released"

    BARCODE_LENGTH = 13

    class Barcode(Base):
        __tablename__ = 'barcode'
        barcodeId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        barcodeString = sa.Column(sa.String(13), nullable=True)

        @classmethod
        def _get_barcode_string(cls, num):
            num_str = str(num)
            for i in range(BARCODE_LENGTH - len(num_str)):
                num_str = "0" + num_str
            return num_str

        @classmethod
        def create(cls):
            barcode = cls()
            session.add(barcode)
            session.flush()

            barcode.barcodeString = cls._get_barcode_string(barcode.barcodeId)
            session.flush()

            return barcode

    class Stamp(Base):
        __tablename__ = 'stamp'
        stampId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        ip = sa.Column(sa.String(100), nullable=False)
        createdBy = sa.Column(sa.String(100), nullable=False)
        createdAt = sa.Column(sa.DateTime, default=datetime.now, nullable=False)
        barcodeId = sa.Column(sa.Integer, nullable=False)

        @classmethod
        def create(cls):
            barcode = Barcode.create()
            stamp = cls(barcodeId=barcode.barcodeId, ip="", createdBy="")

            session.add(stamp)
            session.flush()

            return stamp

    class MetaData(Base):
        __tablename__ = 'metaData'

        metaDataId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        metaId = sa.Column(sa.Integer, sa.ForeignKey("meta.metaId"), nullable=False)
        metaDataKey = sa.Column(sa.String(100), nullable=False)
        metaDataValue = sa.Column(sa.String(100), nullable=False)

        @classmethod
        def create(cls, metaId, metaDataKey, metaDataValue):
            meta_data = cls(metaId=metaId, metaDataKey=metaDataKey, metaDataValue=metaDataValue)
            session.add(meta_data)
            session.flush()

            return meta_data

    class Meta(Base):
        __tablename__ = 'meta'

        metaId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

        @classmethod
        def create(cls, metaDataDict=None):
            meta = cls()
            session.add(meta)
            session.flush()

            if metaDataDict:
                for meta_key in metaDataDict:
                    meta_value = metaDataDict[meta_key]
                    meta.add_meta_data(metaDataKey=meta_key, metaDataValue=meta_value)

            return meta

        def add_meta_data(self, metaDataKey, metaDataValue):
            return MetaData.create(metaId=self.metaId, metaDataKey=metaDataKey, metaDataValue=metaDataValue)

    class Folder(Base):
        __tablename__ = 'folder'
        folderId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

        @classmethod
        def create(cls):
            folder = cls()
            session.add(folder)
            session.flush()

            return folder

    class Proof(Base):
        __tablename__ = 'proof'
        proofId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        proofType = sa.Column(sa.String(50), nullable=False)
        proofStampId = sa.Column(sa.Integer, nullable=False)
        scannedFilesFolderId = sa.Column(sa.Integer, nullable=False)
        finished = sa.Column(sa.Boolean, default=False)

        @classmethod
        def create(cls, proofType="ManuallyFilledTallySheets"):
            proof = cls(
                proofType=proofType,
                scannedFilesFolderId=Folder.create().folderId,
                proofStampId=Stamp.create().stampId
            )

            session.add(proof)
            session.flush()

            return proof

        def close(self):
            self.finished = True

            session.add(self)
            session.flush()

    class History(Base):
        __tablename__ = 'history'
        historyId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

        @classmethod
        def create(cls):
            history = cls()
            session.add(history)
            session.flush()

            return history

    class HistoryVersion(Base):
        __tablename__ = 'history_version'
        historyVersionId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        historyId = sa.Column(sa.Integer)
        historyStampId = sa.Column(sa.Integer)

        @classmethod
        def create(cls, historyId, stampId):
            history_version = cls(
                historyId=historyId,
                historyStampId=stampId
            )

            session.add(history_version)
            session.flush()

            return history_version

    class Workflow(Base):
        __tablename__ = 'workflow'

        workflowId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        workflowName = sa.Column(sa.String(100), nullable=False)
        firstStatus = sa.Column(sa.String(100), nullable=False)
        lastStatus = sa.Column(sa.String(100), nullable=False)

        @classmethod
        def create(cls, workflowName, statuses, actions, firstStatus, lastStatus):
            workflow: Workflow = cls(workflowName=workflowName, firstStatus=firstStatus, lastStatus=lastStatus)
            session.add(workflow)
            session.flush()

            for status in statuses:
                WorkflowStatus.create(
                    workflowId=workflow.workflowId,
                    status=status
                )

            for action in actions:
                WorkflowAction.create(
                    workflowId=workflow.workflowId,
                    actionName=action["name"],
                    actionType=action["type"],
                    fromStatus=action["fromStatus"],
                    toStatus=action["toStatus"]
                )

            return workflow

        def get_new_instance(self):
            workflow_instance = WorkflowInstance.create(workflowId=self.workflowId, status=self.firstStatus)

            return workflow_instance

    class WorkflowStatus(Base):
        __tablename__ = 'workflowStatus'

        workflowStatusId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        workflowId = sa.Column(sa.Integer, nullable=False)
        status = sa.Column(sa.String(100), nullable=False)

        @classmethod
        def create(cls, workflowId, status):
            workflow_status = cls(
                workflowId=workflowId,
                status=status
            )
            session.add(workflow_status)
            session.flush()

            return workflow_status

    class WorkflowAction(Base):
        __tablename__ = 'workflowAction'

        workflowActionId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        workflowId = sa.Column(sa.Integer, nullable=False)
        actionName = sa.Column(sa.String(100), nullable=False)
        actionType = sa.Column(sa.String(100), nullable=False)
        fromStatus = sa.Column(sa.String(100), nullable=False)
        toStatus = sa.Column(sa.String(100), nullable=False)

        @classmethod
        def create(cls, workflowId, actionName, actionType, fromStatus, toStatus):
            workflow_status_action = cls(
                workflowId=workflowId,
                actionName=actionName,
                actionType=actionType,
                fromStatus=fromStatus,
                toStatus=toStatus
            )
            session.add(workflow_status_action)
            session.flush()

            return workflow_status_action

    class WorkflowInstanceLog(Base):
        __tablename__ = 'workflowInstanceLog'

        workflowInstanceLogId = sa.Column(sa.Integer, primary_key=True)
        workflowInstanceId = sa.Column(sa.Integer, nullable=False)
        status = sa.Column(sa.String(100), nullable=False)
        workflowActionId = sa.Column(sa.Integer, nullable=False)
        metaId = sa.Column(sa.Integer, nullable=True)
        proofId = sa.Column(sa.Integer, nullable=True)

        @classmethod
        def create(cls, workflowInstanceId, status, workflowActionId, metaId, proofId, stampId):
            workflow_log = cls(
                workflowInstanceLogId=HistoryVersion.create(historyId=workflowInstanceId,
                                                            stampId=stampId).historyVersionId,
                workflowInstanceId=workflowInstanceId,
                status=status,
                workflowActionId=workflowActionId,
                metaId=metaId,
                proofId=proofId
            )
            session.add(workflow_log)
            session.flush()

            return workflow_log

    class WorkflowInstance(Base):
        __tablename__ = 'workflowInstance'

        workflowInstanceId = sa.Column(sa.Integer, primary_key=True)
        workflowId = sa.Column(sa.Integer, nullable=False)
        status = sa.Column(sa.String(100), nullable=False)
        latestLogId = sa.Column(sa.Integer, nullable=True)
        proofId = sa.Column(sa.Integer, nullable=True)

        @classmethod
        def create(cls, workflowId, status):
            workflow_action = cls(
                workflowInstanceId=History.create().historyId,
                proofId=Proof.create().proofId,
                workflowId=workflowId,
                status=status
            )
            session.add(workflow_action)
            session.flush()

            return workflow_action

        def execute_action(self, action: WorkflowAction, meta: Meta, stampId, proofId=None):
            if self.status != action.fromStatus:
                pass
            else:

                # handle existing proofs
                if proofId is not None:
                    self.proofId = proofId

                proof = session.query(Proof).filter(Proof.proofId == self.proofId).one_or_none()
                proof.close()

                self.status = action.toStatus
                self.latestLogId = WorkflowInstanceLog.create(
                    workflowInstanceId=self.workflowInstanceId,
                    status=action.toStatus,
                    workflowActionId=action.workflowActionId,
                    metaId=meta.metaId,
                    stampId=stampId,
                    proofId=self.proofId
                ).workflowInstanceLogId

                self.proofId = Proof.create().proofId

                session.add(self)
                session.flush()

                return self

    class Submission(Base):
        __tablename__ = 'submission'
        submissionId = sa.Column(sa.Integer, primary_key=True)
        latestVersionId = sa.Column(sa.Integer, nullable=True)
        latestStampId = sa.Column(sa.Integer, nullable=True)
        lockedVersionId = sa.Column(sa.Integer, nullable=True)
        lockedStampId = sa.Column(sa.Integer, nullable=True)
        submittedVersionId = sa.Column(sa.Integer, nullable=True)
        submittedStampId = sa.Column(sa.Integer, nullable=True)
        notifiedVersionId = sa.Column(sa.Integer, nullable=True)
        notifiedStampId = sa.Column(sa.Integer, nullable=True)
        releasedVersionId = sa.Column(sa.Integer, nullable=True)
        releasedStampId = sa.Column(sa.Integer, nullable=True)
        submissionProofId = sa.Column(sa.Integer, nullable=True)

    class TallySheet(Base):
        __tablename__ = 'tallySheet'

        tallySheetId = sa.Column(sa.Integer, primary_key=True)
        templateId = sa.Column(sa.Integer, nullable=False)
        metaId = sa.Column(sa.Integer, nullable=False)
        workflowInstanceId = sa.Column(sa.Integer, nullable=True)

    class Template(Base):
        __tablename__ = 'template'

        templateId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        templateName = sa.Column(sa.String(100), nullable=False)

    workflow_data_entry: Workflow = Workflow.create(
        workflowName="Data Entry",
        firstStatus=WORKFLOW_STATUS_TYPE_EMPTY,
        lastStatus=WORKFLOW_STATUS_TYPE_VERIFIED,
        statuses=[
            WORKFLOW_STATUS_TYPE_EMPTY,
            WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED,
            WORKFLOW_STATUS_TYPE_SAVED,
            WORKFLOW_STATUS_TYPE_SUBMITTED,
            WORKFLOW_STATUS_TYPE_VERIFIED
        ],
        actions=[
            {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
             "fromStatus": WORKFLOW_STATUS_TYPE_EMPTY, "toStatus": WORKFLOW_STATUS_TYPE_EMPTY},
            {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
             "fromStatus": WORKFLOW_STATUS_TYPE_SAVED, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
            {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
             "fromStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED,
             "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
            {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
             "fromStatus": WORKFLOW_STATUS_TYPE_SUBMITTED, "toStatus": WORKFLOW_STATUS_TYPE_SUBMITTED},
            {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
             "fromStatus": WORKFLOW_STATUS_TYPE_VERIFIED, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},

            {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT,
             "fromStatus": WORKFLOW_STATUS_TYPE_SUBMITTED, "toStatus": WORKFLOW_STATUS_TYPE_SUBMITTED},
            {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT,
             "fromStatus": WORKFLOW_STATUS_TYPE_VERIFIED, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},

            {"name": "Enter", "type": WORKFLOW_ACTION_TYPE_SAVE,
             "fromStatus": WORKFLOW_STATUS_TYPE_EMPTY, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
            {"name": "EDIT", "type": WORKFLOW_ACTION_TYPE_SAVE,
             "fromStatus": WORKFLOW_STATUS_TYPE_SAVED, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},

            {"name": "Submit", "type": WORKFLOW_ACTION_TYPE_SUBMIT,
             "fromStatus": WORKFLOW_STATUS_TYPE_SAVED, "toStatus": WORKFLOW_STATUS_TYPE_SUBMITTED},

            {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY,
             "fromStatus": WORKFLOW_STATUS_TYPE_SUBMITTED, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},

            {"name": "Edit", "type": WORKFLOW_ACTION_TYPE_EDIT,
             "fromStatus": WORKFLOW_STATUS_TYPE_SUBMITTED, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},

            {"name": "Edit", "type": WORKFLOW_ACTION_TYPE_EDIT,
             "fromStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},

            {"name": "Request Changes", "type": WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
             "fromStatus": WORKFLOW_STATUS_TYPE_SUBMITTED, "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},

            {"name": "Request Changes", "type": WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
             "fromStatus": WORKFLOW_STATUS_TYPE_VERIFIED, "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED}
        ]
    )

    workflow_released_report: Workflow = Workflow.create(
        workflowName="Data Entry",
        firstStatus=WORKFLOW_STATUS_TYPE_EMPTY,
        lastStatus=WORKFLOW_STATUS_TYPE_RELEASED,
        statuses=[
            WORKFLOW_STATUS_TYPE_EMPTY,
            WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED,
            WORKFLOW_STATUS_TYPE_SAVED,
            WORKFLOW_STATUS_TYPE_VERIFIED,
            WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY,
            WORKFLOW_STATUS_TYPE_CERTIFIED,
            WORKFLOW_STATUS_TYPE_RELEASED
        ],
        actions=[
            {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
             "fromStatus": WORKFLOW_STATUS_TYPE_EMPTY, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
            {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
             "fromStatus": WORKFLOW_STATUS_TYPE_SAVED, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
            {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
             "fromStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED,
             "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
            {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
             "fromStatus": WORKFLOW_STATUS_TYPE_VERIFIED, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
            {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
             "fromStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY,
             "toStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY},
            {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
             "fromStatus": WORKFLOW_STATUS_TYPE_CERTIFIED, "toStatus": WORKFLOW_STATUS_TYPE_CERTIFIED},
            {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
             "fromStatus": WORKFLOW_STATUS_TYPE_RELEASED, "toStatus": WORKFLOW_STATUS_TYPE_RELEASED},

            {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT,
             "fromStatus": WORKFLOW_STATUS_TYPE_VERIFIED, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
            {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT,
             "fromStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY,
             "toStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY},
            {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT,
             "fromStatus": WORKFLOW_STATUS_TYPE_CERTIFIED, "toStatus": WORKFLOW_STATUS_TYPE_CERTIFIED},
            {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT,
             "fromStatus": WORKFLOW_STATUS_TYPE_RELEASED, "toStatus": WORKFLOW_STATUS_TYPE_RELEASED},

            {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY,
             "fromStatus": WORKFLOW_STATUS_TYPE_EMPTY, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
            {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY,
             "fromStatus": WORKFLOW_STATUS_TYPE_SAVED, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
            {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY,
             "fromStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},

            {"name": "Print and Certify", "type": WORKFLOW_ACTION_TYPE_MOVE_TO_CERTIFY,
             "fromStatus": WORKFLOW_STATUS_TYPE_VERIFIED, "toStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY},

            {"name": "Upload and Certify", "type": WORKFLOW_ACTION_TYPE_CERTIFY,
             "fromStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY, "toStatus": WORKFLOW_STATUS_TYPE_CERTIFIED},

            {"name": "Release", "type": WORKFLOW_ACTION_TYPE_RELEASE,
             "fromStatus": WORKFLOW_STATUS_TYPE_CERTIFIED, "toStatus": WORKFLOW_STATUS_TYPE_RELEASED},

            {"name": "Request Changes", "type": WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
             "fromStatus": WORKFLOW_STATUS_TYPE_VERIFIED, "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
            {"name": "Request Changes", "type": WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
             "fromStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY,
             "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
            {"name": "Request Changes", "type": WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
             "fromStatus": WORKFLOW_STATUS_TYPE_CERTIFIED, "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
            {"name": "Request Changes", "type": WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
             "fromStatus": WORKFLOW_STATUS_TYPE_RELEASED, "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED}
        ]
    )
    session.commit()

    existing_report_tally_sheets = session.query(TallySheet).filter(
        TallySheet.workflowInstanceId == None,
        Template.templateId == TallySheet.templateId,
        Template.templateName.in_([
            PRE_30_PD, PRE_30_ED, PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS, PRE_ALL_ISLAND_RESULTS,
            PRE_34_I_RO, PRE_34_II_RO, PRE_34,
            PRE_30_PD_PV, PRE_34_PD, PRE_34_ED, PRE_34_AI
        ])
    ).all()
    report_enter_actions = session.query(WorkflowAction).filter(
        WorkflowAction.workflowId == workflow_released_report.workflowId,
        WorkflowAction.fromStatus == WORKFLOW_STATUS_TYPE_EMPTY,
        WorkflowAction.toStatus == WORKFLOW_STATUS_TYPE_SAVED
    ).all()
    report_save_actions = session.query(WorkflowAction).filter(
        WorkflowAction.workflowId == workflow_released_report.workflowId,
        WorkflowAction.fromStatus == WORKFLOW_STATUS_TYPE_SAVED,
        WorkflowAction.toStatus == WORKFLOW_STATUS_TYPE_SAVED
    ).all()
    report_verify_actions = session.query(WorkflowAction).filter(
        WorkflowAction.workflowId == workflow_released_report.workflowId,
        WorkflowAction.fromStatus == WORKFLOW_STATUS_TYPE_SAVED,
        WorkflowAction.toStatus == WORKFLOW_STATUS_TYPE_VERIFIED
    ).all()
    report_move_to_certify_actions = session.query(WorkflowAction).filter(
        WorkflowAction.workflowId == workflow_released_report.workflowId,
        WorkflowAction.fromStatus == WORKFLOW_STATUS_TYPE_VERIFIED,
        WorkflowAction.toStatus == WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY
    ).all()
    report_certify_actions = session.query(WorkflowAction).filter(
        WorkflowAction.workflowId == workflow_released_report.workflowId,
        WorkflowAction.fromStatus == WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY,
        WorkflowAction.toStatus == WORKFLOW_STATUS_TYPE_CERTIFIED
    ).all()
    report_release_actions = session.query(WorkflowAction).filter(
        WorkflowAction.workflowId == workflow_released_report.workflowId,
        WorkflowAction.fromStatus == WORKFLOW_STATUS_TYPE_CERTIFIED,
        WorkflowAction.toStatus == WORKFLOW_STATUS_TYPE_RELEASED
    ).all()

    print(" -- Updating the workflow of existing report tally sheets.")
    for tally_sheet in tqdm(existing_report_tally_sheets):
        workflow_instance: WorkflowInstance = workflow_released_report.get_new_instance()
        tally_sheet.workflowInstanceId = workflow_instance.workflowInstanceId
        session.add(tally_sheet)
        session.commit()

        tally_sheet_versions = session.query(
            HistoryVersion.historyVersionId.label("tallySheetVersionId"),
            HistoryVersion.historyStampId.label("stampId")
        ).filter(
            HistoryVersion.historyId == tally_sheet.tallySheetId
        ).order_by(HistoryVersion.historyVersionId).all()

        for tally_sheet_version_index in range(len(tally_sheet_versions)):
            tally_sheet_version = tally_sheet_versions[tally_sheet_version_index]
            if tally_sheet_version_index == 0:
                for action in report_enter_actions:
                    workflow_instance.execute_action(
                        action=action,
                        meta=Meta.create({"tallySheetVersionId": tally_sheet_version.tallySheetVersionId}),
                        stampId=tally_sheet_version.stampId
                    )
                    session.commit()
            else:
                for action in report_save_actions:
                    workflow_instance.execute_action(
                        action=action,
                        meta=Meta.create({"tallySheetVersionId": tally_sheet_version.tallySheetVersionId}),
                        stampId=tally_sheet_version.stampId
                    )
                    session.commit()

        submission = session.query(Submission).filter(Submission.submissionId == tally_sheet.tallySheetId).one_or_none()

        if submission.lockedVersionId is not None:
            for action in report_verify_actions + report_move_to_certify_actions:
                workflow_instance.execute_action(
                    action=action,
                    meta=Meta.create({"tallySheetVersionId": submission.lockedVersionId}),
                    stampId=submission.lockedStampId
                )
                session.commit()

        if submission.notifiedVersionId is not None:
            for action in report_certify_actions:
                workflow_instance.execute_action(
                    action=action,
                    meta=Meta.create({"tallySheetVersionId": submission.notifiedVersionId}),
                    stampId=submission.notifiedStampId
                )
                session.commit()

        if submission.releasedVersionId is not None:
            for action in report_release_actions:
                workflow_instance.execute_action(
                    action=action,
                    meta=Meta.create({"tallySheetVersionId": submission.releasedVersionId}),
                    stampId=submission.releasedStampId,
                    proofId=submission.submissionProofId
                )
                session.commit()

    existing_data_entry_tally_sheets = session.query(TallySheet).filter(
        TallySheet.tallySheetId == Submission.submissionId,
        TallySheet.workflowInstanceId == None,
        Template.templateId == TallySheet.templateId,
        Template.templateName.in_([
            PRE_28, PRE_41, PRE_21, CE_201_PV, CE_201, PRE_34_CO
        ])
    ).all()
    data_entry_enter_actions = session.query(WorkflowAction).filter(
        WorkflowAction.workflowId == workflow_data_entry.workflowId,
        WorkflowAction.fromStatus == WORKFLOW_STATUS_TYPE_EMPTY,
        WorkflowAction.toStatus == WORKFLOW_STATUS_TYPE_SAVED
    ).all()
    data_entry_save_actions = session.query(WorkflowAction).filter(
        WorkflowAction.workflowId == workflow_data_entry.workflowId,
        WorkflowAction.fromStatus == WORKFLOW_STATUS_TYPE_SAVED,
        WorkflowAction.toStatus == WORKFLOW_STATUS_TYPE_SAVED
    ).all()
    data_entry_submit_actions = session.query(WorkflowAction).filter(
        WorkflowAction.workflowId == workflow_data_entry.workflowId,
        WorkflowAction.fromStatus == WORKFLOW_STATUS_TYPE_SAVED,
        WorkflowAction.toStatus == WORKFLOW_STATUS_TYPE_SUBMITTED
    ).all()
    data_entry_verify_actions = session.query(WorkflowAction).filter(
        WorkflowAction.workflowId == workflow_data_entry.workflowId,
        WorkflowAction.fromStatus == WORKFLOW_STATUS_TYPE_SUBMITTED,
        WorkflowAction.toStatus == WORKFLOW_STATUS_TYPE_VERIFIED
    ).all()

    print(" -- Updating the workflow of existing data entry tally sheets.")
    for tally_sheet in tqdm(existing_data_entry_tally_sheets):
        workflow_instance: WorkflowInstance = workflow_data_entry.get_new_instance()
        tally_sheet.workflowInstanceId = workflow_instance.workflowInstanceId
        session.add(tally_sheet)
        session.commit()

        tally_sheet_versions = session.query(
            HistoryVersion.historyVersionId.label("tallySheetVersionId"),
            HistoryVersion.historyStampId.label("stampId")
        ).filter(
            HistoryVersion.historyId == tally_sheet.tallySheetId
        ).order_by(HistoryVersion.historyVersionId).all()

        for tally_sheet_version_index in range(len(tally_sheet_versions)):
            tally_sheet_version = tally_sheet_versions[tally_sheet_version_index]
            if tally_sheet_version_index == 0:
                for action in data_entry_enter_actions:
                    workflow_instance.execute_action(
                        action=action,
                        meta=Meta.create({"tallySheetVersionId": tally_sheet_version.tallySheetVersionId}),
                        stampId=tally_sheet_version.stampId
                    )
                    session.commit()
            else:
                for action in data_entry_save_actions:
                    workflow_instance.execute_action(
                        action=action,
                        meta=Meta.create({"tallySheetVersionId": tally_sheet_version.tallySheetVersionId}),
                        stampId=tally_sheet_version.stampId
                    )
                    session.commit()

        submission = session.query(Submission).filter(Submission.submissionId == tally_sheet.tallySheetId).one_or_none()

        if submission.submittedVersionId is not None:
            for action in data_entry_submit_actions:
                workflow_instance.execute_action(
                    action=action,
                    meta=Meta.create({"tallySheetVersionId": submission.submittedVersionId}),
                    stampId=submission.submittedStampId
                )
                session.commit()

        if submission.lockedVersionId is not None:
            for action in data_entry_verify_actions:
                workflow_instance.execute_action(
                    action=action,
                    meta=Meta.create({"tallySheetVersionId": submission.lockedVersionId}),
                    stampId=submission.lockedStampId
                )
                session.commit()

    session.commit()


def downgrade():
    op.drop_constraint('tallySheet_fk_workflowInstanceId', 'tallySheet', type_='foreignkey')
    op.drop_constraint('workflowInstance_fk_latestLogId', 'workflowInstance', type_='foreignkey')
    op.drop_column('tallySheet', 'workflowInstanceId')
    op.drop_table('workflowStatus')
    op.drop_table('workflowInstanceLog')
    op.drop_table('workflowInstance')
    op.drop_table('workflowAction')
    op.drop_table('workflow')
