"""empty message

Revision ID: a07d014866a1
Revises: 3971c2f9c31f
Create Date: 2020-03-12 20:45:36.320151

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

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
        sa.Column('workflowFirstStatusId', sa.Integer(), nullable=False),
        sa.Column('workflowLastStatusId', sa.Integer(), nullable=False),
        sa.Column('workflowCurrentStatusId', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('workflowId')
    )
    op.create_table(
        'workflowAction',
        sa.Column('workflowActionId', sa.Integer(), nullable=False),
        sa.Column('workflowId', sa.Integer(), nullable=False),
        sa.Column('workflowActionName', sa.String(length=100), nullable=False),
        sa.Column('workflowActionType', sa.String(length=100), nullable=False),
        sa.Column('workflowActionFromStatusId', sa.Integer(), nullable=False),
        sa.Column('workflowActionToStatusId', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('workflowActionId')
    )
    op.create_table(
        'workflowLog',
        sa.Column('workflowLogId', sa.Integer(), nullable=False),
        sa.Column('workflowId', sa.Integer(), nullable=False),
        sa.Column('workflowLogStatusId', sa.Integer(), nullable=False),
        sa.Column('workflowLogActionId', sa.Integer(), nullable=False),
        sa.Column('metaId', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('workflowLogId')
    )
    op.create_table(
        'workflowStatus',
        sa.Column('workflowStatusId', sa.Integer(), nullable=False),
        sa.Column('workflowId', sa.Integer(), nullable=False),
        sa.Column('workflowStatusName', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('workflowStatusId')
    )

    op.create_foreign_key(
        'workflow_fk_workflowCurrentStatusId', 'workflow', 'workflowStatus',
        ['workflowCurrentStatusId'], ['workflowStatusId']
    )
    op.create_foreign_key('workflow_fk_workflowLastStatusId', 'workflow', 'workflowStatus', ['workflowLastStatusId'],
                          ['workflowStatusId'])
    op.create_foreign_key('workflow_fk_workflowFirstStatusId', 'workflow', 'workflowStatus', ['workflowFirstStatusId'],
                          ['workflowStatusId'])

    op.alter_column('workflowAction', 'workflowActionFromStatusId', existing_type=mysql.INTEGER(display_width=11))
    op.alter_column('workflowAction', 'workflowActionToStatusId', existing_type=mysql.INTEGER(display_width=11))
    op.create_foreign_key('workflowAction_fk_workflowActionFromStatusId', 'workflowAction', 'workflowStatus',
                          ['workflowActionFromStatusId'], ['workflowStatusId'])
    op.create_foreign_key('workflowAction_fk_workflowActionToStatusId', 'workflowAction', 'workflowStatus',
                          ['workflowActionToStatusId'], ['workflowStatusId'])
    op.create_foreign_key('workflowAction_fk_workflowId', 'workflowAction', 'workflow', ['workflowId'], ['workflowId'])

    op.alter_column('workflowLog', 'workflowLogActionId', existing_type=mysql.INTEGER(display_width=11))
    op.alter_column('workflowLog', 'workflowLogStatusId', existing_type=mysql.INTEGER(display_width=11))
    op.create_foreign_key('workflowLog_fk_workflowId', 'workflowLog', 'workflow', ['workflowId'], ['workflowId'])
    op.create_foreign_key('workflowLog_fk_workflowLogStatusId', 'workflowLog', 'workflowStatus',
                          ['workflowLogStatusId'], ['workflowStatusId'])
    op.create_foreign_key('workflowLog_fk_metaId', 'workflowLog', 'meta', ['metaId'], ['metaId'])
    op.create_foreign_key('workflowLog_fk_workflowLogActionId', 'workflowLog', 'workflowAction',
                          ['workflowLogActionId'], ['workflowActionId'])

    op.create_foreign_key('workflowStatus_fk_workflowId', 'workflowStatus', 'workflow', ['workflowId'], ['workflowId'])


def downgrade():
    op.drop_constraint('workflow_fk_workflowLastStatusId', 'workflow', type_='foreignkey')
    op.drop_constraint('workflow_fk_workflowFirstStatusId', 'workflow', type_='foreignkey')

    op.drop_constraint('workflowAction_fk_workflowActionFromStatusId', 'workflowAction', type_='foreignkey')
    op.drop_constraint('workflowAction_fk_workflowActionToStatusId', 'workflowAction', type_='foreignkey')
    op.drop_constraint('workflowAction_fk_workflowId', 'workflowAction', type_='foreignkey')

    op.drop_constraint('workflowLog_fk_workflowId', 'workflowLog', type_='foreignkey')
    op.drop_constraint('workflowLog_fk_workflowLogStatusId', 'workflowLog', type_='foreignkey')
    op.drop_constraint('workflowLog_fk_metaId', 'workflowLog', type_='foreignkey')
    op.drop_constraint('workflowLog_fk_workflowLogActionId', 'workflowLog', type_='foreignkey')

    op.drop_constraint('workflowStatus_fk_workflowId', 'workflowStatus', type_='foreignkey')

    op.drop_table('workflow')
    op.drop_table('workflowStatus')
    op.drop_table('workflowAction')
    op.drop_table('workflowLog')
