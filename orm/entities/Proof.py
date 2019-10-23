from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from orm.entities.Audit import Stamp
from orm.entities.IO import File, Folder
from orm.entities.IO.Folder import FolderFile
from orm.enums import ProofTypeEnum
from exception import NotFoundException, ForbiddenException


class ProofModel(db.Model):
    __tablename__ = 'proof'
    proofId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    proofType = db.Column(db.Enum(ProofTypeEnum), nullable=False)
    proofStampId = db.Column(db.Integer, db.ForeignKey(Stamp.Model.__table__.c.stampId), nullable=False)
    scannedFilesFolderId = db.Column(db.Integer, db.ForeignKey(Folder.Model.__table__.c.folderId), nullable=False)
    finished = db.Column(db.Boolean, default=False)

    scannedFilesFolder = relationship(Folder.Model, foreign_keys=[scannedFilesFolderId])
    proofStamp = relationship(Stamp.Model, foreign_keys=[proofStampId])

    scannedFiles = association_proxy("scannedFilesFolder", "files")
    createdBy = association_proxy("proofStamp", "createdBy")
    createdAt = association_proxy("proofStamp", "createdAt")


Model = ProofModel


def get_all():
    query = Model.query

    return query


def create(proofType):
    scanned_files_folder = Folder.create()
    proof_stamp = Stamp.create()

    result = ProofModel(
        proofType=proofType,
        scannedFilesFolderId=scanned_files_folder.folderId,
        proofStampId=proof_stamp.stampId
    )

    db.session.add(result)
    db.session.flush()

    return result


def update(proofId, finished=None):
    instance = get_by_id(proofId)

    if instance is None:
        raise NotFoundException("Proof not found associated with the given proofId (proofId=%d)" % proofId)
    else:
        if finished is not None:
            if len(instance.scannedFiles) is 0:
                raise ForbiddenException(
                    "A proof required at least one evidence. Please upload an evidence (proofId=%d)" % proofId)

            instance.finished = finished

        db.session.flush()

        return instance


def upload_file(proofId, fileSource, fileType):
    proof = get_by_id(proofId=proofId)

    if proof is None:
        raise NotFoundException("Proof not found associated with the given proofId (proofId=%d)" % proofId)
    elif proof.finished is True:
        raise ForbiddenException("No more evidence is accepted for this proof (proofId=%d)" % proofId)
    else:
        file = File.createFromFileSource(
            fileSource=fileSource,
            fileType=fileType
        )

        FolderFile.create(
            folderId=proof.scannedFilesFolderId,
            fileId=file.fileId
        )

        return proof


def get_by_id(proofId):
    result = Model.query.filter(
        Model.proofId == proofId
    ).one_or_none()

    return result
