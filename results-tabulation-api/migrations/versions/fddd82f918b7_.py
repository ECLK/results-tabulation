"""Merge `submission` and `tallySheet` tables.

Revision ID: fddd82f918b7
Revises: b7b04e64002a
Create Date: 2020-08-14 18:10:16.232820

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from tqdm import tqdm

revision = 'fddd82f918b7'
down_revision = 'b7b04e64002a'
branch_labels = None
depends_on = None

Base = declarative_base()
bind = op.get_bind()
session = Session(bind=bind)
db = sa


def upgrade():
    op.add_column('tallySheet', sa.Column('areaId', sa.Integer(), nullable=True))
    op.add_column('tallySheet', sa.Column('electionId', sa.Integer(), nullable=True))
    op.add_column('tallySheet', sa.Column('latestVersionId', sa.Integer(), nullable=True))
    op.add_column('tallySheetVersion', sa.Column('tallySheetId', sa.Integer(), nullable=True))

    class _Submission(Base):
        __tablename__ = 'submission'
        submissionId = db.Column(db.Integer, primary_key=True)
        electionId = db.Column(db.Integer)
        areaId = db.Column(db.Integer)
        latestVersionId = db.Column(db.Integer)

    class _TallySheet(Base):
        __tablename__ = 'tallySheet'
        tallySheetId = db.Column(db.Integer, primary_key=True)
        electionId = db.Column(db.Integer)
        areaId = db.Column(db.Integer)
        latestVersionId = db.Column(db.Integer)

    class _SubmissionVersion(Base):
        __tablename__ = 'submissionVersion'
        submissionVersionId = db.Column(db.Integer, primary_key=True)
        submissionId = db.Column(db.Integer, primary_key=True)

    class _TallySheetVersion(Base):
        __tablename__ = 'tallySheetVersion'
        tallySheetVersionId = db.Column(db.Integer, primary_key=True)
        tallySheetId = db.Column(db.Integer)

    submissions = session.query(_Submission).all()
    submission_map = {submission.submissionId: submission for submission in submissions}
    tally_sheets = session.query(_TallySheet).all()
    tally_sheet_map = {tally_sheet.tallySheetId: tally_sheet for tally_sheet in tally_sheets}

    print(" -- Updating the existing tally sheets.")
    for tally_sheet in tqdm(tally_sheets):
        submission = submission_map[tally_sheet.tallySheetId]
        tally_sheet.electionId = submission.electionId
        tally_sheet.areaId = submission.areaId
        tally_sheet.latestVersionId = submission.latestVersionId
        session.add(tally_sheet)

    session.commit()

    submission_versions = session.query(_SubmissionVersion).all()
    submission_version_map = {submission_version.submissionVersionId: submission_version for submission_version in
                              submission_versions}
    tally_sheet_versions = session.query(_TallySheetVersion).all()
    tally_sheet_version_map = {tally_sheet_version.tallySheetVersionId: tally_sheet_version for tally_sheet_version in
                               tally_sheet_versions}

    print(" -- Updating the existing tally sheet versions.")
    for tally_sheet_version in tqdm(tally_sheet_versions):
        submission_version = submission_version_map[tally_sheet_version.tallySheetVersionId]
        tally_sheet_version.tallySheetId = submission_version.submissionId
        session.add(tally_sheet_version)

    session.commit()

    op.drop_constraint('tallySheet_ibfk_1', 'tallySheet', type_='foreignkey')
    op.create_foreign_key(op.f('fk_tallySheet_areaId_area'), 'tallySheet', 'area', ['areaId'], ['areaId'])
    op.create_foreign_key(op.f('fk_tallySheet_tallySheetId_history'), 'tallySheet', 'history', ['tallySheetId'],
                          ['historyId'])
    op.create_foreign_key(op.f('fk_tallySheet_electionId_election'), 'tallySheet', 'election', ['electionId'],
                          ['electionId'])
    op.create_foreign_key(op.f('fk_tallySheet_latestVersionId_tallySheetVersion'), 'tallySheet', 'tallySheetVersion',
                          ['latestVersionId'], ['tallySheetVersionId'])
    op.drop_constraint('tallySheetVersion_ibfk_1', 'tallySheetVersion', type_='foreignkey')
    op.create_foreign_key(op.f('fk_tallySheetVersion_tallySheetId_tallySheet'), 'tallySheetVersion', 'tallySheet',
                          ['tallySheetId'], ['tallySheetId'])
    op.create_foreign_key(op.f('fk_tallySheetVersion_tallySheetVersionId_history_version'), 'tallySheetVersion',
                          'history_version', ['tallySheetVersionId'], ['historyVersionId'])

    op.drop_constraint(op.f('submission_ibfk_5'), 'submission', type_='foreignkey')
    op.drop_constraint(op.f('submission_ibfk_13'), 'submission', type_='foreignkey')
    op.drop_constraint(op.f('submission_ibfk_15'), 'submission', type_='foreignkey')
    op.drop_constraint(op.f('submission_ibfk_7'), 'submission', type_='foreignkey')
    op.drop_constraint(op.f('submission_ibfk_8'), 'submission', type_='foreignkey')
    op.drop_constraint(op.f('submissionVersion_ibfk_1'), 'submissionVersion', type_='foreignkey')
    op.drop_constraint(op.f('submissionVersion_ibfk_2'), 'submissionVersion', type_='foreignkey')
    op.drop_table('submissionVersion')
    op.drop_table('submission')


def downgrade():
    op.drop_constraint(op.f('fk_tallySheetVersion_tallySheetVersionId_history_version'), 'tallySheetVersion',
                       type_='foreignkey')
    op.drop_constraint(op.f('fk_tallySheetVersion_tallySheetId_tallySheet'), 'tallySheetVersion', type_='foreignkey')
    op.create_foreign_key('tallySheetVersion_ibfk_1', 'tallySheetVersion', 'submissionVersion', ['tallySheetVersionId'],
                          ['submissionVersionId'])
    op.drop_column('tallySheetVersion', 'tallySheetId')
    op.drop_constraint(op.f('fk_tallySheet_latestVersionId_tallySheetVersion'), 'tallySheet', type_='foreignkey')
    op.drop_constraint(op.f('fk_tallySheet_electionId_election'), 'tallySheet', type_='foreignkey')
    op.drop_constraint(op.f('fk_tallySheet_tallySheetId_history'), 'tallySheet', type_='foreignkey')
    op.drop_constraint(op.f('fk_tallySheet_areaId_area'), 'tallySheet', type_='foreignkey')
    op.create_foreign_key('tallySheet_ibfk_1', 'tallySheet', 'submission', ['tallySheetId'], ['submissionId'])
    op.drop_column('tallySheet', 'latestVersionId')
    op.drop_column('tallySheet', 'electionId')
    op.drop_column('tallySheet', 'areaId')

    op.create_table(
        'submission',
        sa.Column('submissionId', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
        sa.Column('submissionType', mysql.ENUM('TallySheet', 'Report', collation='utf8mb4_unicode_ci'),
                  nullable=False),
        sa.Column('electionId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('areaId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('submissionProofId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.Column('latestVersionId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('lockedVersionId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('submittedVersionId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=True),
        sa.Column('lockedStampId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('submittedStampId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('latestStampId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('notifiedStampId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('notifiedVersionId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('releasedStampId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('releasedVersionId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['areaId'], ['area.areaId'], name='submission_ibfk_1'),
        sa.ForeignKeyConstraint(['electionId'], ['election.electionId'], name='submission_ibfk_2'),
        sa.ForeignKeyConstraint(['latestStampId'], ['stamp.stampId'], name='submission_ibfk_11'),
        sa.ForeignKeyConstraint(['latestVersionId'], ['submissionVersion.submissionVersionId'],
                                name='submission_ibfk_5'),
        sa.ForeignKeyConstraint(['lockedStampId'], ['stamp.stampId'], name='submission_ibfk_9'),
        sa.ForeignKeyConstraint(['lockedVersionId'], ['submissionVersion.submissionVersionId'],
                                name='submission_ibfk_7'),
        sa.ForeignKeyConstraint(['notifiedStampId'], ['stamp.stampId'], name='submission_ibfk_14'),
        sa.ForeignKeyConstraint(['notifiedVersionId'], ['submissionVersion.submissionVersionId'],
                                name='submission_ibfk_15'),
        sa.ForeignKeyConstraint(['releasedStampId'], ['stamp.stampId'], name='submission_ibfk_12'),
        sa.ForeignKeyConstraint(['releasedVersionId'], ['submissionVersion.submissionVersionId'],
                                name='submission_ibfk_13'),
        sa.ForeignKeyConstraint(['submissionId'], ['history.historyId'], name='submission_ibfk_6'),
        sa.ForeignKeyConstraint(['submissionProofId'], ['proof.proofId'], name='submission_ibfk_4'),
        sa.ForeignKeyConstraint(['submittedStampId'], ['stamp.stampId'], name='submission_ibfk_10'),
        sa.ForeignKeyConstraint(['submittedVersionId'], ['submissionVersion.submissionVersionId'],
                                name='submission_ibfk_8'),
        sa.PrimaryKeyConstraint('submissionId'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'submissionVersion',
        sa.Column('submissionVersionId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.Column('submissionId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['submissionId'], ['submission.submissionId'],
                                name='submissionVersion_ibfk_1'),
        sa.ForeignKeyConstraint(['submissionVersionId'], ['history_version.historyVersionId'],
                                name='submissionVersion_ibfk_2'),
        sa.PrimaryKeyConstraint('submissionVersionId'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
