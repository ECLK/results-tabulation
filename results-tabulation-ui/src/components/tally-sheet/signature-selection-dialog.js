import React, {useState} from "react";
import Button from '@material-ui/core/Button';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import Checkbox from '@material-ui/core/Checkbox';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';

const signatures = [
    {"name": "MAHINDA DESHAPRIYA", "designation": "Chairman", "organization": "Election Commission"},
    {"name": "N. J. ABEYESEKERE", "designation": "Member", "organization": "Election Commission"},
    {"name": "S. RATNAJEEVAN H. HOOLE", "designation": "Member", "organization": "Election Commission"}
];

const defaultSignatureSelection = {0: true, 1: true, 2: true};

export function SignatureSelectionDialog({open, handleClose, handleOk}) {
    const [selectedSignatureIds, setSelectedSignatureIds] = useState(defaultSignatureSelection);

    const getSelectedSignatures = () => {
        return signatures.filter((signature, signatureId) => selectedSignatureIds[signatureId]);
    };

    const handleSignatureSelect = (signatureId, isSelected) => (event) => {
        setSelectedSignatureIds({...selectedSignatureIds, [signatureId]: isSelected});
    };

    return <Dialog onClose={handleClose()} aria-labelledby="simple-dialog-title" open={open}>
        <DialogTitle id="form-dialog-title">Signatures</DialogTitle>
        <DialogContent>
            <List>
                {signatures.map((signature, signatureId) => {
                    const {name, designation, organization} = signature;
                    const isSelected = selectedSignatureIds[signatureId];

                    return <ListItem button key={signatureId}>
                        <ListItemText primary={name} secondary={`${designation}, ${organization}`}/>
                        <ListItemSecondaryAction>
                            <Checkbox
                                edge="end"
                                onChange={handleSignatureSelect(signatureId, !isSelected)}
                                checked={isSelected}
                            />
                        </ListItemSecondaryAction>
                    </ListItem>
                })}
            </List>
        </DialogContent>
        <DialogActions>
            <Button onClick={handleClose()} color="primary">
                Cancel
            </Button>
            <Button color="primary" onClick={(event) => {
                handleOk(getSelectedSignatures())(event);
            }}>
                Continue
            </Button>
        </DialogActions>
    </Dialog>
}