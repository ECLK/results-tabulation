"""empty message

Revision ID: 9cb6d7971778
Revises: a4b00dd4b387
Create Date: 2020-01-23 17:46:41.554467

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import literal, func
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from tqdm import tqdm

# revision identifiers, used by Alembic.
from constants.TALLY_SHEET_COLUMN_SOURCE import TALLY_SHEET_COLUMN_SOURCE_CONTENT, TALLY_SHEET_COLUMN_SOURCE_META
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019 import PRE_34_CO, PRE_34_I_RO, PRE_34_II_RO, PRE_34, \
    PRE_34_PD, PRE_34_ED, PRE_34_AI

revision = '9cb6d7971778'
down_revision = 'a4b00dd4b387'
branch_labels = None
depends_on = None


def upgrade():
    Base = declarative_base()
    bind = op.get_bind()
    session = Session(bind=bind)
    db = sa

    op.create_table(
        'template',
        sa.Column('templateId', sa.Integer(), nullable=False),
        sa.Column('templateName', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('templateId')
    )
    op.create_table(
        'templateRow',
        sa.Column('templateRowId', sa.Integer(), nullable=False),
        sa.Column('templateId', sa.Integer(), nullable=True),
        sa.Column('templateRowType', sa.String(length=200), nullable=False),
        sa.Column('hasMany', sa.Boolean(), nullable=False),
        sa.Column('isDerived', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['templateId'], ['template.templateId'], ),
        sa.PrimaryKeyConstraint('templateRowId')
    )
    op.create_table(
        'templateRowColumn',
        sa.Column('templateRowColumnId', sa.Integer(), nullable=False),
        sa.Column('templateRowId', sa.Integer(), nullable=True),
        sa.Column('templateRowColumnName', sa.String(length=200), nullable=False),
        sa.Column('grouped', sa.Boolean(), nullable=False),
        sa.Column('func', sa.String(length=200), nullable=True),
        sa.ForeignKeyConstraint(['templateRowId'], ['templateRow.templateRowId'], ),
        sa.PrimaryKeyConstraint('templateRowColumnId')
    )
    op.create_table(
        'templateRow_derivativeTemplateRow',
        sa.Column('templateRowId', sa.Integer(), nullable=False),
        sa.Column('derivativeTemplateRowId', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['derivativeTemplateRowId'], ['templateRow.templateRowId'], ),
        sa.ForeignKeyConstraint(['templateRowId'], ['templateRow.templateRowId'], ),
        sa.PrimaryKeyConstraint('templateRowId', 'derivativeTemplateRowId')
    )

    op.create_table(
        'tallySheetVersionRow',
        sa.Column('tallySheetVersionRowId', sa.Integer(), nullable=False),
        sa.Column('templateRowId', sa.Integer(), nullable=False),
        sa.Column('tallySheetVersionId', sa.Integer(), nullable=False),
        sa.Column('electionId', sa.Integer(), nullable=False),
        sa.Column('areaId', sa.Integer(), nullable=True),
        sa.Column('candidateId', sa.Integer(), nullable=True),
        sa.Column('partyId', sa.Integer(), nullable=True),
        sa.Column('numValue', sa.Integer(), nullable=True),
        sa.Column('strValue', sa.String(length=100), nullable=True),
        sa.Column('dateValue', sa.DateTime(), nullable=True),
        sa.Column('ballotBoxId', sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(['areaId'], ['area.areaId'], ),
        sa.ForeignKeyConstraint(['templateRowId'], ['templateRow.templateRowId'], ),
        sa.ForeignKeyConstraint(['candidateId'], ['candidate.candidateId'], ),
        sa.ForeignKeyConstraint(['electionId'], ['election.electionId'], ),
        sa.ForeignKeyConstraint(['partyId'], ['party.partyId'], ),
        sa.ForeignKeyConstraint(['tallySheetVersionId'], ['tallySheetVersion.tallySheetVersionId'], ),
        sa.PrimaryKeyConstraint('tallySheetVersionRowId')
    )
    op.create_table(
        'tallySheet_map',
        sa.Column('tallySheetMapId', sa.Integer(), nullable=False),
        sa.Column('pre_41_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('pre_34_co_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('ce_201_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('ce_201_pv_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('pre_30_pd_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('pre_34_i_ro_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('pre_34_pd_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('pre_30_ed_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('pre_34_ii_ro_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('pre_34_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('pre_34_ed_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('pre_all_island_ed_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('pre_all_island_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('pre_34_ai_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('pe_27_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('pe_4_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('pe_ce_ro_v1_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('pe_r1_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('pe_ce_ro_pr_1_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('pe_ce_ro_v2_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('pe_r2_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('pe_ce_ro_pr_2_tallySheetId', sa.Integer(), nullable=True),
        sa.Column('pe_ce_ro_pr_3_tallySheetId', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['ce_201_pv_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['ce_201_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pe_27_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pe_4_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pe_ce_ro_pr_1_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pe_ce_ro_pr_2_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pe_ce_ro_pr_3_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pe_ce_ro_v1_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pe_ce_ro_v2_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pe_r1_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pe_r2_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pre_30_ed_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pre_30_pd_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pre_34_ai_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pre_34_co_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pre_34_ed_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pre_34_i_ro_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pre_34_ii_ro_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pre_34_pd_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pre_34_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pre_41_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pre_all_island_ed_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['pre_all_island_tallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.PrimaryKeyConstraint('tallySheetMapId')
    )
    op.create_table(
        'tallySheet_tallySheet',
        sa.Column('parentTallySheetId', sa.Integer(), nullable=False),
        sa.Column('childTallySheetId', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['childTallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.ForeignKeyConstraint(['parentTallySheetId'], ['tallySheet.tallySheetId'], ),
        sa.PrimaryKeyConstraint('parentTallySheetId', 'childTallySheetId')
    )

    op.alter_column(
        'area_map', 'voteType',
        existing_type=mysql.ENUM('Postal', 'NonPostal', 'PostalAndNonPostal',
                                 collation='utf8mb4_unicode_ci'),
        type_=sa.String(length=100),
        nullable=False)
    op.add_column('election', sa.Column('electionTemplateName', sa.String(length=100), nullable=True))
    op.alter_column(
        'election', 'isListed',
        existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=100),
        type_=sa.Boolean(),
        existing_nullable=False)
    op.alter_column(
        'election', 'voteType',
        existing_type=mysql.ENUM('Postal', 'NonPostal', 'PostalAndNonPostal',
                                 collation='utf8mb4_unicode_ci'),
        type_=sa.String(length=100),
        existing_nullable=False)
    op.add_column('tallySheet', sa.Column('templateId', sa.Integer(), nullable=True))

    class _Election(Base):
        __tablename__ = 'election'
        electionId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        electionTemplateName = db.Column(db.String(100))
        rootElectionId = sa.Column(sa.Integer,
                                   sa.ForeignKey("election.electionId", name="fk_election_root_election_id"),
                                   nullable=True)
        parentElectionId = sa.Column(sa.Integer, sa.ForeignKey("election.electionId"), nullable=True)

    class _ElectionCandidate(Base):
        __tablename__ = 'election_candidate'
        electionCandidateId = db.Column(db.Integer, primary_key=True, autoincrement=True)
        electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=False)
        partyId = db.Column(db.Integer, nullable=False)
        candidateId = db.Column(db.Integer, nullable=False)
        qualifiedForPreferences = db.Column(db.Boolean, default=False, nullable=False)

    class _AreaMap(Base):
        __tablename__ = 'area_map'
        areaMapId = db.Column(db.Integer, primary_key=True, autoincrement=True)
        electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=True)
        voteType = db.Column(db.String(100), nullable=False)
        pollingStationId = db.Column(db.Integer, nullable=True)
        countingCentreId = db.Column(db.Integer, nullable=True)
        districtCentreId = db.Column(db.Integer, nullable=True)
        electionCommissionId = db.Column(db.Integer, nullable=True)
        pollingDistrictId = db.Column(db.Integer, nullable=True)
        pollingDivisionId = db.Column(db.Integer, nullable=True)
        electoralDistrictId = db.Column(db.Integer, nullable=True)
        countryId = db.Column(db.Integer, nullable=True)

    class _Submission(Base):
        __tablename__ = 'submission'
        submissionId = db.Column(sa.Integer, primary_key=True)
        electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=False)
        areaId = db.Column(db.Integer, nullable=False)
        latestVersionId = db.Column(db.Integer, db.ForeignKey("submissionVersion.submissionVersionId"), nullable=True)
        latestStampId = db.Column(db.Integer, db.ForeignKey("stamp.stampId"), nullable=True)
        lockedVersionId = db.Column(db.Integer, db.ForeignKey("submissionVersion.submissionVersionId"), nullable=True)
        lockedStampId = db.Column(db.Integer, db.ForeignKey("stamp.stampId"), nullable=True)
        submittedVersionId = db.Column(db.Integer, db.ForeignKey("submissionVersion.submissionVersionId"),
                                       nullable=True)
        submittedStampId = db.Column(db.Integer, db.ForeignKey("stamp.stampId"), nullable=True)
        notifiedVersionId = db.Column(db.Integer, db.ForeignKey("submissionVersion.submissionVersionId"), nullable=True)
        notifiedStampId = db.Column(db.Integer, db.ForeignKey("stamp.stampId"), nullable=True)
        releasedVersionId = db.Column(db.Integer, db.ForeignKey("submissionVersion.submissionVersionId"), nullable=True)
        releasedStampId = db.Column(db.Integer, db.ForeignKey("stamp.stampId"), nullable=True)

    class _SubmissionVersion(Base):
        __tablename__ = 'submissionVersion'
        submissionVersionId = db.Column(sa.Integer, primary_key=True)
        submissionId = db.Column(db.Integer, db.ForeignKey("submission.submissionId"))

        submission = relationship("_Submission", foreign_keys=[submissionId])

    class _TallySheet(Base):
        __tablename__ = 'tallySheet'

        tallySheetId = db.Column(db.Integer, db.ForeignKey("submission.submissionId"), primary_key=True)
        templateId = db.Column(db.Integer, db.ForeignKey("template.templateId"), nullable=False)
        tallySheetCode = db.Column(db.String(100), nullable=True)

        submission = relationship("_Submission", foreign_keys=[tallySheetId])

        def add_parent(self, parentTallySheet):
            parentTallySheet.add_child(self.tallySheetId)

            return self

        def add_child(self, childTallySheet):
            existing_mapping = session.query(_TallySheetTallySheet).filter(
                _TallySheetTallySheet.parentTallySheetId == self.tallySheetId,
                _TallySheetTallySheet.childTallySheetId == childTallySheet.tallySheetId
            ).one_or_none()

            if existing_mapping is None:
                session.add(_TallySheetTallySheet(
                    parentTallySheetId=self.tallySheetId,
                    childTallySheetId=childTallySheet.tallySheetId
                ))
                session.flush()

            return self

    class _TallySheetTallySheet(Base):
        __tablename__ = 'tallySheet_tallySheet'
        parentTallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), primary_key=True)
        childTallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), primary_key=True)

    class _TallySheetMap(Base):
        __tablename__ = 'tallySheet_map'
        tallySheetMapId = db.Column(db.Integer, primary_key=True)

        pre_41_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
        pre_34_co_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
        ce_201_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
        ce_201_pv_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)

        pre_30_pd_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
        pre_34_i_ro_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
        pre_34_pd_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)

        pre_30_ed_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
        pre_34_ii_ro_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
        pre_34_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
        pre_34_ed_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)

        pre_all_island_ed_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
        pre_all_island_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
        pre_34_ai_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)

        pe_27_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
        pe_4_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
        pe_ce_ro_v1_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
        pe_r1_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
        pe_ce_ro_pr_1_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
        pe_ce_ro_v2_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
        pe_r2_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
        pe_ce_ro_pr_2_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
        pe_ce_ro_pr_3_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)

    class _TallySheetVersion(Base):
        __tablename__ = 'tallySheetVersion'
        tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("submissionVersion.submissionVersionId"),
                                        primary_key=True)
        isComplete = db.Column(db.Boolean, default=False, nullable=False)

    class _TallySheetVersionRow(Base):
        __tablename__ = 'tallySheetVersionRow'
        tallySheetVersionRowId = db.Column(db.Integer, primary_key=True)
        templateRowId = db.Column(db.Integer, nullable=False)
        tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheetVersion.tallySheetVersionId"),
                                        nullable=False)
        electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=False)
        areaId = db.Column(db.Integer, nullable=True)
        candidateId = db.Column(db.Integer, nullable=True)
        partyId = db.Column(db.Integer, nullable=True)
        ballotBoxId = db.Column(db.String(100), nullable=True)
        numValue = db.Column(db.Integer, nullable=True)
        strValue = db.Column(db.String(100), nullable=True)
        dateValue = db.Column(db.DateTime, nullable=True)

    class _TallySheetVersionRow_RejectedVoteCount(Base):
        __tablename__ = 'tallySheetVersionRow_RejectedVoteCount'
        tallySheetVersionRowId = db.Column(db.Integer, primary_key=True)
        tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheetVersion.tallySheetVersionId"),
                                        nullable=False)
        electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=False)
        areaId = db.Column(db.Integer, nullable=True)
        candidateId = db.Column(db.Integer, nullable=True)
        rejectedVoteCount = db.Column(db.Integer, nullable=False)

    class _Template(Base):
        __tablename__ = 'template'
        templateId = db.Column(db.Integer, primary_key=True, autoincrement=True)
        templateName = db.Column(db.String(100), nullable=False)

        def __init__(self, templateName):
            super(_Template, self).__init__(templateName=templateName)
            session.add(self)
            session.flush()

        def add_row(self, templateRowType, hasMany=False, isDerived=False, columns=[]):
            session.add(self)
            session.flush()

            templateRow = _TemplateRow(
                templateId=self.templateId,
                templateRowType=templateRowType,
                hasMany=hasMany,
                isDerived=isDerived
            )

            session.add(templateRow)
            session.flush()

            for column in columns:
                session.add(
                    templateRow.add_column(column["columnName"], grouped=column["grouped"], func=column["func"]))

            return templateRow

    class _TemplateRow(Base):
        __tablename__ = 'templateRow'
        templateRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
        templateId = db.Column(db.Integer, db.ForeignKey("template.templateId"))
        templateRowType = db.Column(db.String(200), nullable=False)
        hasMany = db.Column(db.Boolean, nullable=False, default=False)
        isDerived = db.Column(db.Boolean, nullable=False, default=False)

        def add_derivative_template_row(self, derivativeTemplateRow):
            session.add(_TemplateRow_DerivativeTemplateRow(
                templateRowId=self.templateRowId,
                derivativeTemplateRowId=derivativeTemplateRow.templateRowId
            ))
            session.flush()

            return self

        def add_column(self, templateRowColumnName, grouped=False, func=None):
            return _TemplateRowColumn(
                templateRowId=self.templateRowId,
                templateRowColumnName=templateRowColumnName,
                grouped=grouped,
                func=func
            )

    class _TemplateRowColumn(Base):
        __tablename__ = 'templateRowColumn'
        templateRowColumnId = db.Column(db.Integer, primary_key=True, autoincrement=True)
        templateRowId = db.Column(db.Integer, db.ForeignKey("templateRow.templateRowId"))
        templateRowColumnName = db.Column(db.String(200), nullable=False)
        grouped = db.Column(db.Boolean, default=False, nullable=False)
        func = db.Column(db.String(200), nullable=True)

    class _TemplateRow_DerivativeTemplateRow(Base):
        __tablename__ = 'templateRow_derivativeTemplateRow'
        templateRowId = db.Column(db.Integer, db.ForeignKey("templateRow.templateRowId"), primary_key=True, default=0)
        derivativeTemplateRowId = db.Column(db.Integer, db.ForeignKey("templateRow.templateRowId"), primary_key=True,
                                            default=0)

    def save_existing_tally_sheet_version_rows(existing_tally_sheet_version_rows, label=""):
        tally_sheet_version_row_attribute_names = ["tallySheetVersionId", "templateRowId", "electionId", "areaId",
                                                   "partyId", "candidateId",
                                                   "numValue", "strValue", "dateValue", "ballotBoxId"]
        existing_tally_sheet_version_rows_count = len(existing_tally_sheet_version_rows)
        existing_tally_sheet_version_rows_last_index = existing_tally_sheet_version_rows_count - 1

        print(" -- migrate tally sheet rows (%s)" % label)
        for existing_tally_sheet_version_row_index in tqdm(range(existing_tally_sheet_version_rows_count)):
            existing_tally_sheet_version_row = existing_tally_sheet_version_rows[existing_tally_sheet_version_row_index]
            tally_sheet_version_row_dict = {}
            for tally_sheet_version_row_attribute_name in tally_sheet_version_row_attribute_names:
                if hasattr(existing_tally_sheet_version_row, tally_sheet_version_row_attribute_name):
                    tally_sheet_version_row_dict[tally_sheet_version_row_attribute_name] = getattr(
                        existing_tally_sheet_version_row, tally_sheet_version_row_attribute_name
                    )

            session.add(_TallySheetVersionRow(**tally_sheet_version_row_dict))

            # To make the commit by batches
            if existing_tally_sheet_version_row_index % 1000 == 0:
                session.commit()

            # To commit the last batch
            if existing_tally_sheet_version_row_index == existing_tally_sheet_version_rows_last_index:
                session.commit()

    #################################################################################################################
    # Update existing election's electionTemplateName
    #################################################################################################################
    existing_elections = session.query(
        _Election
    ).all()

    # Update all existing election's template to "PRESIDENTIAL_ELECTION_2019"
    for existing_election in existing_elections:
        existing_election.electionTemplateName = "PRESIDENTIAL_ELECTION_2019"
        session.add(existing_election)

    session.commit()

    # END ###########################################################################################################

    #################################################################################################################
    # Update mappings between tally sheets
    #################################################################################################################
    print(" -- update mappings (parent/ child) between tally sheets")
    for existing_election in tqdm(existing_elections):
        counting_centres = session.query(
            _AreaMap.countingCentreId,
            _AreaMap.pollingDivisionId,
            _AreaMap.electoralDistrictId,
            _AreaMap.countryId,
            _AreaMap.voteType
        ).filter(
            _AreaMap.electionId == existing_election.electionId
        ).group_by(
            _AreaMap.countingCentreId,
            _AreaMap.pollingDivisionId,
            _AreaMap.electoralDistrictId,
            _AreaMap.countryId,
            _AreaMap.voteType
        ).all()

        for counting_centre in counting_centres:
            pre_ai_tally_sheet = session.query(_TallySheet).join(
                _Submission,
                _Submission.submissionId == _TallySheet.tallySheetId
            ).filter(
                _TallySheet.tallySheetCode == "PRE_ALL_ISLAND_RESULTS",
                _Submission.areaId == counting_centre.countryId
            ).one_or_none()
            pre_ai_ed_tally_sheet = session.query(_TallySheet).join(
                _Submission,
                _Submission.submissionId == _TallySheet.tallySheetId
            ).filter(
                _TallySheet.tallySheetCode == "PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS",
                _Submission.areaId == counting_centre.countryId
            ).one_or_none()
            pre_34_ai_tally_sheet = session.query(_TallySheet).join(
                _Submission,
                _Submission.submissionId == _TallySheet.tallySheetId
            ).filter(
                _TallySheet.tallySheetCode == "PRE_34_AI",
                _Submission.areaId == counting_centre.countryId
            ).one_or_none()
            pre_30_ed_tally_sheet = session.query(_TallySheet).join(
                _Submission,
                _Submission.submissionId == _TallySheet.tallySheetId
            ).filter(
                _TallySheet.tallySheetCode == "PRE_30_ED",
                _Submission.areaId == counting_centre.electoralDistrictId
            ).one_or_none()
            pre_34_tally_sheet = session.query(_TallySheet).join(
                _Submission,
                _Submission.submissionId == _TallySheet.tallySheetId
            ).filter(
                _TallySheet.tallySheetCode == "PRE_34",
                _Submission.areaId == counting_centre.electoralDistrictId
            ).one_or_none()
            pre_34_ii_ro_tally_sheet = session.query(_TallySheet).join(
                _Submission,
                _Submission.submissionId == _TallySheet.tallySheetId
            ).filter(
                _TallySheet.tallySheetCode == "PRE_34_II_RO",
                _Submission.areaId == counting_centre.electoralDistrictId
            ).one_or_none()
            pre_34_ed_tally_sheet = session.query(_TallySheet).join(
                _Submission,
                _Submission.submissionId == _TallySheet.tallySheetId
            ).filter(
                _TallySheet.tallySheetCode == "PRE_34_ED",
                _Submission.areaId == counting_centre.electoralDistrictId
            ).one_or_none()

            if counting_centre.voteType == "Postal":
                pre_30_pd_tally_sheet = session.query(_TallySheet).join(
                    _Submission,
                    _Submission.submissionId == _TallySheet.tallySheetId
                ).filter(
                    _TallySheet.tallySheetCode == "PRE_30_PD",
                    _Submission.areaId == counting_centre.electoralDistrictId
                ).one_or_none()
                pre_34_pd_tally_sheet = session.query(_TallySheet).join(
                    _Submission,
                    _Submission.submissionId == _TallySheet.tallySheetId
                ).filter(
                    _TallySheet.tallySheetCode == "PRE_34_PD",
                    _Submission.areaId == counting_centre.electoralDistrictId
                ).one_or_none()
                pre_34_i_ro_tally_sheet = session.query(_TallySheet).join(
                    _Submission,
                    _Submission.submissionId == _TallySheet.tallySheetId
                ).filter(
                    _TallySheet.tallySheetCode == "PRE_34_I_RO",
                    _Submission.areaId == counting_centre.electoralDistrictId
                ).one_or_none()
            else:
                pre_30_pd_tally_sheet = session.query(_TallySheet).join(
                    _Submission,
                    _Submission.submissionId == _TallySheet.tallySheetId
                ).filter(
                    _TallySheet.tallySheetCode == "PRE_30_PD",
                    _Submission.areaId == counting_centre.pollingDivisionId
                ).one_or_none()
                pre_34_pd_tally_sheet = session.query(_TallySheet).join(
                    _Submission,
                    _Submission.submissionId == _TallySheet.tallySheetId
                ).filter(
                    _TallySheet.tallySheetCode == "PRE_34_PD",
                    _Submission.areaId == counting_centre.pollingDivisionId
                ).one_or_none()
                pre_34_i_ro_tally_sheet = session.query(_TallySheet).join(
                    _Submission,
                    _Submission.submissionId == _TallySheet.tallySheetId
                ).filter(
                    _TallySheet.tallySheetCode == "PRE_34_I_RO",
                    _Submission.areaId == counting_centre.pollingDivisionId
                ).one_or_none()

            pre_41_tally_sheet = session.query(_TallySheet).join(
                _Submission,
                _Submission.submissionId == _TallySheet.tallySheetId
            ).filter(
                _TallySheet.tallySheetCode == "PRE_41",
                _Submission.areaId == counting_centre.countingCentreId
            ).one_or_none()
            pre_34_co_tally_sheet = session.query(_TallySheet).join(
                _Submission,
                _Submission.submissionId == _TallySheet.tallySheetId
            ).filter(
                _TallySheet.tallySheetCode == "PRE_34_CO",
                _Submission.areaId == counting_centre.countingCentreId
            ).one_or_none()

            ce_201_tally_sheet = session.query(_TallySheet).join(
                _Submission,
                _Submission.submissionId == _TallySheet.tallySheetId
            ).filter(
                _TallySheet.tallySheetCode == "CE_201",
                _Submission.areaId == counting_centre.countingCentreId
            ).one_or_none()

            ce_201_pv_tally_sheet = session.query(_TallySheet).join(
                _Submission,
                _Submission.submissionId == _TallySheet.tallySheetId
            ).filter(
                _TallySheet.tallySheetCode == "CE_201_PV",
                _Submission.areaId == counting_centre.countingCentreId
            ).one_or_none()

            pre_30_pd_tally_sheet.add_child(pre_41_tally_sheet)
            pre_30_ed_tally_sheet.add_child(pre_30_pd_tally_sheet)
            pre_ai_ed_tally_sheet.add_child(pre_30_ed_tally_sheet)
            pre_ai_tally_sheet.add_child(pre_ai_ed_tally_sheet)

            pre_34_i_ro_tally_sheet.add_child(pre_34_co_tally_sheet)
            pre_34_ii_ro_tally_sheet.add_child(pre_34_i_ro_tally_sheet)
            pre_34_tally_sheet.add_child(pre_34_ii_ro_tally_sheet)

            pre_34_pd_tally_sheet.add_child(pre_30_pd_tally_sheet)
            pre_34_pd_tally_sheet.add_child(pre_34_i_ro_tally_sheet)
            pre_34_ed_tally_sheet.add_child(pre_34_pd_tally_sheet)
            pre_34_ai_tally_sheet.add_child(pre_34_ed_tally_sheet)

            tally_sheet_map = _TallySheetMap(
                pre_41_tallySheetId=pre_41_tally_sheet.tallySheetId,
                pre_34_co_tallySheetId=pre_34_co_tally_sheet.tallySheetId,
                ce_201_tallySheetId=None if ce_201_tally_sheet is None else ce_201_tally_sheet.tallySheetId,
                ce_201_pv_tallySheetId=None if ce_201_pv_tally_sheet is None else ce_201_pv_tally_sheet.tallySheetId,

                pre_30_pd_tallySheetId=pre_30_pd_tally_sheet.tallySheetId,
                pre_34_i_ro_tallySheetId=pre_34_i_ro_tally_sheet.tallySheetId,
                pre_34_pd_tallySheetId=pre_34_pd_tally_sheet.tallySheetId,

                pre_30_ed_tallySheetId=pre_30_ed_tally_sheet.tallySheetId,
                pre_34_ii_ro_tallySheetId=pre_34_ii_ro_tally_sheet.tallySheetId,
                pre_34_tallySheetId=pre_34_tally_sheet.tallySheetId,
                pre_34_ed_tallySheetId=pre_34_ed_tally_sheet.tallySheetId,

                pre_all_island_ed_tallySheetId=pre_ai_ed_tally_sheet.tallySheetId,
                pre_all_island_tallySheetId=pre_ai_tally_sheet.tallySheetId,
                pre_34_ai_tallySheetId=pre_34_ai_tally_sheet.tallySheetId,
            )

            session.add(tally_sheet_map)

    session.commit()

    # END ###########################################################################################################

    #################################################################################################################
    # CE 201 PV rows
    #################################################################################################################
    class _TallySheetVersionRow_CE_201_PV(Base):
        __tablename__ = 'tallySheetVersionRow_CE_201_PV'
        tallySheetVersionRowId = db.Column(db.Integer, primary_key=True)
        tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheetVersion.tallySheetVersionId"),
                                        nullable=False)
        ballotBoxId = db.Column(db.String(20), nullable=True, default="")
        numberOfPacketsInserted = db.Column(db.Integer, nullable=False)
        numberOfAPacketsFound = db.Column(db.Integer, nullable=False)

    class _TallySheetVersionRow_CE_201_PV_CC(Base):
        __tablename__ = 'tallySheetVersionRow_CE_201_PV_CC'
        tallySheetVersionRowId = db.Column(db.Integer, primary_key=True)
        tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheetVersion.tallySheetVersionId"),
                                        nullable=False)
        countingCentreId = db.Column(db.Integer, nullable=False)
        situation = db.Column(db.String(100), nullable=True)
        timeOfCommencementOfCount = db.Column(db.DateTime, nullable=True)
        numberOfAPacketsFound = db.Column(db.Integer, nullable=False)
        numberOfACoversRejected = db.Column(db.Integer, nullable=False)
        numberOfBCoversRejected = db.Column(db.Integer, nullable=False)
        numberOfValidBallotPapers = db.Column(db.Integer, nullable=False)

    tally_sheet_template_ce_201_pv = _Template(
        templateName="CE-201-PV"
    )

    tally_sheet_template_ce_201_pv_situation_row = tally_sheet_template_ce_201_pv.add_row(
        templateRowType="SITUATION",
        hasMany=False,
        isDerived=False,
        columns=[
            {"columnName": "electionId", "grouped": False, "func": None},
            {"columnName": "areaId", "grouped": False, "func": None},
            {"columnName": "strValue", "grouped": False, "func": None}
        ]
    )
    tally_sheet_template_ce_201_pv_time_of_commencement_row = tally_sheet_template_ce_201_pv.add_row(
        templateRowType="TIME_OF_COMMENCEMENT",
        hasMany=False,
        isDerived=False,
        columns=[
            {"columnName": "electionId", "grouped": False, "func": None},
            {"columnName": "areaId", "grouped": False, "func": None},
            {"columnName": "strValue", "grouped": False, "func": None}
        ]
    )
    tally_sheet_template_ce_201_pv_ballot_box_row = tally_sheet_template_ce_201_pv.add_row(
        templateRowType="BALLOT_BOX",
        hasMany=True,
        isDerived=False,
        columns=[
            {"columnName": "electionId", "grouped": False, "func": None},
            {"columnName": "areaId", "grouped": False, "func": None},
            {"columnName": "ballotBoxId", "grouped": False, "func": None,
             "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
            {"columnName": "strValue", "grouped": False, "func": None}
        ]
    )
    tally_sheet_template_ce_201_pv_number_of_packets_inserted_to_ballot_box_row = tally_sheet_template_ce_201_pv.add_row(
        templateRowType="NUMBER_OF_PACKETS_INSERTED_TO_BALLOT_BOX",
        hasMany=True,
        isDerived=False,
        columns=[
            {"columnName": "electionId", "grouped": False, "func": None},
            {"columnName": "areaId", "grouped": False, "func": None},
            {"columnName": "ballotBoxId", "grouped": False, "func": None,
             "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
            {"columnName": "numValue", "grouped": False, "func": None}
        ]
    )
    tally_sheet_template_ce_201_pv_number_of_packets_found_inside_ballot_box_row = tally_sheet_template_ce_201_pv.add_row(
        templateRowType="NUMBER_OF_PACKETS_FOUND_INSIDE_BALLOT_BOX",
        hasMany=True,
        isDerived=False,
        columns=[
            {"columnName": "electionId", "grouped": False, "func": None},
            {"columnName": "areaId", "grouped": False, "func": None},
            {"columnName": "ballotBoxId", "grouped": False, "func": None,
             "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
            {"columnName": "numValue", "grouped": False, "func": None}
        ]
    )
    tally_sheet_template_ce_201_pv_number_of_packets_rejected_after_opening_cover_a_row = tally_sheet_template_ce_201_pv.add_row(
        templateRowType="NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_A",
        hasMany=False,
        isDerived=False,
        columns=[
            {"columnName": "electionId", "grouped": False, "func": None},
            {"columnName": "areaId", "grouped": False, "func": None},
            {"columnName": "numValue", "grouped": False, "func": None}
        ]
    )
    tally_sheet_template_ce_201_pv_number_of_packets_rejected_after_opening_cover_b_row = tally_sheet_template_ce_201_pv.add_row(
        templateRowType="NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_B",
        hasMany=False,
        isDerived=False,
        columns=[
            {"columnName": "electionId", "grouped": False, "func": None},
            {"columnName": "areaId", "grouped": False, "func": None},
            {"columnName": "numValue", "grouped": False, "func": None}
        ]
    )

    existing_tally_sheets = session.query(
        _TallySheet
    ).filter(
        _TallySheet.tallySheetCode == "CE_201_PV"
    ).all()

    for existing_tally_sheet in existing_tally_sheets:
        existing_tally_sheet.templateId = tally_sheet_template_ce_201_pv.templateId

    class _ROW:
        pass

    # A util method used to append the auto generated column `ballotBoxId` in CE-201-PV.
    def _append_ballot_box_id(rows):
        _ballot_box_id = 0
        _rows = []
        for row in rows:
            _row = _ROW()
            for _row_key in row.keys():
                _row_value = getattr(row, _row_key)
                setattr(_row, _row_key, _row_value)

            setattr(_row, "ballotBoxId", _ballot_box_id)
            _rows.append(_row)

            _ballot_box_id += 1

        return _rows

    existing_tally_sheet_version_rows = session.query(
        _TallySheetVersionRow_CE_201_PV_CC.tallySheetVersionId,
        _Submission.electionId,
        _Submission.areaId,
        _TallySheetVersionRow_CE_201_PV_CC.situation.label("strValue"),
        literal(tally_sheet_template_ce_201_pv_situation_row.templateRowId).label("templateRowId")
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersionRow_CE_201_PV_CC.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).all()

    existing_tally_sheet_version_rows += session.query(
        _TallySheetVersionRow_CE_201_PV_CC.tallySheetVersionId,
        _Submission.electionId,
        _Submission.areaId,
        _TallySheetVersionRow_CE_201_PV_CC.timeOfCommencementOfCount.label("dateValue"),
        literal(tally_sheet_template_ce_201_pv_time_of_commencement_row.templateRowId).label("templateRowId")
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersionRow_CE_201_PV_CC.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).all()

    existing_tally_sheet_version_rows += _append_ballot_box_id(
        rows=session.query(
            _TallySheetVersionRow_CE_201_PV.tallySheetVersionId,
            _Submission.electionId,
            _Submission.areaId,
            literal(0).label("ballotBoxId"),
            _TallySheetVersionRow_CE_201_PV.ballotBoxId.label("strValue"),
            literal(tally_sheet_template_ce_201_pv_ballot_box_row.templateRowId).label("templateRowId")
        ).join(
            _SubmissionVersion,
            _SubmissionVersion.submissionVersionId == _TallySheetVersionRow_CE_201_PV.tallySheetVersionId
        ).join(
            _Submission,
            _Submission.submissionId == _SubmissionVersion.submissionId
        ).all()
    )

    existing_tally_sheet_version_rows += _append_ballot_box_id(
        rows=session.query(
            _TallySheetVersionRow_CE_201_PV.tallySheetVersionId,
            _Submission.electionId,
            _Submission.areaId,
            literal(0).label("ballotBoxId"),
            _TallySheetVersionRow_CE_201_PV.numberOfPacketsInserted.label("numValue"),
            literal(
                tally_sheet_template_ce_201_pv_number_of_packets_inserted_to_ballot_box_row.templateRowId
            ).label("templateRowId")
        ).join(
            _SubmissionVersion,
            _SubmissionVersion.submissionVersionId == _TallySheetVersionRow_CE_201_PV.tallySheetVersionId
        ).join(
            _Submission,
            _Submission.submissionId == _SubmissionVersion.submissionId
        ).all()
    )

    existing_tally_sheet_version_rows += _append_ballot_box_id(
        rows=session.query(
            _TallySheetVersionRow_CE_201_PV.tallySheetVersionId,
            _Submission.electionId,
            _Submission.areaId,
            literal(0).label("ballotBoxId"),
            _TallySheetVersionRow_CE_201_PV.numberOfAPacketsFound.label("numValue"),
            literal(
                tally_sheet_template_ce_201_pv_number_of_packets_found_inside_ballot_box_row.templateRowId
            ).label("templateRowId")
        ).join(
            _SubmissionVersion,
            _SubmissionVersion.submissionVersionId == _TallySheetVersionRow_CE_201_PV.tallySheetVersionId
        ).join(
            _Submission,
            _Submission.submissionId == _SubmissionVersion.submissionId
        ).all()
    )

    existing_tally_sheet_version_rows += session.query(
        _TallySheetVersionRow_CE_201_PV_CC.tallySheetVersionId,
        _Submission.electionId,
        _Submission.areaId,
        _TallySheetVersionRow_CE_201_PV_CC.numberOfACoversRejected.label("numValue"),
        literal(
            tally_sheet_template_ce_201_pv_number_of_packets_rejected_after_opening_cover_a_row.templateRowId
        ).label("templateRowId")
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersionRow_CE_201_PV_CC.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).all()

    existing_tally_sheet_version_rows += session.query(
        _TallySheetVersionRow_CE_201_PV_CC.tallySheetVersionId,
        _Submission.electionId,
        _Submission.areaId,
        _TallySheetVersionRow_CE_201_PV_CC.numberOfBCoversRejected.label("numValue"),
        literal(
            tally_sheet_template_ce_201_pv_number_of_packets_rejected_after_opening_cover_b_row.templateRowId
        ).label("templateRowId")
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersionRow_CE_201_PV_CC.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).all()

    session.commit()

    save_existing_tally_sheet_version_rows(existing_tally_sheet_version_rows, label="CE-201-PV")

    # END ###########################################################################################################

    #################################################################################################################
    # CE 201 rows
    #################################################################################################################
    class _TallySheetVersionRow_CE_201(Base):
        __tablename__ = 'tallySheetVersionRow_CE_201'
        tallySheetVersionRowId = db.Column(db.Integer, primary_key=True)
        tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheetVersion.tallySheetVersionId"),
                                        nullable=False)
        areaId = db.Column(db.Integer, nullable=False)
        ballotsIssued = db.Column(db.Integer, nullable=False)
        ballotsReceived = db.Column(db.Integer, nullable=False)
        ballotsSpoilt = db.Column(db.Integer, nullable=False)
        ballotsUnused = db.Column(db.Integer, nullable=False)
        ordinaryBallotCountFromBoxCount = db.Column(db.Integer, nullable=False)
        tenderedBallotCountFromBoxCount = db.Column(db.Integer, nullable=False)
        ordinaryBallotCountFromBallotPaperAccount = db.Column(db.Integer, nullable=False)
        tenderedBallotCountFromBallotPaperAccount = db.Column(db.Integer, nullable=False)

    tally_sheet_template_ce_201 = _Template(
        templateName="CE-201"
    )
    tally_sheet_template_ce_201_ballot_box_row = tally_sheet_template_ce_201.add_row(
        templateRowType="BALLOT_BOX",
        hasMany=True,
        isDerived=False,
        columns=[
            {"columnName": "electionId", "grouped": False, "func": None},
            {"columnName": "areaId", "grouped": False, "func": None},
            {"columnName": "ballotBoxId", "grouped": False, "func": None}
        ]
    )
    tally_sheet_template_ce_201_number_of_ballots_received = tally_sheet_template_ce_201.add_row(
        templateRowType="NUMBER_OF_BALLOTS_RECEIVED",
        hasMany=True,
        isDerived=False,
        columns=[
            {"columnName": "electionId", "grouped": False, "func": None},
            {"columnName": "areaId", "grouped": False, "func": None},
            {"columnName": "numValue", "grouped": False, "func": None}
        ]
    )
    tally_sheet_template_ce_201_number_of_ballots_spoilt = tally_sheet_template_ce_201.add_row(
        templateRowType="NUMBER_OF_BALLOTS_SPOILT",
        hasMany=True,
        isDerived=False,
        columns=[
            {"columnName": "electionId", "grouped": False, "func": None},
            {"columnName": "areaId", "grouped": False, "func": None},
            {"columnName": "numValue", "grouped": False, "func": None}
        ]
    )
    tally_sheet_template_ce_201_number_of_ballots_issued = tally_sheet_template_ce_201.add_row(
        templateRowType="NUMBER_OF_BALLOTS_ISSUED",
        hasMany=True,
        isDerived=False,
        columns=[
            {"columnName": "electionId", "grouped": False, "func": None},
            {"columnName": "areaId", "grouped": False, "func": None},
            {"columnName": "numValue", "grouped": False, "func": None}
        ]
    )
    tally_sheet_template_ce_201_number_of_ballots_unused = tally_sheet_template_ce_201.add_row(
        templateRowType="NUMBER_OF_BALLOTS_UNUSED",
        hasMany=True,
        isDerived=False,
        columns=[
            {"columnName": "electionId", "grouped": False, "func": None},
            {"columnName": "areaId", "grouped": False, "func": None},
            {"columnName": "numValue", "grouped": False, "func": None}
        ]
    )
    tally_sheet_template_ce_201_number_of_ordinary_ballots_in_ballot_paper_account = tally_sheet_template_ce_201.add_row(
        templateRowType="NUMBER_OF_ORDINARY_BALLOTS_IN_BALLOT_PAPER_ACCOUNT",
        hasMany=True,
        isDerived=False,
        columns=[
            {"columnName": "electionId", "grouped": False, "func": None},
            {"columnName": "areaId", "grouped": False, "func": None},
            {"columnName": "numValue", "grouped": False, "func": None}
        ]
    )
    tally_sheet_template_ce_201_number_of_ordinary_ballots_in_ballot_box = tally_sheet_template_ce_201.add_row(
        templateRowType="NUMBER_OF_ORDINARY_BALLOTS_IN_BALLOT_BOX",
        hasMany=True,
        isDerived=False,
        columns=[
            {"columnName": "electionId", "grouped": False, "func": None},
            {"columnName": "areaId", "grouped": False, "func": None},
            {"columnName": "numValue", "grouped": False, "func": None}
        ]
    )
    tally_sheet_template_ce_201_number_of_tendered_ballots_in_ballot_paper_account = tally_sheet_template_ce_201.add_row(
        templateRowType="NUMBER_OF_TENDERED_BALLOTS_IN_BALLOT_PAPER_ACCOUNT",
        hasMany=True,
        isDerived=False,
        columns=[
            {"columnName": "electionId", "grouped": False, "func": None},
            {"columnName": "areaId", "grouped": False, "func": None},
            {"columnName": "numValue", "grouped": False, "func": None}
        ]
    )
    tally_sheet_template_ce_201_number_of_tendered_ballots_in_ballot_box = tally_sheet_template_ce_201.add_row(
        templateRowType="NUMBER_OF_TENDERED_BALLOTS_IN_BALLOT_BOX",
        hasMany=True,
        isDerived=False,
        columns=[
            {"columnName": "electionId", "grouped": False, "func": None},
            {"columnName": "areaId", "grouped": False, "func": None},
            {"columnName": "numValue", "grouped": False, "func": None}
        ]
    )

    existing_tally_sheets = session.query(
        _TallySheet
    ).filter(
        _TallySheet.tallySheetCode == "CE_201"
    ).all()

    for existing_tally_sheet in existing_tally_sheets:
        existing_tally_sheet.templateId = tally_sheet_template_ce_201.templateId

    existing_tally_sheet_version_rows = session.query(
        _TallySheetVersionRow_CE_201.tallySheetVersionId,
        _Submission.electionId,
        _TallySheetVersionRow_CE_201.areaId.label("areaId"),
        _TallySheetVersionRow_CE_201.ballotsReceived.label("numValue"),
        literal(tally_sheet_template_ce_201_number_of_ballots_received.templateRowId).label("templateRowId")
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersionRow_CE_201.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).all()

    existing_tally_sheet_version_rows += session.query(
        _TallySheetVersionRow_CE_201.tallySheetVersionId,
        _Submission.electionId,
        _TallySheetVersionRow_CE_201.areaId.label("areaId"),
        _TallySheetVersionRow_CE_201.ballotsSpoilt.label("numValue"),
        literal(tally_sheet_template_ce_201_number_of_ballots_spoilt.templateRowId).label("templateRowId")
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersionRow_CE_201.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).all()

    existing_tally_sheet_version_rows += session.query(
        _TallySheetVersionRow_CE_201.tallySheetVersionId,
        _Submission.electionId,
        _TallySheetVersionRow_CE_201.areaId.label("areaId"),
        _TallySheetVersionRow_CE_201.ballotsIssued.label("numValue"),
        literal(tally_sheet_template_ce_201_number_of_ballots_issued.templateRowId).label("templateRowId")
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersionRow_CE_201.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).all()

    existing_tally_sheet_version_rows += session.query(
        _TallySheetVersionRow_CE_201.tallySheetVersionId,
        _Submission.electionId,
        _TallySheetVersionRow_CE_201.areaId.label("areaId"),
        _TallySheetVersionRow_CE_201.ballotsUnused.label("numValue"),
        literal(tally_sheet_template_ce_201_number_of_ballots_unused.templateRowId).label("templateRowId")
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersionRow_CE_201.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).all()

    existing_tally_sheet_version_rows += session.query(
        _TallySheetVersionRow_CE_201.tallySheetVersionId,
        _Submission.electionId,
        _TallySheetVersionRow_CE_201.areaId.label("areaId"),
        _TallySheetVersionRow_CE_201.ordinaryBallotCountFromBallotPaperAccount.label("numValue"),
        literal(
            tally_sheet_template_ce_201_number_of_ordinary_ballots_in_ballot_paper_account.templateRowId
        ).label("templateRowId")
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersionRow_CE_201.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).all()

    existing_tally_sheet_version_rows += session.query(
        _TallySheetVersionRow_CE_201.tallySheetVersionId,
        _Submission.electionId,
        _TallySheetVersionRow_CE_201.areaId.label("areaId"),
        _TallySheetVersionRow_CE_201.ordinaryBallotCountFromBoxCount.label("numValue"),
        literal(
            tally_sheet_template_ce_201_number_of_ordinary_ballots_in_ballot_box.templateRowId
        ).label("templateRowId")
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersionRow_CE_201.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).all()

    existing_tally_sheet_version_rows += session.query(
        _TallySheetVersionRow_CE_201.tallySheetVersionId,
        _Submission.electionId,
        _TallySheetVersionRow_CE_201.areaId.label("areaId"),
        _TallySheetVersionRow_CE_201.tenderedBallotCountFromBallotPaperAccount.label("numValue"),
        literal(
            tally_sheet_template_ce_201_number_of_tendered_ballots_in_ballot_paper_account.templateRowId
        ).label("templateRowId")
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersionRow_CE_201.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).all()

    existing_tally_sheet_version_rows += session.query(
        _TallySheetVersionRow_CE_201.tallySheetVersionId,
        _Submission.electionId,
        _TallySheetVersionRow_CE_201.areaId.label("areaId"),
        _TallySheetVersionRow_CE_201.tenderedBallotCountFromBoxCount.label("numValue"),
        literal(
            tally_sheet_template_ce_201_number_of_tendered_ballots_in_ballot_box.templateRowId
        ).label("templateRowId")
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersionRow_CE_201.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).all()

    session.commit()

    save_existing_tally_sheet_version_rows(existing_tally_sheet_version_rows, label="CE-201")

    # END ###########################################################################################################

    #################################################################################################################
    # PRE 41 rows
    #################################################################################################################
    class _TallySheetVersionRow_PRE_41(Base):
        __tablename__ = 'tallySheetVersionRow_PRE_41'
        tallySheetVersionRowId = db.Column(db.Integer, primary_key=True)
        tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheetVersion.tallySheetVersionId"),
                                        nullable=False)
        candidateId = db.Column(db.Integer, nullable=False)
        count = db.Column(db.Integer, nullable=False)
        countInWords = db.Column(db.String(1000), nullable=True)

    tally_sheet_template_pre_41 = _Template(
        templateName="PRE-41"
    )
    tally_sheet_template_pre_41_candidate_wise_first_preference_row = tally_sheet_template_pre_41.add_row(
        templateRowType="CANDIDATE_FIRST_PREFERENCE",
        hasMany=True,
        isDerived=False,
        columns=[
            {"columnName": "electionId", "grouped": False, "func": None},
            {"columnName": "areaId", "grouped": False, "func": None},
            {"columnName": "partyId", "grouped": False, "func": None},
            {"columnName": "candidateId", "grouped": False, "func": None},
            {"columnName": "numValue", "grouped": False, "func": None},
            {"columnName": "strValue", "grouped": False, "func": None}
        ]
    )
    tally_sheet_template_pre_41_rejected_vote_row = tally_sheet_template_pre_41.add_row(
        templateRowType="REJECTED_VOTE",
        hasMany=False,
        isDerived=False,
        columns=[
            {"columnName": "electionId", "grouped": False, "func": None},
            {"columnName": "areaId", "grouped": False, "func": None},
            {"columnName": "numValue", "grouped": False, "func": None}
        ]
    )

    existing_tally_sheets = session.query(
        _TallySheet
    ).filter(
        _TallySheet.tallySheetCode == "PRE_41"
    ).all()

    for existing_tally_sheet in existing_tally_sheets:
        existing_tally_sheet.templateId = tally_sheet_template_pre_41.templateId

    existing_tally_sheet_version_rows = session.query(
        _TallySheetVersionRow_PRE_41.tallySheetVersionId,
        _Submission.electionId,
        _Submission.areaId,
        _ElectionCandidate.partyId,
        _TallySheetVersionRow_PRE_41.candidateId,
        _TallySheetVersionRow_PRE_41.count.label("numValue"),
        _TallySheetVersionRow_PRE_41.countInWords.label("strValue"),
        literal(tally_sheet_template_pre_41_candidate_wise_first_preference_row.templateRowId).label("templateRowId")
    ).join(
        _TallySheetVersion,
        _TallySheetVersion.tallySheetVersionId == _TallySheetVersionRow_PRE_41.tallySheetVersionId
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersion.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).join(
        _ElectionCandidate,
        _ElectionCandidate.candidateId == _TallySheetVersionRow_PRE_41.candidateId
    ).all()

    existing_tally_sheet_version_rows += session.query(
        _TallySheetVersionRow_RejectedVoteCount.tallySheetVersionId,
        _Submission.electionId,
        _Submission.areaId,
        _TallySheetVersionRow_RejectedVoteCount.rejectedVoteCount.label("numValue"),
        literal(tally_sheet_template_pre_41_rejected_vote_row.templateRowId).label("templateRowId")
    ).join(
        _TallySheetVersion,
        _TallySheetVersion.tallySheetVersionId == _TallySheetVersionRow_RejectedVoteCount.tallySheetVersionId
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersion.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).join(
        _TallySheet,
        _TallySheet.tallySheetId == _Submission.submissionId
    ).filter(
        _TallySheet.templateId == tally_sheet_template_pre_41.templateId
    ).all()

    session.commit()

    save_existing_tally_sheet_version_rows(existing_tally_sheet_version_rows, label="PRE-41")

    # END ###########################################################################################################

    #################################################################################################################
    # PRE 30 PD rows
    #################################################################################################################
    class _TallySheetVersionRow_PRE_30_PD(Base):
        __tablename__ = 'tallySheetVersionRow_PRE_30_PD'
        tallySheetVersionRowId = db.Column(db.Integer, primary_key=True)
        tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheetVersion.tallySheetVersionId"),
                                        nullable=False)
        candidateId = db.Column(db.Integer, nullable=False)
        countingCentreId = db.Column(db.Integer, nullable=False)
        count = db.Column(db.Integer, nullable=False)

    tally_sheet_template_pre_30_pd = _Template(
        templateName="PRE-30-PD"
    )
    tally_sheet_template_pre_30_pd_candidate_wise_first_preference_row = tally_sheet_template_pre_30_pd.add_row(
        templateRowType="CANDIDATE_FIRST_PREFERENCE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "partyId", "grouped": True, "func": None},
            {"columnName": "candidateId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_41_candidate_wise_first_preference_row)
    tally_sheet_template_pre_30_pd_rejected_vote_row = tally_sheet_template_pre_30_pd.add_row(
        templateRowType="REJECTED_VOTE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_41_rejected_vote_row)

    existing_tally_sheets = session.query(
        _TallySheet
    ).filter(
        _TallySheet.tallySheetCode == "PRE_30_PD"
    ).all()

    for existing_tally_sheet in existing_tally_sheets:
        existing_tally_sheet.templateId = tally_sheet_template_pre_30_pd.templateId

    existing_tally_sheet_version_rows = session.query(
        _TallySheetVersionRow_PRE_30_PD.tallySheetVersionId,
        _Submission.electionId,
        _TallySheetVersionRow_PRE_30_PD.countingCentreId.label("areaId"),
        _ElectionCandidate.partyId,
        _TallySheetVersionRow_PRE_30_PD.candidateId,
        _TallySheetVersionRow_PRE_30_PD.count.label("numValue"),
        literal(tally_sheet_template_pre_30_pd_candidate_wise_first_preference_row.templateRowId).label("templateRowId")
    ).join(
        _TallySheetVersion,
        _TallySheetVersion.tallySheetVersionId == _TallySheetVersionRow_PRE_30_PD.tallySheetVersionId
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersion.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).join(
        _ElectionCandidate,
        _ElectionCandidate.candidateId == _TallySheetVersionRow_PRE_30_PD.candidateId
    ).all()

    existing_tally_sheet_version_rows += session.query(
        _TallySheetVersionRow_RejectedVoteCount.tallySheetVersionId,
        _Submission.electionId,
        _TallySheetVersionRow_RejectedVoteCount.areaId,
        _TallySheetVersionRow_RejectedVoteCount.rejectedVoteCount.label("numValue"),
        literal(tally_sheet_template_pre_30_pd_rejected_vote_row.templateRowId).label("templateRowId")
    ).join(
        _TallySheetVersion,
        _TallySheetVersion.tallySheetVersionId == _TallySheetVersionRow_RejectedVoteCount.tallySheetVersionId
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersion.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).join(
        _TallySheet,
        _TallySheet.tallySheetId == _Submission.submissionId
    ).filter(
        _TallySheet.templateId == tally_sheet_template_pre_30_pd.templateId
    ).all()

    session.commit()

    save_existing_tally_sheet_version_rows(existing_tally_sheet_version_rows, label="PRE-30-PD")

    # END ###########################################################################################################

    #################################################################################################################
    # PRE 30 ED rows
    #################################################################################################################
    class _TallySheetVersionRow_PRE_30_ED(Base):
        __tablename__ = 'tallySheetVersionRow_PRE_30_ED'
        tallySheetVersionRowId = db.Column(db.Integer, primary_key=True)
        tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheetVersion.tallySheetVersionId"),
                                        nullable=False)
        electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=False)
        areaId = db.Column(db.Integer, nullable=True)
        candidateId = db.Column(db.Integer, nullable=False)
        countingCentreId = db.Column(db.Integer, nullable=False)
        count = db.Column(db.Integer, nullable=False)

    tally_sheet_template_pre_30_ed = _Template(
        templateName="PRE-30-ED"
    )
    tally_sheet_template_pre_30_ed_candidate_wise_first_preference_row = tally_sheet_template_pre_30_ed.add_row(
        templateRowType="CANDIDATE_FIRST_PREFERENCE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "partyId", "grouped": True, "func": None},
            {"columnName": "candidateId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_30_pd_candidate_wise_first_preference_row)
    tally_sheet_template_pre_30_ed_rejected_vote_row = tally_sheet_template_pre_30_ed.add_row(
        templateRowType="REJECTED_VOTE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_30_pd_rejected_vote_row)

    existing_tally_sheets = session.query(
        _TallySheet
    ).filter(
        _TallySheet.tallySheetCode == "PRE_30_ED"
    ).all()

    for existing_tally_sheet in existing_tally_sheets:
        existing_tally_sheet.templateId = tally_sheet_template_pre_30_ed.templateId

    existing_tally_sheet_version_rows = session.query(
        _TallySheetVersionRow_PRE_30_ED.tallySheetVersionId,
        _TallySheetVersionRow_PRE_30_ED.electionId,
        _TallySheetVersionRow_PRE_30_ED.areaId.label("areaId"),
        _ElectionCandidate.partyId,
        _TallySheetVersionRow_PRE_30_ED.candidateId,
        _TallySheetVersionRow_PRE_30_ED.count.label("numValue"),
        literal(tally_sheet_template_pre_30_ed_candidate_wise_first_preference_row.templateRowId).label("templateRowId")
    ).join(
        _TallySheetVersion,
        _TallySheetVersion.tallySheetVersionId == _TallySheetVersionRow_PRE_30_ED.tallySheetVersionId
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersion.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).join(
        _ElectionCandidate,
        _ElectionCandidate.candidateId == _TallySheetVersionRow_PRE_30_ED.candidateId
    ).all()

    existing_tally_sheet_version_rows += session.query(
        _TallySheetVersionRow_RejectedVoteCount.tallySheetVersionId,
        _TallySheetVersionRow_RejectedVoteCount.electionId,
        _TallySheetVersionRow_RejectedVoteCount.areaId,
        _TallySheetVersionRow_RejectedVoteCount.rejectedVoteCount.label("numValue"),
        literal(tally_sheet_template_pre_30_ed_rejected_vote_row.templateRowId).label("templateRowId")
    ).join(
        _TallySheetVersion,
        _TallySheetVersion.tallySheetVersionId == _TallySheetVersionRow_RejectedVoteCount.tallySheetVersionId
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersion.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).join(
        _TallySheet,
        _TallySheet.tallySheetId == _Submission.submissionId
    ).filter(
        _TallySheet.templateId == tally_sheet_template_pre_30_ed.templateId
    ).all()

    session.commit()

    save_existing_tally_sheet_version_rows(existing_tally_sheet_version_rows, label="PRE-30-ED")

    # END ###########################################################################################################

    #################################################################################################################
    # PRE All Island ED rows
    #################################################################################################################
    class _TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS(Base):
        __tablename__ = 'tallySheetVersionRow_ALL_ISLAND_RESULTS_BY_ED'
        tallySheetVersionRowId = db.Column(db.Integer, primary_key=True)
        tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheetVersion.tallySheetVersionId"),
                                        nullable=False)
        electoralDistrictId = db.Column(db.Integer, nullable=True)
        candidateId = db.Column(db.Integer, nullable=False)
        count = db.Column(db.Integer, nullable=False)

    tally_sheet_template_pre_all_island_ed = _Template(
        templateName="PRE-ALL-ISLAND-RESULTS-BY-ELECTORAL-DISTRICTS"
    )
    tally_sheet_template_pre_all_island_ed_candidate_wise_first_preference_row = tally_sheet_template_pre_all_island_ed.add_row(
        templateRowType="CANDIDATE_FIRST_PREFERENCE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "partyId", "grouped": True, "func": None},
            {"columnName": "candidateId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_30_ed_candidate_wise_first_preference_row)
    tally_sheet_template_pre_all_island_ed_rejected_vote_row = tally_sheet_template_pre_all_island_ed.add_row(
        templateRowType="REJECTED_VOTE",
        hasMany=False,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_30_ed_rejected_vote_row)

    existing_tally_sheets = session.query(
        _TallySheet
    ).filter(
        _TallySheet.tallySheetCode == "PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS"
    ).all()

    for existing_tally_sheet in existing_tally_sheets:
        existing_tally_sheet.templateId = tally_sheet_template_pre_all_island_ed.templateId

    existing_tally_sheet_version_rows = session.query(
        _TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.tallySheetVersionId,
        _Submission.electionId,
        _TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.electoralDistrictId.label("areaId"),
        _ElectionCandidate.partyId,
        _TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.candidateId,
        _TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.count.label("numValue"),
        literal(tally_sheet_template_pre_all_island_ed_candidate_wise_first_preference_row.templateRowId).label(
            "templateRowId")
    ).join(
        _TallySheetVersion,
        _TallySheetVersion.tallySheetVersionId == _TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.tallySheetVersionId
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersion.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).join(
        _ElectionCandidate,
        _ElectionCandidate.candidateId == _TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.candidateId
    ).all()

    existing_tally_sheet_version_rows += session.query(
        _TallySheetVersionRow_RejectedVoteCount.tallySheetVersionId,
        _TallySheetVersionRow_RejectedVoteCount.electionId,
        _TallySheetVersionRow_RejectedVoteCount.areaId,
        _TallySheetVersionRow_RejectedVoteCount.rejectedVoteCount.label("numValue"),
        literal(tally_sheet_template_pre_all_island_ed_rejected_vote_row.templateRowId).label("templateRowId")
    ).join(
        _TallySheetVersion,
        _TallySheetVersion.tallySheetVersionId == _TallySheetVersionRow_RejectedVoteCount.tallySheetVersionId
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersion.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).join(
        _TallySheet,
        _TallySheet.tallySheetId == _Submission.submissionId
    ).filter(
        _TallySheet.templateId == tally_sheet_template_pre_all_island_ed.templateId
    ).all()

    session.commit()

    save_existing_tally_sheet_version_rows(existing_tally_sheet_version_rows, label="PRE-AI-ED")

    # END ###########################################################################################################

    #################################################################################################################
    # PRE All Island rows
    #################################################################################################################
    class _TallySheetVersionRow_ALL_ISLAND_RESULT(Base):
        __tablename__ = 'tallySheetVersionRow_ALL_ISLAND_RESULT'
        tallySheetVersionRowId = db.Column(db.Integer, primary_key=True)
        tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheetVersion.tallySheetVersionId"),
                                        nullable=False)
        candidateId = db.Column(db.Integer, nullable=False)
        count = db.Column(db.Integer, nullable=False)

    tally_sheet_template_pre_all_island = _Template(
        templateName="PRE-ALL-ISLAND-RESULTS"
    )
    tally_sheet_template_pre_all_island_candidate_wise_first_preference_row = tally_sheet_template_pre_all_island.add_row(
        templateRowType="CANDIDATE_FIRST_PREFERENCE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "partyId", "grouped": True, "func": None},
            {"columnName": "candidateId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_all_island_ed_candidate_wise_first_preference_row)
    tally_sheet_template_pre_all_island_rejected_vote_row = tally_sheet_template_pre_all_island.add_row(
        templateRowType="REJECTED_VOTE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_all_island_ed_rejected_vote_row)

    existing_tally_sheets = session.query(
        _TallySheet
    ).filter(
        _TallySheet.tallySheetCode == "PRE_ALL_ISLAND_RESULTS"
    ).all()

    for existing_tally_sheet in existing_tally_sheets:
        existing_tally_sheet.templateId = tally_sheet_template_pre_all_island.templateId

    existing_tally_sheet_version_rows = session.query(
        _TallySheetVersionRow_ALL_ISLAND_RESULT.tallySheetVersionId,
        _Submission.electionId,
        _Submission.areaId.label("areaId"),
        _ElectionCandidate.partyId,
        _TallySheetVersionRow_ALL_ISLAND_RESULT.candidateId,
        _TallySheetVersionRow_ALL_ISLAND_RESULT.count.label("numValue"),
        literal(tally_sheet_template_pre_all_island_candidate_wise_first_preference_row.templateRowId).label(
            "templateRowId")
    ).join(
        _TallySheetVersion,
        _TallySheetVersion.tallySheetVersionId == _TallySheetVersionRow_ALL_ISLAND_RESULT.tallySheetVersionId
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersion.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).join(
        _ElectionCandidate,
        _ElectionCandidate.candidateId == _TallySheetVersionRow_ALL_ISLAND_RESULT.candidateId
    ).all()

    existing_tally_sheet_version_rows += session.query(
        _TallySheetVersionRow_RejectedVoteCount.tallySheetVersionId,
        _TallySheetVersionRow_RejectedVoteCount.electionId,
        _TallySheetVersionRow_RejectedVoteCount.areaId,
        _TallySheetVersionRow_RejectedVoteCount.rejectedVoteCount.label("numValue"),
        literal(tally_sheet_template_pre_all_island_rejected_vote_row.templateRowId).label("templateRowId")
    ).join(
        _TallySheetVersion,
        _TallySheetVersion.tallySheetVersionId == _TallySheetVersionRow_RejectedVoteCount.tallySheetVersionId
    ).join(
        _SubmissionVersion,
        _SubmissionVersion.submissionVersionId == _TallySheetVersion.tallySheetVersionId
    ).join(
        _Submission,
        _Submission.submissionId == _SubmissionVersion.submissionId
    ).join(
        _TallySheet,
        _TallySheet.tallySheetId == _Submission.submissionId
    ).filter(
        _TallySheet.templateId == tally_sheet_template_pre_all_island.templateId
    ).all()

    session.commit()

    save_existing_tally_sheet_version_rows(existing_tally_sheet_version_rows, label="PRE-AI")

    # END ###########################################################################################################

    #################################################################################################################
    # PRE 34 CO
    #################################################################################################################
    class TallySheetVersionRow_PRE_34_preference_Model(Base):
        __tablename__ = 'tallySheetVersionRow_PRE_34_Preference'
        tallySheetVersionRowId = db.Column(db.Integer, primary_key=True)
        tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheetVersion.tallySheetVersionId"),
                                        nullable=False)
        electionId = db.Column(db.Integer, nullable=False)
        candidateId = db.Column(db.Integer, nullable=True)
        areaId = db.Column(db.Integer, nullable=True)
        preferenceNumber = db.Column(db.Integer, nullable=False)
        preferenceCount = db.Column(db.Integer, nullable=False)

    tally_sheet_template_pre_34_co = _Template(
        templateName=PRE_34_CO
    )
    tally_sheet_template_pre_34_co_candidate_wise_second_preference_row = tally_sheet_template_pre_34_co.add_row(
        templateRowType="CANDIDATE_SECOND_PREFERENCE",
        hasMany=True,
        isDerived=False,
        columns=[
            {"columnName": "electionId", "grouped": False, "func": None},
            {"columnName": "areaId", "grouped": False, "func": None},
            {"columnName": "partyId", "grouped": False, "func": None},
            {"columnName": "candidateId", "grouped": False, "func": None},
            {"columnName": "numValue", "grouped": False, "func": None}
        ]
    )
    tally_sheet_template_pre_34_co_candidate_wise_third_preference_row = tally_sheet_template_pre_34_co.add_row(
        templateRowType="CANDIDATE_THIRD_PREFERENCE",
        hasMany=True,
        isDerived=False,
        columns=[
            {"columnName": "electionId", "grouped": False, "func": None},
            {"columnName": "areaId", "grouped": False, "func": None},
            {"columnName": "partyId", "grouped": False, "func": None},
            {"columnName": "candidateId", "grouped": False, "func": None},
            {"columnName": "numValue", "grouped": False, "func": None}
        ]
    )

    existing_tally_sheets = session.query(
        _TallySheet
    ).filter(
        _TallySheet.tallySheetCode == "PRE_34_CO"
    ).all()

    for existing_tally_sheet in existing_tally_sheets:
        existing_tally_sheet.templateId = tally_sheet_template_pre_34_co.templateId

    session.commit()

    # END ###########################################################################################################

    #################################################################################################################
    # PRE 34 I RO
    #################################################################################################################

    tally_sheet_template_pre_34_i_ro = _Template(
        templateName=PRE_34_I_RO
    )
    tally_sheet_template_pre_34_i_ro_candidate_wise_second_preference_row = tally_sheet_template_pre_34_i_ro.add_row(
        templateRowType="CANDIDATE_SECOND_PREFERENCE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "partyId", "grouped": True, "func": None},
            {"columnName": "candidateId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_34_co_candidate_wise_second_preference_row)
    tally_sheet_template_pre_34_i_ro_candidate_wise_third_preference_row = tally_sheet_template_pre_34_i_ro.add_row(
        templateRowType="CANDIDATE_THIRD_PREFERENCE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "partyId", "grouped": True, "func": None},
            {"columnName": "candidateId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_34_co_candidate_wise_third_preference_row)

    existing_tally_sheets = session.query(
        _TallySheet
    ).filter(
        _TallySheet.tallySheetCode == "PRE_34_I_RO"
    ).all()

    for existing_tally_sheet in existing_tally_sheets:
        existing_tally_sheet.templateId = tally_sheet_template_pre_34_i_ro.templateId

    session.commit()

    # END ###########################################################################################################

    #################################################################################################################
    # PRE 34 II RO
    #################################################################################################################
    tally_sheet_template_pre_34_ii_ro = _Template(
        templateName=PRE_34_II_RO
    )
    tally_sheet_template_pre_34_ii_ro_candidate_wise_second_preference_row = tally_sheet_template_pre_34_ii_ro.add_row(
        templateRowType="CANDIDATE_SECOND_PREFERENCE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "partyId", "grouped": True, "func": None},
            {"columnName": "candidateId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_34_i_ro_candidate_wise_second_preference_row)
    tally_sheet_template_pre_34_ii_ro_candidate_wise_third_preference_row = tally_sheet_template_pre_34_ii_ro.add_row(
        templateRowType="CANDIDATE_THIRD_PREFERENCE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "partyId", "grouped": True, "func": None},
            {"columnName": "candidateId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_34_i_ro_candidate_wise_third_preference_row)

    existing_tally_sheets = session.query(
        _TallySheet
    ).filter(
        _TallySheet.tallySheetCode == "PRE_34_II_RO"
    ).all()

    for existing_tally_sheet in existing_tally_sheets:
        existing_tally_sheet.templateId = tally_sheet_template_pre_34_ii_ro.templateId

    session.commit()

    # END ###########################################################################################################

    #################################################################################################################
    # PRE 34
    #################################################################################################################

    tally_sheet_template_pre_34 = _Template(
        templateName=PRE_34
    )
    tally_sheet_template_pre_34_candidate_wise_second_preference_row = tally_sheet_template_pre_34.add_row(
        templateRowType="CANDIDATE_SECOND_PREFERENCE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "partyId", "grouped": True, "func": None},
            {"columnName": "candidateId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_34_ii_ro_candidate_wise_second_preference_row)
    tally_sheet_template_pre_34_candidate_wise_second_preference_row = tally_sheet_template_pre_34.add_row(
        templateRowType="CANDIDATE_THIRD_PREFERENCE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "partyId", "grouped": True, "func": None},
            {"columnName": "candidateId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_34_ii_ro_candidate_wise_third_preference_row)

    existing_tally_sheets = session.query(
        _TallySheet
    ).filter(
        _TallySheet.tallySheetCode == "PRE_34"
    ).all()

    for existing_tally_sheet in existing_tally_sheets:
        existing_tally_sheet.templateId = tally_sheet_template_pre_34.templateId

    session.commit()

    # END ###########################################################################################################

    #################################################################################################################
    # PRE 34 PD
    #################################################################################################################
    tally_sheet_template_pre_34_pd = _Template(
        templateName=PRE_34_PD
    )
    tally_sheet_template_pre_34_pd_candidate_wise_first_preference_row = tally_sheet_template_pre_34_pd.add_row(
        templateRowType="CANDIDATE_FIRST_PREFERENCE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "partyId", "grouped": True, "func": None},
            {"columnName": "candidateId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_30_pd_candidate_wise_first_preference_row)
    tally_sheet_template_pre_34_pd_candidate_wise_second_preference_row = tally_sheet_template_pre_34_pd.add_row(
        templateRowType="CANDIDATE_SECOND_PREFERENCE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "partyId", "grouped": True, "func": None},
            {"columnName": "candidateId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_34_i_ro_candidate_wise_second_preference_row)
    tally_sheet_template_pre_34_pd_candidate_wise_third_preference_row = tally_sheet_template_pre_34_pd.add_row(
        templateRowType="CANDIDATE_THIRD_PREFERENCE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "partyId", "grouped": True, "func": None},
            {"columnName": "candidateId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_34_i_ro_candidate_wise_third_preference_row)

    existing_tally_sheets = session.query(
        _TallySheet
    ).filter(
        _TallySheet.tallySheetCode == "PRE_34_PD"
    ).all()

    for existing_tally_sheet in existing_tally_sheets:
        existing_tally_sheet.templateId = tally_sheet_template_pre_34_pd.templateId

    session.commit()

    # END ###########################################################################################################

    #################################################################################################################
    # PRE 34 ED
    #################################################################################################################

    tally_sheet_template_pre_34_ed = _Template(
        templateName=PRE_34_ED
    )
    tally_sheet_template_pre_34_ed_candidate_wise_first_preference_row = tally_sheet_template_pre_34_ed.add_row(
        templateRowType="CANDIDATE_FIRST_PREFERENCE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "partyId", "grouped": True, "func": None},
            {"columnName": "candidateId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_34_pd_candidate_wise_first_preference_row)
    tally_sheet_template_pre_34_ed_candidate_wise_second_preference_row = tally_sheet_template_pre_34_ed.add_row(
        templateRowType="CANDIDATE_SECOND_PREFERENCE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "partyId", "grouped": True, "func": None},
            {"columnName": "candidateId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_34_pd_candidate_wise_second_preference_row)
    tally_sheet_template_pre_34_ed_candidate_wise_third_preference_row = tally_sheet_template_pre_34_ed.add_row(
        templateRowType="CANDIDATE_THIRD_PREFERENCE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "partyId", "grouped": True, "func": None},
            {"columnName": "candidateId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_34_pd_candidate_wise_third_preference_row)

    existing_tally_sheets = session.query(
        _TallySheet
    ).filter(
        _TallySheet.tallySheetCode == "PRE_34_ED"
    ).all()

    for existing_tally_sheet in existing_tally_sheets:
        existing_tally_sheet.templateId = tally_sheet_template_pre_34_ed.templateId

    session.commit()

    # END ###########################################################################################################

    #################################################################################################################
    # PRE 34 AI
    #################################################################################################################

    tally_sheet_template_pre_34_ai = _Template(
        templateName=PRE_34_AI
    )
    tally_sheet_template_pre_34_ai_candidate_wise_first_preference_row = tally_sheet_template_pre_34_ai.add_row(
        templateRowType="CANDIDATE_FIRST_PREFERENCE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "partyId", "grouped": True, "func": None},
            {"columnName": "candidateId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_34_ed_candidate_wise_first_preference_row)
    tally_sheet_template_pre_34_ai_candidate_wise_second_preference_row = tally_sheet_template_pre_34_ai.add_row(
        templateRowType="CANDIDATE_SECOND_PREFERENCE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "partyId", "grouped": True, "func": None},
            {"columnName": "candidateId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_34_ed_candidate_wise_second_preference_row)
    tally_sheet_template_pre_34_ai_candidate_wise_third_preference_row = tally_sheet_template_pre_34_ai.add_row(
        templateRowType="CANDIDATE_THIRD_PREFERENCE",
        hasMany=True,
        isDerived=True,
        columns=[
            {"columnName": "electionId", "grouped": True, "func": None},
            {"columnName": "areaId", "grouped": True, "func": None},
            {"columnName": "partyId", "grouped": True, "func": None},
            {"columnName": "candidateId", "grouped": True, "func": None},
            {"columnName": "numValue", "grouped": False, "func": "sum"}
        ]
    ).add_derivative_template_row(tally_sheet_template_pre_34_ed_candidate_wise_third_preference_row)

    existing_tally_sheets = session.query(
        _TallySheet
    ).filter(
        _TallySheet.tallySheetCode == "PRE_34_AI"
    ).all()

    for existing_tally_sheet in existing_tally_sheets:
        existing_tally_sheet.templateId = tally_sheet_template_pre_34_ai.templateId

    session.commit()

    # END ###########################################################################################################

    op.alter_column(
        'election', 'electionTemplateName',
        existing_type=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=100),
        nullable=False)
    op.alter_column(
        'tallySheet', 'templateId',
        existing_type=mysql.INTEGER(display_width=11),
        nullable=False)
    op.create_foreign_key('tally_sheet_fk_template_id', 'tallySheet', 'template', ['templateId'], ['templateId'])

    op.drop_table('tallySheetVersionRow_PRE_41')
    op.drop_table('tallySheetVersionRow_PRE_34_summary')
    op.drop_table('tallySheetVersionRow_PRE_30_PD')
    op.drop_table('tallySheetVersionRow_PRE_21')
    op.drop_table('tallySheetVersionRow_PRE_34_Preference')
    op.drop_table('tallySheetVersionRow_CE_201_PV_CC')
    op.drop_table('tallySheetVersionRow_PRE_30_ED')
    op.drop_table('tallySheetVersionRow_CE_201_ballotBox')
    op.drop_table('tallySheetVersionRow_CE_201_PV')
    op.drop_table('tallySheetVersionRow_RejectedVoteCount')
    op.drop_table('tallySheetVersionRow_ALL_ISLAND_RESULT')
    op.drop_table('tallySheetVersionRow_ALL_ISLAND_RESULTS_BY_ED')
    op.drop_table('tallySheetVersionRow_CE_201')
    op.drop_column('tallySheet', 'tallySheetCode')
    op.drop_column('tallySheetVersion', 'tallySheetVersionCode')


def downgrade():
    op.add_column(
        'tallySheetVersion', sa.Column(
            'tallySheetVersionCode',
            mysql.ENUM('CE_201', 'CE_201_PV', 'PRE_28', 'PRE_41', 'PRE_30_PD',
                       'PRE_30_PD_PV', 'PRE_30_ED', 'PRE_21', 'PRE_34_CO',
                       'PRE_34_I_RO', 'PRE_34_II_RO', 'PRE_34',
                       'PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS',
                       'PRE_ALL_ISLAND_RESULTS', 'PRE_34_PD', 'PRE_34_ED',
                       'PRE_34_AI', collation='utf8mb4_unicode_ci'),
            nullable=False))
    op.add_column(
        'tallySheet', sa.Column(
            'tallySheetCode',
            mysql.ENUM(
                'CE_201', 'CE_201_PV', 'PRE_28', 'PRE_41', 'PRE_30_PD',
                'PRE_30_PD_PV', 'PRE_30_ED', 'PRE_21', 'PRE_34_CO', 'PRE_34_I_RO',
                'PRE_34_II_RO', 'PRE_34',
                'PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS',
                'PRE_ALL_ISLAND_RESULTS', 'PRE_34_PD', 'PRE_34_ED', 'PRE_34_AI',
                collation='utf8mb4_unicode_ci'), nullable=False))
    op.drop_constraint(None, 'tallySheet', type_='foreignkey')
    op.drop_column('tallySheet', 'templateId')
    op.alter_column(
        'election', 'voteType',
        existing_type=sa.String(length=100),
        type_=mysql.ENUM('Postal', 'NonPostal', 'PostalAndNonPostal', collation='utf8mb4_unicode_ci'),
        existing_nullable=False)
    op.alter_column(
        'election', 'isListed',
        existing_type=sa.Boolean(),
        type_=mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=100),
        existing_nullable=False)
    op.drop_column('election', 'electionTemplateName')
    op.alter_column(
        'area_map', 'voteType',
        existing_type=sa.String(length=100),
        type_=mysql.ENUM('Postal', 'NonPostal', 'PostalAndNonPostal', collation='utf8mb4_unicode_ci'),
        nullable=True)
    op.create_table(
        'tallySheetVersionRow_CE_201',
        sa.Column('tallySheetVersionRowId', mysql.INTEGER(display_width=11), nullable=False),
        sa.Column('tallySheetVersionId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.Column('areaId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('ballotsIssued', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('ballotsReceived', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('ballotsSpoilt', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('ballotsUnused', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('ordinaryBallotCountFromBallotPaperAccount', mysql.INTEGER(display_width=11),
                  autoincrement=False, nullable=False),
        sa.Column('ordinaryBallotCountFromBoxCount', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.Column('tenderedBallotCountFromBallotPaperAccount', mysql.INTEGER(display_width=11),
                  autoincrement=False, nullable=False),
        sa.Column('tenderedBallotCountFromBoxCount', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.ForeignKeyConstraint(['areaId'], ['area.areaId'], name='tallySheetVersionRow_CE_201_ibfk_1'),
        sa.ForeignKeyConstraint(['tallySheetVersionId'], ['tallySheetVersion.tallySheetVersionId'],
                                name='tallySheetVersionRow_CE_201_ibfk_2'),
        sa.PrimaryKeyConstraint('tallySheetVersionRowId'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'tallySheetVersionRow_ALL_ISLAND_RESULTS_BY_ED',
        sa.Column('tallySheetVersionRowId', mysql.INTEGER(display_width=11), nullable=False),
        sa.Column('tallySheetVersionId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.Column('electoralDistrictId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.Column('candidateId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['candidateId'], ['candidate.candidateId'],
                                name='tallySheetVersionRow_ALL_ISLAND_RESULTS_BY_ED_ibfk_1'),
        sa.ForeignKeyConstraint(['electoralDistrictId'], ['area.areaId'],
                                name='tallySheetVersionRow_ALL_ISLAND_RESULTS_BY_ED_ibfk_2'),
        sa.ForeignKeyConstraint(['tallySheetVersionId'], ['tallySheetVersion.tallySheetVersionId'],
                                name='tallySheetVersionRow_ALL_ISLAND_RESULTS_BY_ED_ibfk_3'),
        sa.PrimaryKeyConstraint('tallySheetVersionRowId'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'tallySheetVersionRow_ALL_ISLAND_RESULT',
        sa.Column('tallySheetVersionRowId', mysql.INTEGER(display_width=11), nullable=False),
        sa.Column('tallySheetVersionId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.Column('candidateId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['candidateId'], ['candidate.candidateId'],
                                name='tallySheetVersionRow_ALL_ISLAND_RESULT_ibfk_1'),
        sa.ForeignKeyConstraint(['tallySheetVersionId'], ['tallySheetVersion.tallySheetVersionId'],
                                name='tallySheetVersionRow_ALL_ISLAND_RESULT_ibfk_2'),
        sa.PrimaryKeyConstraint('tallySheetVersionRowId'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'tallySheetVersionRow_RejectedVoteCount',
        sa.Column('tallySheetVersionRowId', mysql.INTEGER(display_width=11), nullable=False),
        sa.Column('tallySheetVersionId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.Column('electionId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('areaId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('candidateId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('rejectedVoteCount', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.ForeignKeyConstraint(['areaId'], ['area.areaId'],
                                name='tallySheetVersionRow_RejectedVoteCount_ibfk_1'),
        sa.ForeignKeyConstraint(['candidateId'], ['candidate.candidateId'],
                                name='tallySheetVersionRow_RejectedVoteCount_ibfk_2'),
        sa.ForeignKeyConstraint(['electionId'], ['election.electionId'],
                                name='tallySheetVersionRow_RejectedVoteCount_ibfk_3'),
        sa.ForeignKeyConstraint(['tallySheetVersionId'], ['tallySheetVersion.tallySheetVersionId'],
                                name='tallySheetVersionRow_RejectedVoteCount_ibfk_4'),
        sa.PrimaryKeyConstraint('tallySheetVersionRowId'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'tallySheetVersionRow_CE_201_PV',
        sa.Column('tallySheetVersionRowId', mysql.INTEGER(display_width=11), nullable=False),
        sa.Column('tallySheetVersionId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=True),
        sa.Column('ballotBoxId', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20), nullable=True),
        sa.Column('numberOfPacketsInserted', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=True),
        sa.Column('numberOfAPacketsFound', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=True),
        sa.ForeignKeyConstraint(['tallySheetVersionId'], ['tallySheetVersion.tallySheetVersionId'],
                                name='tallySheetVersionRow_CE_201_PV_ibfk_1'),
        sa.PrimaryKeyConstraint('tallySheetVersionRowId'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'tallySheetVersionRow_CE_201_ballotBox',
        sa.Column('tallySheetVersionRowId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.Column('ballotBoxId', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=100), nullable=False),
        sa.Column('invoiceStage', mysql.ENUM('Issued', 'Received', collation='utf8mb4_unicode_ci'),
                  nullable=False),
        sa.ForeignKeyConstraint(['tallySheetVersionRowId'],
                                ['tallySheetVersionRow_CE_201.tallySheetVersionRowId'],
                                name='tallySheetVersionRow_CE_201_ballotBox_ibfk_1'),
        sa.PrimaryKeyConstraint('tallySheetVersionRowId', 'ballotBoxId', 'invoiceStage'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'tallySheetVersionRow_PRE_30_ED',
        sa.Column('tallySheetVersionRowId', mysql.INTEGER(display_width=11), nullable=False),
        sa.Column('tallySheetVersionId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.Column('candidateId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('electionId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('areaId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['areaId'], ['area.areaId'], name='tallySheetVersionRow_PRE_30_ED_ibfk_1'),
        sa.ForeignKeyConstraint(['candidateId'], ['candidate.candidateId'],
                                name='tallySheetVersionRow_PRE_30_ED_ibfk_2'),
        sa.ForeignKeyConstraint(['electionId'], ['election.electionId'],
                                name='tallySheetVersionRow_PRE_30_ED_ibfk_3'),
        sa.ForeignKeyConstraint(['tallySheetVersionId'], ['tallySheetVersion.tallySheetVersionId'],
                                name='tallySheetVersionRow_PRE_30_ED_ibfk_4'),
        sa.PrimaryKeyConstraint('tallySheetVersionRowId'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'tallySheetVersionRow_CE_201_PV_CC',
        sa.Column('tallySheetVersionRowId', mysql.INTEGER(display_width=11), nullable=False),
        sa.Column('tallySheetVersionId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=True),
        sa.Column('countingCentreId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('situation', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=100), nullable=True),
        sa.Column('timeOfCommencementOfCount', mysql.DATETIME(), nullable=True),
        sa.Column('numberOfAPacketsFound', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=True),
        sa.Column('numberOfACoversRejected', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=True),
        sa.Column('numberOfBCoversRejected', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=True),
        sa.Column('numberOfValidBallotPapers', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=True),
        sa.ForeignKeyConstraint(['countingCentreId'], ['area.areaId'],
                                name='tallySheetVersionRow_CE_201_PV_CC_ibfk_1'),
        sa.ForeignKeyConstraint(['tallySheetVersionId'], ['tallySheetVersion.tallySheetVersionId'],
                                name='tallySheetVersionRow_CE_201_PV_CC_ibfk_2'),
        sa.PrimaryKeyConstraint('tallySheetVersionRowId'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'tallySheetVersionRow_PRE_34_Preference',
        sa.Column('tallySheetVersionRowId', mysql.INTEGER(display_width=11), nullable=False),
        sa.Column('tallySheetVersionId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.Column('electionId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('candidateId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('areaId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('preferenceNumber', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('preferenceCount', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['areaId'], ['area.areaId'],
                                name='tallySheetVersionRow_PRE_34_Preference_ibfk_1'),
        sa.ForeignKeyConstraint(['candidateId'], ['candidate.candidateId'],
                                name='tallySheetVersionRow_PRE_34_Preference_ibfk_2'),
        sa.ForeignKeyConstraint(['electionId'], ['election.electionId'],
                                name='tallySheetVersionRow_PRE_34_Preference_ibfk_3'),
        sa.ForeignKeyConstraint(['tallySheetVersionId'], ['tallySheetVersion.tallySheetVersionId'],
                                name='tallySheetVersionRow_PRE_34_Preference_ibfk_4'),
        sa.PrimaryKeyConstraint('tallySheetVersionRowId'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'tallySheetVersionRow_PRE_21',
        sa.Column('tallySheetVersionRowId', mysql.INTEGER(display_width=11), nullable=False),
        sa.Column('tallySheetVersionId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=True),
        sa.Column('count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('invalidVoteCategoryId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.ForeignKeyConstraint(['invalidVoteCategoryId'],
                                ['election_invalidVoteCategory.invalidVoteCategoryId'],
                                name='tallySheetVersionRow_PRE_21_ibfk_1'),
        sa.ForeignKeyConstraint(['tallySheetVersionId'], ['tallySheetVersion.tallySheetVersionId'],
                                name='tallySheetVersionRow_PRE_21_ibfk_2'),
        sa.PrimaryKeyConstraint('tallySheetVersionRowId'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'tallySheetVersionRow_PRE_30_PD',
        sa.Column('tallySheetVersionRowId', mysql.INTEGER(display_width=11), nullable=False),
        sa.Column('tallySheetVersionId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.Column('candidateId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('countingCentreId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['candidateId'], ['candidate.candidateId'],
                                name='tallySheetVersionRow_PRE_30_PD_ibfk_1'),
        sa.ForeignKeyConstraint(['countingCentreId'], ['area.areaId'],
                                name='tallySheetVersionRow_PRE_30_PD_ibfk_2'),
        sa.ForeignKeyConstraint(['tallySheetVersionId'], ['tallySheetVersion.tallySheetVersionId'],
                                name='tallySheetVersionRow_PRE_30_PD_ibfk_3'),
        sa.PrimaryKeyConstraint('tallySheetVersionRowId'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'tallySheetVersionRow_PRE_34_summary',
        sa.Column('tallySheetVersionRowId', mysql.INTEGER(display_width=11), nullable=False),
        sa.Column('tallySheetVersionId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.Column('electionId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('ballotPapersNotCounted', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.Column('remainingBallotPapers', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.ForeignKeyConstraint(['electionId'], ['election.electionId'],
                                name='tallySheetVersionRow_PRE_34_summary_ibfk_1'),
        sa.ForeignKeyConstraint(['tallySheetVersionId'], ['tallySheetVersion.tallySheetVersionId'],
                                name='tallySheetVersionRow_PRE_34_summary_ibfk_2'),
        sa.PrimaryKeyConstraint('tallySheetVersionRowId'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'tallySheetVersionRow_PRE_41',
        sa.Column('tallySheetVersionRowId', mysql.INTEGER(display_width=11), nullable=False),
        sa.Column('tallySheetVersionId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.Column('candidateId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('countInWords', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=1000),
                  nullable=True),
        sa.ForeignKeyConstraint(['candidateId'], ['candidate.candidateId'],
                                name='tallySheetVersionRow_PRE_41_ibfk_1'),
        sa.ForeignKeyConstraint(['tallySheetVersionId'], ['tallySheetVersion.tallySheetVersionId'],
                                name='tallySheetVersionRow_PRE_41_ibfk_2'),
        sa.PrimaryKeyConstraint('tallySheetVersionRowId', 'tallySheetVersionId', 'candidateId'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.drop_table('templateRow_derivativeTemplateRow')
    op.drop_table('templateRowColumn')
    op.drop_table('templateRow')
    op.drop_table('template')
    op.drop_table('tallySheet_tallySheet')
    op.drop_table('tallySheet_map')
    op.drop_table('tallySheetVersionRow')
