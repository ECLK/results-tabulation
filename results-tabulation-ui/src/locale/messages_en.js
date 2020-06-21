export const MESSAGES_EN = {
    error_input: "Please check the input values for errors",
    error_updating_report: "Unknown error occurred while updating the report.",
    error_verifying_report: "Unknown error occurred while verifying the report.",
    error_unlock_report: "Unknown error occurred while unlocking the report.",
    error_upload: "Unknown error occurred while uploading proof.",
    error_release: "Unknown error occurred while releasing.",
    error_notify: "Unknown error occurred while notifying.",
    error_tallysheet_not_reachable: "Tally sheet is not reachable.",
    error_tallysheet_save: "Unknown error occurred while saving the tally sheet.",
    error_tallysheet_submit: "Unknown error occurred while submitting the tally sheet.",
    error_tally_sheet_same_user_cannot_submit_and_lock_tally_sheet: "You cannot verify/ confirm a tally sheet last edited by yourself",
    success_report_editable: "Report was made editable successfully.",
    success_report_verify: "Report was verified successfully.",
    success_report_unlock: "Report was unlocked successfully.",
    success_pre41_submit: "Tally sheet was submitted successfully",
    success_upload: "Proof sheet was submitted successfully",
    success_release: "Report released successfully.",
    success_notify: "Report notified successfully.",
    error_preferences_not_enabled_yet: "Preferences have not been enabled yet.",
};

export const API_MESSAGES_EN = {
    // Authorization
    1000: "No valid user found.",
    1001: "No valid user role found.",
    1002: "No matching claim found.",
    1003: "Invalid authorization token.",
    1004: "No authorization header found.",
    1005: "Your are not authorized to view tally sheet.",
    1006: "Your are not authorized to edit tally sheet.",
    1007: "You cannot verify the data last edited by yourself.",
    1008: "Workflow action is not authorized",

    // Forbidden
    2000: "PE-R2 cannot be viewed unless PE-CE-RO-V2 is verified with a total of votes of non zero.",
    2001: "Proof requires at least one evidence, please upload.",
    2002: "No more evidence is accepted to this proof",
    2003: "PE-21 cannot be processed before PE-R2 is completed and verified.",

    // Not found
    3000: "Election is not found.",
    3001: "Proof is not found.",
    3002: "Tally sheet is not found.",
    3003: "Tally sheet version is not found.",
    3004: "Submission is not found.",

    // Method not allowed
    4000: "Tally sheet is no longer readable.",
    4001: "Tally sheet is no longer editable.",
    4002: "Tally sheet is no longer accepting proof documents.",
    4003: "Tally sheet is incomplete.",
    4004: "Submission irrelevant version cannot be mapped",
    4005: "Workflow action is now allowed.",
    4006: "Tally sheet is not allowed to be notified.",
    4007: "Tally sheet is not allowed to be release.",
    4008: "Cannot request changes since the data from this report has been already aggregated in verified summary reports."

}
