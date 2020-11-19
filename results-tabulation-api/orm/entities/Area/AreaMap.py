from app import db


class AreaMapModel(db.Model):
    __tablename__ = 'area_map'
    areaMapId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=True)
    voteType = db.Column(db.String(100), nullable=False)
    pollingStationId = db.Column(db.Integer, db.ForeignKey("area.areaId"), nullable=True)
    countingCentreId = db.Column(db.Integer, db.ForeignKey("area.areaId"), nullable=True)
    districtCentreId = db.Column(db.Integer, db.ForeignKey("area.areaId"), nullable=True)
    electionCommissionId = db.Column(db.Integer, db.ForeignKey("area.areaId"), nullable=True)
    pollingDistrictId = db.Column(db.Integer, db.ForeignKey("area.areaId"), nullable=True)
    pollingDivisionId = db.Column(db.Integer, db.ForeignKey("area.areaId"), nullable=True)
    electoralDistrictId = db.Column(db.Integer, db.ForeignKey("area.areaId"), nullable=True)
    administrativeDistrictId = db.Column(db.Integer, db.ForeignKey("area.areaId"), nullable=True)
    provinceId = db.Column(db.Integer, db.ForeignKey("area.areaId"), nullable=True)
    countryId = db.Column(db.Integer, db.ForeignKey("area.areaId"), nullable=True)

    def __init__(
            self,
            electionId,
            voteType,
            pollingStationId=None,
            countingCentreId=None,
            districtCentreId=None,
            electionCommissionId=None,
            pollingDistrictId=None,
            pollingDivisionId=None,
            electoralDistrictId=None,
            administrativeDistrictId=None,
            provinceId=None,
            countryId=None
    ):
        super(AreaMapModel, self).__init__(
            electionId=electionId,
            voteType=voteType,
            pollingStationId=pollingStationId,
            countingCentreId=countingCentreId,
            districtCentreId=districtCentreId,
            electionCommissionId=electionCommissionId,
            pollingDistrictId=pollingDistrictId,
            pollingDivisionId=pollingDivisionId,
            electoralDistrictId=electoralDistrictId,
            administrativeDistrictId=administrativeDistrictId,
            provinceId=provinceId,
            countryId=countryId
        )
        db.session.add(self)
        db.session.flush()


Model = AreaMapModel


def create(
        electionId,
        voteType,
        pollingStationId=None,
        countingCentreId=None,
        districtCentreId=None,
        electionCommissionId=None,
        pollingDistrictId=None,
        pollingDivisionId=None,
        electoralDistrictId=None,
        administrativeDistrictId=None,
        provinceId=None,
        countryId=None
):
    election = Model(
        electionId=electionId,
        voteType=voteType,
        pollingStationId=pollingStationId,
        countingCentreId=countingCentreId,
        districtCentreId=districtCentreId,
        electionCommissionId=electionCommissionId,
        pollingDistrictId=pollingDistrictId,
        pollingDivisionId=pollingDivisionId,
        electoralDistrictId=electoralDistrictId,
        administrativeDistrictId=administrativeDistrictId,
        provinceId=provinceId,
        countryId=countryId
    )

    return election
