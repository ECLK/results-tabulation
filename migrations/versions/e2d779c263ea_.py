"""empty message

Revision ID: e2d779c263ea
Revises: 3c39e8314e54
Create Date: 2019-11-12 18:43:36.999892

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e2d779c263ea'
down_revision = '3c39e8314e54'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('dashboard_status_report', sa.Column('electionId', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'dashboard_status_report', 'election', ['electionId'], ['electionId'])

    Base = declarative_base()

    class _ElectionModel(Base):
        __tablename__ = 'election'
        electionId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        electionName = sa.Column(sa.String(100), nullable=False)
        parentElectionId = sa.Column(sa.Integer, sa.ForeignKey("election.electionId"), nullable=True)

        subElections = relationship("_ElectionModel")
        parentElection = relationship("_ElectionModel", remote_side=[electionId])

    class _StatusReportModel(Base):
        __tablename__ = 'dashboard_status_report'

        statusReportId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        electionId = sa.Column(sa.Integer, sa.ForeignKey(_ElectionModel.__table__.c.electionId), nullable=True)

    class _SubmissionModel(Base):
        __tablename__ = 'submission'
        submissionId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        electionId = sa.Column(sa.Integer, sa.ForeignKey(_ElectionModel.__table__.c.electionId), nullable=False)

    class _TallySheetModel(Base):
        __tablename__ = 'tallySheet'

        tallySheetId = sa.Column(sa.Integer, sa.ForeignKey(_SubmissionModel.__table__.c.submissionId), primary_key=True)
        statusReportId = sa.Column(sa.Integer, sa.ForeignKey(_StatusReportModel.__table__.c.statusReportId),
                                   nullable=True)

        submission = relationship("_SubmissionModel", foreign_keys=[tallySheetId])
        statusReport = relationship(_StatusReportModel, foreign_keys=[statusReportId])

    bind = op.get_bind()
    session = Session(bind=bind)

    existing_root_elections = session.query(_ElectionModel).filter(_ElectionModel.parentElectionId == None).all()
    for root_election in existing_root_elections:
        root_election_id = root_election.electionId
        mapped_election_ids = [root_election_id]
        for sub_election in root_election.subElections:
            mapped_election_ids.append(sub_election.electionId)

        tally_sheets = session.query(
            _TallySheetModel
        ).join(
            _SubmissionModel,
            _SubmissionModel.submissionId == _TallySheetModel.tallySheetId
        ).filter(
            _SubmissionModel.electionId.in_(mapped_election_ids)
        )

        for tally_sheet in tally_sheets:
            tally_sheet.statusReport.electionId = root_election_id

    session.commit()


def downgrade():
    op.drop_constraint(None, 'dashboard_status_report', type_='foreignkey')
    op.drop_column('dashboard_status_report', 'electionId')
