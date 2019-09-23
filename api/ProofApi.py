from app import db
from util import RequestBody
import connexion

from schemas import Proof_Schema as Schema
from orm.entities import Proof
from orm.enums import FileTypeEnum


def get_all():
    result = Proof.get_all()

    return Schema(many=True).dump(result).data


def get_by_id(proofId):
    result = Proof.get_by_id(
        proofId=proofId
    )

    return Schema().dump(result).data


def upload_file(body):
    request_body = RequestBody(body)
    result = Proof.upload_file(
        proofId=request_body.get("proofId"),
        fileSource=connexion.request.files['scannedFile'],
        fileType=FileTypeEnum.Image
    )

    db.session.commit()

    return Schema().dump(result).data, 201


def finish(proofId):
    result = Proof.update(
        finished=True,
        proofId=proofId
    )

    db.session.commit()

    return Schema().dump(result).data, 201
