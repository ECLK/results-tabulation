"""empty message

Revision ID: 92daa0023135
Revises: 611e7f408080
Create Date: 2019-10-14 15:35:11.115404

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

# revision identifiers, used by Alembic.
revision = 'dc592322ba4f'
down_revision = '611e7f408080'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('barcode',
                    sa.Column('barcodeId', sa.Integer(), nullable=False),
                    sa.Column('barcodeString', sa.String(length=13), nullable=True),
                    sa.PrimaryKeyConstraint('barcodeId')
                    )
    op.add_column('stamp', sa.Column('barcodeId', sa.Integer(), nullable=True))
    op.create_foreign_key('stamp_barcodeId_fk', 'stamp', 'barcode', ['barcodeId'], ['barcodeId'])

    # Add bar codes to all the stamps.

    Base = declarative_base()

    class _BarcodeModel(Base):
        __tablename__ = 'barcode'
        barcodeId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        barcodeString = sa.Column(sa.String(13), nullable=True)

    class _StampModel(Base):
        __tablename__ = 'stamp'
        stampId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        barcodeId = sa.Column(sa.Integer, sa.ForeignKey(_BarcodeModel.__table__.c.barcodeId), nullable=False)

    def _get_barcode_string(num):
        num_str = str(num)
        for i in range(12 - len(num_str)):
            num_str = "0" + num_str
        return num_str

    bind = op.get_bind()
    session = Session(bind=bind)

    existing_stamps = session.query(_StampModel).all()
    for existing_stamp in existing_stamps:
        barcode = _BarcodeModel()
        session.add(barcode)
        session.flush()
        barcode.barcodeString = _get_barcode_string(barcode.barcodeId)

        existing_stamp.barcodeId = barcode.barcodeId
        session.flush()

    session.commit()


def downgrade():
    op.drop_constraint('stamp_barcodeId_fk', 'stamp', type_='foreignkey')
    op.drop_column('stamp', 'barcodeId')
    op.drop_table('barcode')
