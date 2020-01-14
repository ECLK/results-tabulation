from app import db
from constants.TALLY_SHEET_CODES import PRE_41, PRE_30_PD, PRE_30_ED, \
    PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS, PRE_ALL_ISLAND_RESULTS, CE_201, CE_201_PV

TALLY_SHEET_CODE_MAP_COLUMN_NAME = {
    PRE_41: "pre_41_tallySheetId",
    PRE_30_PD: "pre_30_pd_tallySheetId",
    PRE_30_ED: "pre_30_ed_tallySheetId",
    PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS: "pre_all_island_ed_tallySheetId",
    PRE_ALL_ISLAND_RESULTS: "pre_all_island_tallySheetId",
    CE_201: "ce_201_tallySheetId",
    CE_201_PV: "ce_201_pv_tallySheetId"
}


class TallySheetMapModel(db.Model):
    __tablename__ = 'tallySheet_map'
    tallySheetMapId = db.Column(db.Integer, primary_key=True, autoincrement=True)

    pre_41_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
    pre_34_co_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
    ce_201_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
    ce_201_pv_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)

    pre_30_pd_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
    pre_34_i_ro_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
    pre_34_pd_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)

    pre_30_ed_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
    pre_34_ii_ro_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
    pre_34_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
    pre_34_ed_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)

    pre_all_island_ed_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
    pre_all_island_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
    pre_34_ai_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)

    def __init__(
            self,
            pre_41_tallySheetId=None,
            pre_34_co_tallySheetId=None,
            ce_201_tallySheetId=None,
            ce_201_pv_tallySheetId=None,

            pre_30_pd_tallySheetId=None,
            pre_34_i_ro_tallySheetId=None,
            pre_34_pd_tallySheetId=None,

            pre_30_ed_tallySheetId=None,
            pre_34_ii_ro_tallySheetId=None,
            pre_34_tallySheetId=None,
            pre_34_ed_tallySheetId=None,

            pre_all_island_ed_tallySheetId=None,
            pre_all_island_tallySheetId=None,
            pre_34_ai_tallySheetId=None
    ):
        super(TallySheetMapModel, self).__init__(
            pre_41_tallySheetId=pre_41_tallySheetId,
            pre_34_co_tallySheetId=pre_34_co_tallySheetId,
            ce_201_tallySheetId=ce_201_tallySheetId,
            ce_201_pv_tallySheetId=ce_201_pv_tallySheetId,

            pre_30_pd_tallySheetId=pre_30_pd_tallySheetId,
            pre_34_i_ro_tallySheetId=pre_34_i_ro_tallySheetId,
            pre_34_pd_tallySheetId=pre_34_pd_tallySheetId,

            pre_30_ed_tallySheetId=pre_30_ed_tallySheetId,
            pre_34_ii_ro_tallySheetId=pre_34_ii_ro_tallySheetId,
            pre_34_tallySheetId=pre_34_tallySheetId,
            pre_34_ed_tallySheetId=pre_34_ed_tallySheetId,

            pre_all_island_ed_tallySheetId=pre_all_island_ed_tallySheetId,
            pre_all_island_tallySheetId=pre_all_island_tallySheetId,
            pre_34_ai_tallySheetId=pre_34_ai_tallySheetId
        )
        db.session.add(self)
        db.session.flush()


Model = TallySheetMapModel


def create(
        pre_41_tallySheetId=None,
        pre_34_co_tallySheetId=None,
        ce_201_tallySheetId=None,
        ce_201_pv_tallySheetId=None,

        pre_30_pd_tallySheetId=None,
        pre_34_i_ro_tallySheetId=None,
        pre_34_pd_tallySheetId=None,

        pre_30_ed_tallySheetId=None,
        pre_34_ii_ro_tallySheetId=None,
        pre_34_tallySheetId=None,
        pre_34_ed_tallySheetId=None,

        pre_all_island_ed_tallySheetId=None,
        pre_all_island_tallySheetId=None,
        pre_34_ai_tallySheetId=None
):
    election = Model(
        pre_41_tallySheetId=pre_41_tallySheetId,
        pre_34_co_tallySheetId=pre_34_co_tallySheetId,
        ce_201_tallySheetId=ce_201_tallySheetId,
        ce_201_pv_tallySheetId=ce_201_pv_tallySheetId,

        pre_30_pd_tallySheetId=pre_30_pd_tallySheetId,
        pre_34_i_ro_tallySheetId=pre_34_i_ro_tallySheetId,
        pre_34_pd_tallySheetId=pre_34_pd_tallySheetId,

        pre_30_ed_tallySheetId=pre_30_ed_tallySheetId,
        pre_34_ii_ro_tallySheetId=pre_34_ii_ro_tallySheetId,
        pre_34_tallySheetId=pre_34_tallySheetId,
        pre_34_ed_tallySheetId=pre_34_ed_tallySheetId,

        pre_all_island_ed_tallySheetId=pre_all_island_ed_tallySheetId,
        pre_all_island_tallySheetId=pre_all_island_tallySheetId,
        pre_34_ai_tallySheetId=pre_34_ai_tallySheetId
    )

    return election
