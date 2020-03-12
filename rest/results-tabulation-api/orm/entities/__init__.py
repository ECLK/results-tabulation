from orm.entities.IO import File, Folder
from orm.entities.IO.Folder import FolderFile
from orm.entities.IO.File import Image
from orm.entities import Election, Candidate, Workflow
from orm.entities import Area
from orm.entities.Area import Electorate
from orm.entities import Party
from orm.entities.Election import ElectionParty, ElectionCandidate
from orm.entities import Invoice, StationaryItem, BallotBox, Ballot, BallotBook
from orm.entities.Invoice import InvoiceStationaryItem
from orm.entities import Proof, History
from orm.entities.History import HistoryVersion
from orm.entities.Area import Office
from orm.entities.Area.Electorate import Country, Province, AdministrativeDistrict, ElectoralDistrict, PollingDivision, \
    PollingDistrict

from orm.entities.Area.Office import DistrictCentre, CountingCentre, PollingStation, ElectionCommission

from orm.entities import Submission, SubmissionVersion
from orm.entities.SubmissionVersion import TallySheetVersion

from orm.entities.Election import InvalidVoteCategory
from orm.entities.Dashboard import StatusCE201
from orm.entities.Dashboard import StatusPRE41
from orm.entities.Dashboard import StatusPRE34


# import sadisplay
# import codecs
#
# desc = sadisplay.describe([
#     File.Model, Folder.Model, FolderFile.Model,
#
#     Party.Model, Candidate.Model,
#
#     Election.Model, Area.Model, ElectionParty.Model, ElectionCandidate.Model,
#
#     Invoice.Model,
#     StationaryItem.Model, BallotBox.Model, Ballot.Model,
#     InvoiceStationaryItem.Model,
#
#     Proof.Model,
#
#     History.Model, HistoryVersion.Model,
#
#     PartyWiseResult.Model, PartyCount.Model,
#     CandidateWiseResult.Model, CandidateCount.Model,
#
#     Submission.Model, SubmissionVersion.Model,
#
#     TallySheet.Model,
#
#     TallySheetVersion.Model,
#     TallySheetVersionPRE41.Model,
#
#     Report.Model,
#     # Report_PRE_41.Model, Report_PRE_30_PD.Model, Report_PRE_30_ED
#
#     ReportVersion.Model,
#     # ReportVersion_PRE_41.Model, ReportVersion_PRE_30_PD.Model, ReportVersion_PRE_30_ED
# ])
#
# with codecs.open('./schemas/schema.plantuml', 'w', encoding='utf-8') as f:
#     f.write(sadisplay.plantuml(desc))
#
# with codecs.open('./schemas/schema.dot', 'w', encoding='utf-8') as f:
#     f.write(sadisplay.dot(desc))
