import React, {useContext, useEffect, useState} from "react";
import {getTallySheetProof, getProofImage, TALLY_SHEET_STATUS_ENUM} from "../services/tabulation-api";
import {MESSAGE_TYPES} from "../services/messages.provider";
import {
    PATH_ELECTION_RESULTS_RELEASE
} from "../App";
import Button from "@material-ui/core/Button";
import CircularProgress from '@material-ui/core/CircularProgress';
import {MESSAGES_EN} from "../locale/messages_en";
import PrintLetterButton from "../components/tally-sheet/print-letter-button";
import TabulationPage from "./index";
import {TallySheetContext} from "../services/tally-sheet.provider";

export default function ReleaseView(props) {
    const tallySheetContext = useContext(TallySheetContext);
    const tallySheet = tallySheetContext.getTallySheetById(props.tallySheetId);

    const PROOF_STATUS_ENUM = {
        PROOF_NOT_LOADED: -4,
        PROOF_LOADING: -3,
        PROOF_NOT_UPLOADED: -2,
    };

    const RELEASE_STATUS_ENUM = {
        RELEASE_STATE_NOT_LOADED: -4,
        RELEASE_STATE_LOADING: -3,
        RELEASE_UNFINISHED: 0,
        RELEASE_FINISHED: 1,
    };

    const {election, messages} = props;
    const {electionName} = election;
    const [tallySheetVersionId, setTallySheetVersionId] = useState(null);
    const [tallySheetVersionHtml, setTallySheetVersionHtml] = useState("");
    const [tallySheetProof, setTallySheetProof] = useState("");
    const [latestProofId, setLatestProofId] = useState(PROOF_STATUS_ENUM.PROOF_NOT_LOADED);
    const [latestProof, setLatestProof] = useState(null);
    const [releaseState, setReleaseState] = useState(RELEASE_STATUS_ENUM.RELEASE_STATE_NOT_LOADED);
    const [progress, setProgress] = useState(-1);
    const [processing, setProcessing] = useState(false);
    const [iframeHeight, setIframeHeight] = useState(600);
    const [iframeWidth] = useState("100%");
    const iframeRef = React.createRef();


    const fetchTallySheetVersion = async () => {
        const {tallySheetId, tallySheetCode, latestVersionId, submittedVersionId, lockedVersionId} = tallySheet;
        let tallySheetVersionId = null;
        if (!tallySheet.template.isDerived) {
            if (lockedVersionId) {
                tallySheetVersionId = lockedVersionId;
            } else if (submittedVersionId) {
                tallySheetVersionId = submittedVersionId;
            } else if (latestVersionId) {
                tallySheetVersionId = latestVersionId;
            }
        } else {
            if (lockedVersionId) {
                tallySheetVersionId = lockedVersionId;
            } else {
                const tallySheetVersion = await tallySheetContext.saveTallySheetVersion(tallySheetId, tallySheetCode);
                tallySheetVersionId = tallySheetVersion.tallySheetVersionId;
            }
        }

        setTallySheetVersionId(tallySheetVersionId);
    };

    const fetchTallySheetVersionHtml = async () => {
        setTallySheetVersionHtml("Processing ... ");
        const {tallySheetId} = tallySheet;
        const tallySheetVersionHtml = await tallySheetContext.fetchTallySheetVersionHtml(tallySheetId, tallySheetVersionId);

        setTallySheetVersionHtml(tallySheetVersionHtml)
    };

    const fetchProofStatus = async () => {
        setLatestProofId(PROOF_STATUS_ENUM.PROOF_LOADING);
        setReleaseState(RELEASE_STATUS_ENUM.RELEASE_STATE_LOADING);
        const {submissionProofId} = tallySheet;
        const proofStatus = await getTallySheetProof(submissionProofId);
        updateProofStatus(proofStatus);
    }

    const updateProofStatus = (proofStatus) => {
        const {scannedFiles, finished} = proofStatus;
        setReleaseState(finished ? RELEASE_STATUS_ENUM.RELEASE_FINISHED : RELEASE_STATUS_ENUM.RELEASE_UNFINISHED);
        if (scannedFiles.length > 0) {
            const latestProof = scannedFiles[scannedFiles.length - 1];
            setLatestProof(latestProof);
            setLatestProofId(latestProof.fileId);
        } else {
            setLatestProof(null);
            setLatestProofId(PROOF_STATUS_ENUM.PROOF_NOT_UPLOADED);
        }
    };

    const fetchProofImage = async () => {
        setTallySheetProof("Loading proof image ...");
        const proofImgArray = await getProofImage(latestProofId);
        var proofImgBlob = new Blob([proofImgArray], {type: latestProof.fileMimeType});
        const proofImgDataUrl = URL.createObjectURL(proofImgBlob);
        setTallySheetProof(proofImgDataUrl)
    };

    useEffect(() => {
        latestProofId >= 0 && fetchProofImage();
    }, [latestProofId]);

    useEffect(() => {
        fetchTallySheetVersion() && fetchProofStatus();
    }, [tallySheet]);

    useEffect(() => {
        tallySheetVersionId && fetchTallySheetVersionHtml();
    }, [tallySheetVersionId]);

    const handleIframeHeight = () => (evt) => {
        setIframeHeight(evt.target.contentDocument.documentElement.scrollHeight + 50);
    };


    const handleNotify = () => async (evt) => {
        // setProcessing(true);
        // const {tallySheetId} = tallySheet;
        // try {
        //     setTallySheet(await notifyTallySheet(tallySheetId));
        //     // await fetchProofStatus();
        //     messages.push("Success", MESSAGES_EN.success_notify, MESSAGE_TYPES.SUCCESS);
        // } catch (e) {
        //     messages.push("Error", MESSAGES_EN.error_notify, MESSAGE_TYPES.ERROR);
        // }
        // setProcessing(false);
    };

    const handleRelease = () => async (evt) => {
        // setProcessing(true);
        // const {tallySheetId} = tallySheet;
        // try {
        //     setTallySheet(await releaseTallySheet(tallySheetId));
        //     // await fetchProofStatus();
        //     messages.push("Success", MESSAGES_EN.success_release, MESSAGE_TYPES.SUCCESS);
        // } catch (e) {
        //     messages.push("Error", MESSAGES_EN.error_release, MESSAGE_TYPES.ERROR);
        // }
        // setProcessing(false);
    };

    const handleUpload = () => async (evt) => {
        setProcessing(true);
        try {
            const {submissionProofId} = tallySheet;
            var formData = new FormData();
            formData.append("proofId", submissionProofId);
            formData.append("scannedFile", evt.target.files[0]);
            const proofStatus = await tallySheetContext.uploadTallySheetProof(formData, progressEvent => setProgress(100 * progressEvent.loaded / progressEvent.total));
            updateProofStatus(proofStatus);
            messages.push("Success", MESSAGES_EN.success_upload, MESSAGE_TYPES.SUCCESS);
            setProgress(-1)
        } catch (e) {
            messages.push("Error", MESSAGES_EN.error_upload, MESSAGE_TYPES.ERROR);
        }
        setProcessing(false);
    };

    const getReportViewJsx = () => {
        const {tallySheetCode} = tallySheet;
        const electionId = tallySheet.electionId;
        const additionalBreadCrumbLinks = [
            {
                label: tallySheetCode.toLowerCase() + " release",
                to: PATH_ELECTION_RESULTS_RELEASE(electionId, tallySheetCode, electionId)
            }
        ];

        let leftPlane;

        if (latestProofId === PROOF_STATUS_ENUM.PROOF_LOADING) {
            leftPlane = <div style={{float: "right", width: "50%", textAlign: "center"}}>Loading proof status ...</div>;
        } else if (latestProofId === PROOF_STATUS_ENUM.PROOF_NOT_UPLOADED) {
            leftPlane = <div style={{float: "right", width: "50%", textAlign: "center"}}>Proof not uploaded</div>;
        } else if (latestProofId >= 0) {
            if (tallySheetProof.startsWith('blob:')) {
                leftPlane = <iframe
                    src={tallySheetProof}
                    style={{float: "right", width: "50%"}}
                    height={iframeHeight}
                    width={iframeWidth}
                />;
            } else {
                leftPlane = <div style={{float: "right", width: "50%", textAlign: "center"}}>{tallySheetProof}</div>;
            }
        }

        const isUploadDisabled = tallySheet.tallySheetStatus !== TALLY_SHEET_STATUS_ENUM.VERIFIED ||
            releaseState !== RELEASE_STATUS_ENUM.RELEASE_UNFINISHED;
        // const isReleaseDisabled = isUploadDisabled || latestProofId < 0;
        const imageTitle = releaseState === RELEASE_STATUS_ENUM.RELEASE_FINISHED ? "Released proof" : "Signed draft";
        const progressStyle = {};
        if (progress < 0) {
            progressStyle.visibility = "hidden";
        }

        return <TabulationPage additionalBreadCrumbLinks={additionalBreadCrumbLinks} election={election}>
            <div className="page-content">
                <div>{electionName}</div>
                <div>{tallySheetCode}</div>


                <div className="report-view-status">
                    <div className="report-view-status-actions">

                        <PrintLetterButton
                            variant="outlined" color="default"
                            size="small"
                            onClick={() => {
                            }}
                            tallySheetId={tallySheet.tallySheetId}
                            tallySheetVersionId={tallySheet.lockedVersionId}
                        >
                            Print Letter
                        </PrintLetterButton>
                        <Button
                            variant="outlined" color="default" component="label" size="small"
                            disabled={processing || isUploadDisabled || progress > 0}>
                            Upload Proof
                            <div style={progressStyle} id="upload-progress">
                                <CircularProgress variant="static" size={20} value={progress}/>
                            </div>
                            <input accept="image/*,application/pdf" type="file" style={{display: 'none'}}
                                   onChange={handleUpload()}/>
                        </Button>

                        <Button
                            variant="outlined" color="default" size="small"
                            disabled={processing || !tallySheet.locked || tallySheet.notified}
                            onClick={handleNotify()}>
                            Notify
                        </Button>

                        <Button
                            variant="outlined" color="default" size="small"
                            disabled={processing || !tallySheet.locked || tallySheet.released}
                            onClick={handleRelease()}>
                            Release
                        </Button>
                    </div>
                </div>

                <div id="realease-header">
                    <div id="realease-header-content">
                        <div>
                            <h4> Digital copy </h4>
                        </div>
                        <div>
                            <h4> {imageTitle} </h4>
                        </div>
                    </div>
                </div>

                {leftPlane}
                <iframe
                    id="framehalf"
                    style={{border: "none", width: "100%"}}
                    height={iframeHeight}
                    width={iframeWidth}
                    srcDoc={tallySheetVersionHtml}
                    onLoad={handleIframeHeight()}
                    ref={iframeRef}
                >

                </iframe>
            </div>
        </TabulationPage>
    };

    return getReportViewJsx()
}
