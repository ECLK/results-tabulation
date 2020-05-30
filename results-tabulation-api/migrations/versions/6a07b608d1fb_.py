"""empty message

Revision ID: 6a07b608d1fb
Revises: 8da6a3e78339
Create Date: 2019-11-14 16:35:46.385240

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

# revision identifiers, used by Alembic.
revision = '6a07b608d1fb'
down_revision = '8da6a3e78339'
branch_labels = None
depends_on = None


def upgrade():
    Base = declarative_base()
    bind = op.get_bind()
    session = Session(bind=bind)

    class _NewTallySheetVersionRow_PRE_34_preference_Model(Base):
        __tablename__ = 'tallySheetVersionRow_PRE_34_Preference'
        tallySheetVersionRowId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        tallySheetVersionId = sa.Column(sa.Integer, nullable=False)
        electionId = sa.Column(sa.Integer, nullable=False)
        candidateId = sa.Column(sa.Integer, nullable=True)
        areaId = sa.Column(sa.Integer, nullable=True)
        preferenceNumber = sa.Column(sa.Integer, nullable=False)
        preferenceCount = sa.Column(sa.Integer, nullable=False)

    existing_records = session.query(
        _NewTallySheetVersionRow_PRE_34_preference_Model.tallySheetVersionRowId,
        _NewTallySheetVersionRow_PRE_34_preference_Model.tallySheetVersionId,
        _NewTallySheetVersionRow_PRE_34_preference_Model.electionId,
        _NewTallySheetVersionRow_PRE_34_preference_Model.candidateId,
        _NewTallySheetVersionRow_PRE_34_preference_Model.preferenceNumber,
        _NewTallySheetVersionRow_PRE_34_preference_Model.preferenceCount
    ).all()

    op.drop_table('tallySheetVersionRow_PRE_34_Preference')
    op.create_table(
        'tallySheetVersionRow_PRE_34_Preference',
        sa.Column('tallySheetVersionRowId', sa.Integer(), nullable=False),
        sa.Column('tallySheetVersionId', sa.Integer(), nullable=False),
        sa.Column('electionId', sa.Integer(), nullable=False),
        sa.Column('candidateId', sa.Integer(), nullable=True),
        sa.Column('areaId', sa.Integer(), nullable=True),
        sa.Column('preferenceNumber', sa.Integer(), nullable=False),
        sa.Column('preferenceCount', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['areaId'], ['area.areaId'], ),
        sa.ForeignKeyConstraint(['candidateId'], ['candidate.candidateId'], ),
        sa.ForeignKeyConstraint(['electionId'], ['election.electionId'], ),
        sa.ForeignKeyConstraint(['tallySheetVersionId'], ['tallySheetVersion.tallySheetVersionId'], ),
        sa.PrimaryKeyConstraint('tallySheetVersionRowId'),
        sa.UniqueConstraint('tallySheetVersionId', 'preferenceNumber', 'candidateId', 'areaId',
                            name='TallySheetVersionRow_PRE_34_preference_Model_uk')
    )

    for existing_record in existing_records:
        session.add(_NewTallySheetVersionRow_PRE_34_preference_Model(
            electionId=existing_record.electionId,
            tallySheetVersionId=existing_record.tallySheetVersionId,
            preferenceNumber=existing_record.preferenceNumber,
            preferenceCount=existing_record.preferenceCount,
            candidateId=existing_record.candidateId
        ))

    session.commit()


def downgrade():
    Base = declarative_base()
    bind = op.get_bind()
    session = Session(bind=bind)

    class _NewTallySheetVersionRow_PRE_34_preference_Model(Base):
        __tablename__ = 'tallySheetVersionRow_PRE_34_Preference'
        tallySheetVersionRowId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        tallySheetVersionId = sa.Column(sa.Integer, nullable=False)
        electionId = sa.Column(sa.Integer, nullable=False)
        candidateId = sa.Column(sa.Integer, nullable=True)
        areaId = sa.Column(sa.Integer, nullable=True)
        preferenceNumber = sa.Column(sa.Integer, nullable=False)
        preferenceCount = sa.Column(sa.Integer, nullable=False)

    existing_records = session.query(
        _NewTallySheetVersionRow_PRE_34_preference_Model.tallySheetVersionRowId,
        _NewTallySheetVersionRow_PRE_34_preference_Model.tallySheetVersionId,
        _NewTallySheetVersionRow_PRE_34_preference_Model.electionId,
        _NewTallySheetVersionRow_PRE_34_preference_Model.candidateId,
        _NewTallySheetVersionRow_PRE_34_preference_Model.preferenceNumber,
        _NewTallySheetVersionRow_PRE_34_preference_Model.preferenceCount
    ).all()

    op.drop_table('tallySheetVersionRow_PRE_34_Preference')
    op.create_table(
        'tallySheetVersionRow_PRE_34_Preference',
        sa.Column('tallySheetVersionRowId', sa.Integer(), nullable=False),
        sa.Column('tallySheetVersionId', sa.Integer(), nullable=False),
        sa.Column('electionId', sa.Integer(), nullable=False),
        sa.Column('candidateId', sa.Integer(), nullable=True),
        sa.Column('preferenceNumber', sa.Integer(), nullable=False),
        sa.Column('preferenceCount', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['candidateId'], ['candidate.candidateId'], ),
        sa.ForeignKeyConstraint(['electionId'], ['election.electionId'], ),
        sa.ForeignKeyConstraint(['tallySheetVersionId'], ['tallySheetVersion.tallySheetVersionId'], ),
        sa.PrimaryKeyConstraint('tallySheetVersionRowId'),
        sa.UniqueConstraint('tallySheetVersionId', 'preferenceNumber', 'candidateId',
                            name='TallySheetVersionRow_PRE_34_preference_Model_uk')
    )

    for existing_record in existing_records:
        session.add(_NewTallySheetVersionRow_PRE_34_preference_Model(
            electionId=existing_record.electionId,
            tallySheetVersionId=existing_record.tallySheetVersionId,
            preferenceNumber=existing_record.preferenceNumber,
            preferenceCount=existing_record.preferenceCount,
            candidateId=existing_record.candidateId
        ))

    session.commit()
