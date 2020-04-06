from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from exception.messages import MESSAGE_CODE_PROOF_CANNOT_BE_CONFIRMED_WITHOUT_EVIDENCE, \
    MESSAGE_CODE_PROOF_NOT_MORE_EVIDENCE_ACCEPTED, MESSAGE_CODE_PROOF_NOT_FOUND
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

    @classmethod
    def create(cls, proofType=ProofTypeEnum.ManuallyFilledTallySheets):
        proof = cls(
            proofType=proofType,
            scannedFilesFolderId=Folder.create().folderId,
            proofStampId=Stamp.create().stampId
        )

        db.session.add(proof)
        db.session.flush()

        return proof

    def close(self):
        self.finished = True

        db.session.add(self)
        db.session.flush()

    def open(self):
        self.finished = False

        db.session.add(self)
        db.session.flush()

    def size(self):
        return len(self.scannedFiles)


Model = ProofModel
create = Model.create


def get_all():
    query = Model.query

    return query


def create(proofType=ProofTypeEnum.ManuallyFilledTallySheets):
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
        raise NotFoundException(
            "Proof not found associated with the given proofId (proofId=%d)" % proofId,
            code=MESSAGE_CODE_PROOF_NOT_FOUND
        )
    else:
        if finished is not None:
            if len(instance.scannedFiles) is 0:
                raise ForbiddenException(
                    message="A proof required at least one evidence. Please upload an evidence (proofId=%d)" % proofId,
                    code=MESSAGE_CODE_PROOF_CANNOT_BE_CONFIRMED_WITHOUT_EVIDENCE
                )

            instance.finished = finished

        db.session.flush()

        return instance


def upload_file(proofId, fileSource, fileType):
    proof = get_by_id(proofId=proofId)

    if proof is None:
        raise NotFoundException(
            message="Proof not found associated with the given proofId (proofId=%d)" % proofId,
            code=MESSAGE_CODE_PROOF_NOT_FOUND
        )
    elif proof.finished is True:
        raise ForbiddenException(
            message="No more evidence is accepted for this proof (proofId=%d)" % proofId,
            code=MESSAGE_CODE_PROOF_NOT_MORE_EVIDENCE_ACCEPTED
        )
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
