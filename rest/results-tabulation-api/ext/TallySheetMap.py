from app import db


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

    pe_27_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
    pe_4_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
    pe_ce_ro_v1_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
    pe_r1_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
    pe_ce_ro_pr_1_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
    pe_ce_ro_v2_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
    pe_r2_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
    pe_ce_ro_pr_2_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)
    pe_ce_ro_pr_3_tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=True)

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
            pre_34_ai_tallySheetId=None,

            pe_27_tallySheetId=None,
            pe_4_tallySheetId=None,
            pe_ce_ro_v1_tallySheetId=None,
            pe_r1_tallySheetId=None,
            pe_ce_ro_pr_1_tallySheetId=None,
            pe_ce_ro_v2_tallySheetId=None,
            pe_r2_tallySheetId=None,
            pe_ce_ro_pr_2_tallySheetId=None,
            pe_ce_ro_pr_3_tallySheetId=None
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
            pre_34_ai_tallySheetId=pre_34_ai_tallySheetId,

            pe_27_tallySheetId=pe_27_tallySheetId,
            pe_4_tallySheetId=pe_4_tallySheetId,
            pe_ce_ro_v1_tallySheetId=pe_ce_ro_v1_tallySheetId,
            pe_r1_tallySheetId=pe_r1_tallySheetId,
            pe_ce_ro_pr_1_tallySheetId=pe_ce_ro_pr_1_tallySheetId,
            pe_ce_ro_v2_tallySheetId=pe_ce_ro_v2_tallySheetId,
            pe_r2_tallySheetId=pe_r2_tallySheetId,
            pe_ce_ro_pr_2_tallySheetId=pe_ce_ro_pr_2_tallySheetId,
            pe_ce_ro_pr_3_tallySheetId=pe_ce_ro_pr_3_tallySheetId
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
        pre_34_ai_tallySheetId=None,

        pe_27_tallySheetId=None,
        pe_4_tallySheetId=None,
        pe_ce_ro_v1_tallySheetId=None,
        pe_r1_tallySheetId=None,
        pe_ce_ro_pr_1_tallySheetId=None,
        pe_ce_ro_v2_tallySheetId=None,
        pe_r2_tallySheetId=None,
        pe_ce_ro_pr_2_tallySheetId=None,
        pe_ce_ro_pr_3_tallySheetId=None
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
        pre_34_ai_tallySheetId=pre_34_ai_tallySheetId,

        pe_27_tallySheetId=pe_27_tallySheetId,
        pe_4_tallySheetId=pe_4_tallySheetId,
        pe_ce_ro_v1_tallySheetId=pe_ce_ro_v1_tallySheetId,
        pe_r1_tallySheetId=pe_r1_tallySheetId,
        pe_ce_ro_pr_1_tallySheetId=pe_ce_ro_pr_1_tallySheetId,
        pe_ce_ro_v2_tallySheetId=pe_ce_ro_v2_tallySheetId,
        pe_r2_tallySheetId=pe_r2_tallySheetId,
        pe_ce_ro_pr_2_tallySheetId=pe_ce_ro_pr_2_tallySheetId,
        pe_ce_ro_pr_3_tallySheetId=pe_ce_ro_pr_3_tallySheetId
    )

    return election
