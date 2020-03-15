"""empty message

Revision ID: 8e6be037a5a6
Revises: 3971c2f9c31f
Create Date: 2020-03-15 15:56:46.247767

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8e6be037a5a6'
down_revision = '3971c2f9c31f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'status',
        sa.Column('statusId', sa.Integer(), nullable=False),
        sa.Column('statusName', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('statusId')
    )
    op.create_table(
        'statusAction',
        sa.Column('statusActionId', sa.Integer(), nullable=False),
        sa.Column('statusActionName', sa.String(length=100), nullable=False),
        sa.Column('statusActionType', sa.String(length=100), nullable=False),
        sa.Column('fromStatusId', sa.Integer(), nullable=False),
        sa.Column('toStatusId', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['fromStatusId'], ['status.statusId'], 'statusAction_fk_fromStatusId'),
        sa.ForeignKeyConstraint(['toStatusId'], ['status.statusId'], 'statusAction_fk_toStatusId'),
        sa.PrimaryKeyConstraint('statusActionId')
    )
    op.create_table(
        'workflow',
        sa.Column('workflowId', sa.Integer(), nullable=False),
        sa.Column('workflowName', sa.String(length=100), nullable=False),
        sa.Column('firstStatusId', sa.Integer(), nullable=False),
        sa.Column('lastStatusId', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['firstStatusId'], ['status.statusId'], 'workflowStatus_fk_firstStatusId'),
        sa.ForeignKeyConstraint(['lastStatusId'], ['status.statusId'], 'workflowStatus_fk_lastStatusId'),
        sa.PrimaryKeyConstraint('workflowId')
    )
    op.create_table(
        'workflowInstance',
        sa.Column('workflowInstanceId', sa.Integer(), nullable=False),
        sa.Column('workflowId', sa.Integer(), nullable=False),
        sa.Column('statusId', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['statusId'], ['status.statusId'], 'workflowInstance_fk_statusId'),
        sa.ForeignKeyConstraint(['workflowId'], ['workflow.workflowId'], 'workflowInstance_fk_workflowId'),
        sa.ForeignKeyConstraint(['workflowInstanceId'], ['history.historyId'],
                                'workflowInstance_fk_workflowInstanceId'),
        sa.PrimaryKeyConstraint('workflowInstanceId')
    )
    op.create_table(
        'workflowInstanceLog',
        sa.Column('workflowInstanceLogId', sa.Integer(), nullable=False),
        sa.Column('workflowInstanceId', sa.Integer(), nullable=False),
        sa.Column('statusId', sa.Integer(), nullable=False),
        sa.Column('statusActionId', sa.Integer(), nullable=False),
        sa.Column('metaId', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['metaId'], ['meta.metaId'], 'workflowInstanceLog_fk_metaId'),
        sa.ForeignKeyConstraint(['statusActionId'], ['statusAction.statusActionId'],
                                'workflowInstanceLog_fk_statusActionId'),
        sa.ForeignKeyConstraint(['statusId'], ['status.statusId'], 'workflowInstanceLog_fk_statusId'),
        sa.ForeignKeyConstraint(['workflowInstanceId'], ['workflowInstance.workflowInstanceId'],
                                'workflowInstanceLog_fk_workflowInstanceId'),
        sa.ForeignKeyConstraint(['workflowInstanceLogId'], ['history_version.historyVersionId'],
                                'workflowInstanceLog_fk_workflowInstanceLogId'),
        sa.PrimaryKeyConstraint('workflowInstanceLogId')
    )
    op.create_table(
        'workflowStatus',
        sa.Column('workflowStatusId', sa.Integer(), nullable=False),
        sa.Column('workflowId', sa.Integer(), nullable=False),
        sa.Column('statusId', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['statusId'], ['status.statusId'], 'workflowStatus_fk_statusId'),
        sa.ForeignKeyConstraint(['workflowId'], ['workflow.workflowId'], 'workflowStatus_fk_workflowId'),
        sa.PrimaryKeyConstraint('workflowStatusId')
    )
    op.create_table(
        'workflowStatusAction',
        sa.Column('workflowStatusActionId', sa.Integer(), nullable=False),
        sa.Column('workflowId', sa.Integer(), nullable=False),
        sa.Column('statusActionId', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['statusActionId'], ['statusAction.statusActionId'],
                                'workflowStatusAction_fk_statusActionId'),
        sa.ForeignKeyConstraint(['workflowId'], ['workflow.workflowId'], 'workflowStatusAction_fk_workflowId'),
        sa.PrimaryKeyConstraint('workflowStatusActionId')
    )
    op.add_column('tallySheet', sa.Column('workflowInstanceId', sa.Integer(), nullable=True))
    op.create_foreign_key('tallySheet_fk_workflowInstanceId', 'tallySheet', 'workflowInstance', ['workflowInstanceId'],
                          ['workflowInstanceId'])


def downgrade():
    op.drop_constraint('tallySheet_fk_workflowInstanceId', 'tallySheet', type_='foreignkey')
    op.drop_column('tallySheet', 'workflowInstanceId')
    op.drop_table('workflowStatusAction')
    op.drop_table('workflowStatus')
    op.drop_table('workflowInstanceLog')
    op.drop_table('workflowInstance')
    op.drop_table('workflow')
    op.drop_table('statusAction')
    op.drop_table('status')
