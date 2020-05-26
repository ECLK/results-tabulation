"""empty message

Revision ID: b159e6f82036
Revises: a07d014866a1
Create Date: 2020-03-22 08:25:03.798304

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b159e6f82036'
down_revision = 'a07d014866a1'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_index('BallotPerElection', table_name='ballot')
    op.drop_table('ballotBox')
    op.drop_table('ballotBook')
    op.drop_table('ballot')
    op.drop_table('invoice_stationaryItem')
    op.drop_table('stationaryItem')
    op.drop_table('invoice')


def downgrade():
    op.create_table(
        'ballotBox',
        sa.Column('stationaryItemId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('ballotBoxId', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20), nullable=False),
        sa.Column('electionId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['electionId'], ['election.electionId'], name='ballotbox_ibfk_1'),
        sa.ForeignKeyConstraint(['stationaryItemId'], ['stationaryItem.stationaryItemId'],
                                name='ballotbox_ibfk_2'),
        sa.PrimaryKeyConstraint('stationaryItemId', 'ballotBoxId'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'invoice',
        sa.Column('invoiceId', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
        sa.Column('electionId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('issuingOfficeId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('receivingOfficeId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.Column('confirmed', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
        sa.Column('issuedBy', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('issuedTo', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('issuedAt', mysql.DATETIME(), nullable=False),
        sa.Column('delete', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['electionId'], ['election.electionId'], name='invoice_ibfk_1'),
        sa.ForeignKeyConstraint(['issuingOfficeId'], ['area.areaId'], name='invoice_ibfk_2'),
        sa.ForeignKeyConstraint(['receivingOfficeId'], ['area.areaId'], name='invoice_ibfk_3'),
        sa.PrimaryKeyConstraint('invoiceId'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'invoice_stationaryItem',
        sa.Column('invoiceId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('stationaryItemId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('received', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
        sa.Column('receivedBy', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('receivedFrom', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('receivedAt', mysql.DATETIME(), nullable=True),
        sa.Column('receivedOfficeId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.Column('receivedProofId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['invoiceId'], ['invoice.invoiceId'], name='invoice_stationaryitem_ibfk_1'),
        sa.ForeignKeyConstraint(['receivedOfficeId'], ['area.areaId'],
                                name='invoice_stationaryitem_ibfk_2'),
        sa.ForeignKeyConstraint(['receivedProofId'], ['proof.proofId'],
                                name='invoice_stationaryitem_ibfk_3'),
        sa.ForeignKeyConstraint(['stationaryItemId'], ['stationaryItem.stationaryItemId'],
                                name='invoice_stationaryitem_ibfk_4'),
        sa.PrimaryKeyConstraint('invoiceId', 'stationaryItemId'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'ballot',
        sa.Column('stationaryItemId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('ballotId', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=20), nullable=False),
        sa.Column('electionId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('ballotType', mysql.ENUM('Ordinary', 'Tendered', collation='utf8mb4_unicode_ci'),
                  nullable=False),
        sa.ForeignKeyConstraint(['electionId'], ['election.electionId'], name='ballot_ibfk_1'),
        sa.ForeignKeyConstraint(['stationaryItemId'], ['stationaryItem.stationaryItemId'],
                                name='ballot_ibfk_2'),
        sa.PrimaryKeyConstraint('stationaryItemId', 'ballotId'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.create_index('BallotPerElection', 'ballot', ['ballotId', 'electionId'], unique=True)
    op.create_table(
        'ballotBook',
        sa.Column('stationaryItemId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.Column('fromBallotStationaryItemId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.Column('toBallotStationaryItemId', mysql.INTEGER(display_width=11), autoincrement=False,
                  nullable=False),
        sa.ForeignKeyConstraint(['fromBallotStationaryItemId'], ['ballot.stationaryItemId'],
                                name='ballotbook_ibfk_1'),
        sa.ForeignKeyConstraint(['stationaryItemId'], ['stationaryItem.stationaryItemId'],
                                name='ballotbook_ibfk_2'),
        sa.ForeignKeyConstraint(['toBallotStationaryItemId'], ['ballot.stationaryItemId'],
                                name='ballotbook_ibfk_3'),
        sa.PrimaryKeyConstraint('stationaryItemId'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
    op.create_table(
        'stationaryItem',
        sa.Column('stationaryItemId', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
        sa.Column('stationaryItemType', mysql.ENUM('Ballot', 'BallotBox', collation='utf8mb4_unicode_ci'),
                  nullable=False),
        sa.Column('electionId', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['electionId'], ['election.electionId'], name='stationaryitem_ibfk_1'),
        sa.PrimaryKeyConstraint('stationaryItemId'),
        mysql_collate='utf8mb4_unicode_ci',
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )
