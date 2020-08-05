import React, {useContext, useEffect, useState} from "react";
import Dialog from "@material-ui/core/Dialog";
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import DialogTitle from '@material-ui/core/DialogTitle';
import {ElectionContext} from "../../services/election.provider";
import DialogContent from "@material-ui/core/DialogContent";
import DialogActions from "@material-ui/core/DialogActions";
import Button from "@material-ui/core/Button";


export function PartySelectionDialog({electionId, open, handleClose, handleOk}) {
    const electionContext = useContext(ElectionContext);

    const [election, setElection] = useState(null);

    useEffect(() => {
        electionContext.getElectionById(electionId).then(setElection);
    }, [electionId]);

    return <Dialog onClose={handleClose()} aria-labelledby="simple-dialog-title" open={open}>
        <DialogTitle id="form-dialog-title">Parties and Independent Groups</DialogTitle>
        <DialogContent>
            <List>
                {election && election.parties && election.parties.map((party) => {
                    const {partyId, partyName, partyAbbreviation} = party;
                    return <ListItem button onClick={handleOk(party)} key={partyId}>
                        <ListItemText inset={false} primary={
                            <span><strong>{partyAbbreviation}</strong>&nbsp; - &nbsp;{partyName}</span>
                        }/>
                    </ListItem>
                })}
            </List>
            <List>
            </List>
        </DialogContent>
        <DialogActions>
            <Button onClick={handleClose()} color="primary">
                Cancel
            </Button>
        </DialogActions>
    </Dialog>
}