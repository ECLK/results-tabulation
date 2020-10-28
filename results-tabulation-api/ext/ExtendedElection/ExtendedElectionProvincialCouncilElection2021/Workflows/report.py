from orm.entities import Workflow
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.WORKFLOW_ACTION_TYPE import \
    WORKFLOW_ACTION_TYPE_VIEW, WORKFLOW_ACTION_TYPE_REQUEST_CHANGES, \
    WORKFLOW_ACTION_TYPE_VERIFY, WORKFLOW_ACTION_TYPE_PRINT
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.WORKFLOW_STATUS_TYPE import \
    WORKFLOW_STATUS_TYPE_EMPTY, WORKFLOW_STATUS_TYPE_SAVED, WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED, \
    WORKFLOW_STATUS_TYPE_VERIFIED


def create_workflow():
    return Workflow.create(
        workflowName="Report",
        firstStatus=WORKFLOW_STATUS_TYPE_EMPTY,
        lastStatus=WORKFLOW_STATUS_TYPE_VERIFIED,
        statuses=[
            WORKFLOW_STATUS_TYPE_EMPTY,
            WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED,
            WORKFLOW_STATUS_TYPE_SAVED,
            WORKFLOW_STATUS_TYPE_VERIFIED
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
                {"name": "Request Changes", "type": WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
                 "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED}
            ],
            WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED: [
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                 "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
                {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
            ]
        }
    )
