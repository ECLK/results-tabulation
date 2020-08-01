import React, {useContext, useEffect, useState} from "react";
import Dialog from "@material-ui/core/Dialog";
import Avatar from '@material-ui/core/Avatar';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import ListItemText from '@material-ui/core/ListItemText';
import DialogTitle from '@material-ui/core/DialogTitle';
import PersonIcon from '@material-ui/icons/Person';
import {ElectionContext} from "../../services/election.provider";
import Processing from "../processing";


export function PartySelectionDialog({electionId, open, handleClose, handleOk}) {
    const electionContext = useContext(ElectionContext);

    const [election, setElection] = useState(null);

    useEffect(() => {
        electionContext.getElectionById(electionId).then(setElection);
    }, [electionId]);

    return <Dialog onClose={handleClose()} aria-labelledby="simple-dialog-title" open={open}>
        <Processing showProgress={!election}>
            <List>
                {election && election.parties && election.parties.map((party) => {
                    const {partyId, partyName, partyAbbreviation} = party;
                    return <ListItem button onClick={handleOk(party)} key={partyId}>
                        <ListItemText primary={partyAbbreviation + " - " + partyName}/>
                    </ListItem>
                })}
            </List>
        </Processing>
    </Dialog>
}