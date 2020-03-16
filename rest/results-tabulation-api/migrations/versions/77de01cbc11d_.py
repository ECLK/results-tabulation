"""empty message

Revision ID: 77de01cbc11d
Revises: 3971c2f9c31f
Create Date: 2020-03-16 12:43:36.803804

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '77de01cbc11d'
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
        sa.ForeignKeyConstraint(['workflowId'], ['workflow.workflowId'], 'workflowInstance_fk_workflowId'),
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
        sa.ForeignKeyConstraint(['metaId'], ['meta.metaId'], 'workflowInstanceLog_fk_metaId'),
        sa.ForeignKeyConstraint(['workflowActionId'], ['workflowAction.workflowActionId'],
                                'workflowInstanceLog_fk_workflowActionId'),
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
        sa.Column('status', sa.String(length=100), nullable=False),
        sa.ForeignKeyConstraint(['workflowId'], ['workflow.workflowId'], 'workflowStatus_fk_workflowId'),
        sa.PrimaryKeyConstraint('workflowStatusId')
    )

    op.add_column('tallySheet', sa.Column('workflowInstanceId', sa.Integer(), nullable=True))
    op.create_foreign_key('tallySheet_fk_workflowInstanceId', 'tallySheet', 'workflowInstance', ['workflowInstanceId'],
                          ['workflowInstanceId'])
    op.create_foreign_key('workflowInstance_fk_latestLogId', 'workflowInstance', 'workflowInstanceLog', ['latestLogId'],
                          ['workflowInstanceLogId'])


def downgrade():
    op.drop_constraint('tallySheet_fk_workflowInstanceId', 'tallySheet', type_='foreignkey')
    op.drop_constraint('workflowInstance_fk_latestLogId', 'workflowInstance', type_='foreignkey')
    op.drop_column('tallySheet', 'workflowInstanceId')
    op.drop_table('workflowStatus')
    op.drop_table('workflowInstanceLog')
    op.drop_table('workflowInstance')
    op.drop_table('workflowAction')
    op.drop_table('workflow')
