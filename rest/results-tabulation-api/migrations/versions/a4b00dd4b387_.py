"""

Revision ID: a4b00dd4b387
Revises: 65900aaf5afd
Create Date: 2019-12-05 18:13:34.550588

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.dialects.mysql import LONGBLOB
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
import os

# revision identifiers, used by Alembic.
revision = 'a4b00dd4b387'
down_revision = '65900aaf5afd'
branch_labels = None
depends_on = None

Base = declarative_base()
bind = op.get_bind()
session = Session(bind=bind)


class _File(Base):
    __tablename__ = 'file'
    fileId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    fileContent = sa.Column(LONGBLOB, nullable=True)


def upgrade():
    op.add_column('file', sa.Column('fileContent', mysql.LONGBLOB(), nullable=True))

    for filename in os.listdir("./data"):
        print(filename)
        file = session.query(_File).filter(_File.fileId == filename).one_or_none()
        if file is not None:
            with open("./data/%s" % filename, "r") as file:
                file.fileContent = file.read()

    session.commit()


def downgrade():
    op.drop_column('file', 'fileContent')
