"""empty message

Revision ID: 5d7ed731c34a
Revises: 9cb6d7971778
Create Date: 2020-02-15 22:39:18.693398

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from tqdm import tqdm

# revision identifiers, used by Alembic.
revision = '5d7ed731c34a'
down_revision = '9cb6d7971778'
branch_labels = None
depends_on = None


def upgrade():
    Base = declarative_base()
    bind = op.get_bind()
    session = Session(bind=bind)

    class _TallySheet(Base):
        __tablename__ = 'tallySheet'
        tallySheetId = sa.Column(sa.Integer, primary_key=True)
        metaId = sa.Column(sa.Integer)

    class _Submission(Base):
        __tablename__ = 'submission'
        submissionId = sa.Column(sa.Integer, primary_key=True)
        areaId = sa.Column(sa.Integer)
        electionId = sa.Column(sa.Integer)

    class _Meta(Base):
        __tablename__ = 'meta'

        metaId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

        def __init__(self):
            super(_Meta, self).__init__()
            session.add(self)
            session.flush()

    class _MetaData(Base):
        __tablename__ = 'metaData'

        metaDataId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        metaId = sa.Column(sa.Integer)
        metaDataKey = sa.Column(sa.String(100), nullable=False)
        metaDataValue = sa.Column(sa.String(100), nullable=False)

        def __init__(self, metaId, metaDataKey, metaDataValue):
            super(_MetaData, self).__init__(metaId=metaId, metaDataKey=metaDataKey, metaDataValue=metaDataValue)
            session.add(self)
            session.flush()

    op.create_table(
        'meta',
        sa.Column('metaId', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('metaId')
    )
    op.create_table(
        'metaData',
        sa.Column('metaDataId', sa.Integer(), nullable=False),
        sa.Column('metaId', sa.Integer(), nullable=False),
        sa.Column('metaDataKey', sa.String(length=100), nullable=False),
        sa.Column('metaDataValue', sa.String(length=100), nullable=False),
        sa.ForeignKeyConstraint(['metaId'], ['meta.metaId'], ),
        sa.PrimaryKeyConstraint('metaDataId'),
        sa.UniqueConstraint('metaId', 'metaDataKey', name='MetaDataModelUK')
    )
    op.add_column('tallySheet', sa.Column('metaId', sa.Integer(), nullable=True))

    tally_sheets = session.query(
        _TallySheet
    ).all()

    print(" -- Adding a 'meta' with 'areaId' to each tally sheet.")
    for tally_sheet in tqdm(tally_sheets):
        submission = session.query(_Submission.areaId, _Submission.electionId).filter(
            _Submission.submissionId == tally_sheet.tallySheetId).one_or_none()
        meta = _Meta()
        _MetaData(metaId=meta.metaId, metaDataKey="areaId", metaDataValue=submission.areaId)
        _MetaData(metaId=meta.metaId, metaDataKey="electionId", metaDataValue=submission.electionId)
        tally_sheet.metaId = meta.metaId
        session.add(tally_sheet)

    session.commit()

    op.alter_column(
        'tallySheet', 'metaId',
        existing_type=mysql.INTEGER(display_width=11),
        nullable=False)
    op.create_foreign_key('tally_sheet_fk_meta_id', 'tallySheet', 'meta', ['metaId'], ['metaId'])


def downgrade():
    op.drop_constraint('tally_sheet_fk_meta_id', 'tallySheet', type_='foreignkey')
    op.drop_column('tallySheet', 'metaId')
    op.drop_table('metaData')
    op.drop_table('meta')
