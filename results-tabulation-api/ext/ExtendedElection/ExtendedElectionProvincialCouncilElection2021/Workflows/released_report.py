from orm.entities import Workflow
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.WORKFLOW_ACTION_TYPE import \
    WORKFLOW_ACTION_TYPE_VIEW, \
    WORKFLOW_ACTION_TYPE_REQUEST_CHANGES, \
    WORKFLOW_ACTION_TYPE_VERIFY, \
    WORKFLOW_ACTION_TYPE_MOVE_TO_CERTIFY, WORKFLOW_ACTION_TYPE_CERTIFY, WORKFLOW_ACTION_TYPE_RELEASE, \
    WORKFLOW_ACTION_TYPE_PRINT, WORKFLOW_ACTION_TYPE_UPLOAD_PROOF_DOCUMENT, WORKFLOW_ACTION_TYPE_PRINT_LETTER, \
    WORKFLOW_ACTION_TYPE_RELEASE_NOTIFY, WORKFLOW_ACTION_TYPE_BACK_TO_VERIFIED
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.WORKFLOW_STATUS_TYPE import \
    WORKFLOW_STATUS_TYPE_EMPTY, \
    WORKFLOW_STATUS_TYPE_SAVED, WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED, \
    WORKFLOW_STATUS_TYPE_VERIFIED, WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY, \
    WORKFLOW_STATUS_TYPE_CERTIFIED, WORKFLOW_STATUS_TYPE_RELEASED, WORKFLOW_STATUS_TYPE_RELEASE_NOTIFIED


def create_workflow():
    return Workflow.create(
        workflowName="Released Report",
        firstStatus=WORKFLOW_STATUS_TYPE_EMPTY,
        lastStatus=WORKFLOW_STATUS_TYPE_RELEASED,
        statuses=[
            WORKFLOW_STATUS_TYPE_EMPTY,
            WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED,
            WORKFLOW_STATUS_TYPE_SAVED,
            WORKFLOW_STATUS_TYPE_VERIFIED,
            WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY,
            WORKFLOW_STATUS_TYPE_CERTIFIED,
            WORKFLOW_STATUS_TYPE_RELEASED
        ],
        actionsMap={
            WORKFLOW_STATUS_TYPE_EMPTY: [
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
            ],
            WORKFLOW_STATUS_TYPE_SAVED: [
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
            ],
            WORKFLOW_STATUS_TYPE_VERIFIED: [
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                {"name": "Print Letter", "type": WORKFLOW_ACTION_TYPE_PRINT_LETTER,
                 "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                {"name": "Request Changes", "type": WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
                 "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
                {"name": "Move to Certify", "type": WORKFLOW_ACTION_TYPE_MOVE_TO_CERTIFY,
                 "toStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY},
            ],
            WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED: [
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                 "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
                {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
            ],
            WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY: [
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                 "toStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY},
                {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT,
                 "toStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY},
                {"name": "Upload Certified Documents", "type": WORKFLOW_ACTION_TYPE_UPLOAD_PROOF_DOCUMENT,
                 "toStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY},
                {"name": "Certify", "type": WORKFLOW_ACTION_TYPE_CERTIFY,
                 "toStatus": WORKFLOW_STATUS_TYPE_CERTIFIED},
                {"name": "Back to Verified", "type": WORKFLOW_ACTION_TYPE_BACK_TO_VERIFIED,
                 "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
            ],
            WORKFLOW_STATUS_TYPE_CERTIFIED: [
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_CERTIFIED},
                {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT, "toStatus": WORKFLOW_STATUS_TYPE_CERTIFIED},
                {"name": "Notify Release", "type": WORKFLOW_ACTION_TYPE_RELEASE_NOTIFY,
                 "toStatus": WORKFLOW_STATUS_TYPE_RELEASE_NOTIFIED},
                {"name": "Back to Verified", "type": WORKFLOW_ACTION_TYPE_BACK_TO_VERIFIED,
                 "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
            ],
            WORKFLOW_STATUS_TYPE_RELEASE_NOTIFIED: [
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                 "toStatus": WORKFLOW_STATUS_TYPE_RELEASE_NOTIFIED},
                {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT,
                 "toStatus": WORKFLOW_STATUS_TYPE_RELEASE_NOTIFIED},
                {"name": "Release", "type": WORKFLOW_ACTION_TYPE_RELEASE,
                 "toStatus": WORKFLOW_STATUS_TYPE_RELEASED},
                {"name": "Back to Verified", "type": WORKFLOW_ACTION_TYPE_BACK_TO_VERIFIED,
                 "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
            ],
            WORKFLOW_STATUS_TYPE_RELEASED: [
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW, "toStatus": WORKFLOW_STATUS_TYPE_RELEASED},
                {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT, "toStatus": WORKFLOW_STATUS_TYPE_RELEASED},
                {"name": "Back to Verified", "type": WORKFLOW_ACTION_TYPE_BACK_TO_VERIFIED,
                 "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED}
            ]
        }
    )
