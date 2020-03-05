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


def upgrade():
    Base = declarative_base()
    bind = op.get_bind()
    session = Session(bind=bind)

    op.add_column('file', sa.Column('fileContent', mysql.LONGBLOB(), nullable=True))

    class _File(Base):
        __tablename__ = 'file'
        fileId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
        fileContent = sa.Column(LONGBLOB, nullable=True)

    data_directory_path = "./data"

    if os.path.isdir(data_directory_path):
        for filename in os.listdir(data_directory_path):
            file = session.query(_File).filter(_File.fileId == filename).one_or_none()
            if file is not None:
                with open("./data/%s" % filename, "rb") as file:
                    file.fileContent = file.read()

    session.commit()


def downgrade():
    op.drop_column('file', 'fileContent')
