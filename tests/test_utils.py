from datetime import datetime

from app import db
from orm.entities import Area
from orm.entities.Audit.Stamp import Stamp


def get_mock_stamp():
    mock_stamp = Stamp()
    mock_stamp.ip = "0.0.0.0"
    mock_stamp.createdBy = "TestAdmin"
    mock_stamp.createdAt = datetime.now()
    db.session.add(mock_stamp)
    db.session.flush()

    return mock_stamp


def get_mock_area_ids():
    areas = db.session.query(Area.Model).all()
    return set([area.areaId for area in areas])
