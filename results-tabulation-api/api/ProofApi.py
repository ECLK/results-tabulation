from app import db
from exception import NotFoundException
from exception.messages import MESSAGE_CODE_PROOF_NOT_FOUND
from util import RequestBody, get_paginated_query
import connexion

from schemas import Proof_Schema as Schema
from orm.entities import Proof
from orm.enums import FileTypeEnum


def get_all():
    result = Proof.get_all()

    result = get_paginated_query(result).all()

    return Schema(many=True).dump(result).data


def get_by_id(proofId):
    result = Proof.get_by_id(
        proofId=proofId
    )

    if result is None:
        raise NotFoundException("Proof not found. (proofId=%d)" % proofId, code=MESSAGE_CODE_PROOF_NOT_FOUND)

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
