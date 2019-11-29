import React, {Component} from 'react'
import AppBar from '@material-ui/core/AppBar'
import Toolbar from '@material-ui/core/Toolbar'
import Button from '@material-ui/core/Button'
import Typography from '@material-ui/core/Typography'
import IconButton from '@material-ui/core/IconButton'
import './Navbar.css';
import {withRouter} from 'react-router-dom';
import AccountCircle from '@material-ui/icons/AccountCircle';
import ExitToAppIcon from '@material-ui/icons/ExitToApp';
import * as auth from "../../auth";
import {getUserName} from "../../auth";

class NavBar extends Component {
    constructor(props, context) {
        super(props, context);
        this.handleClickOpenDataEntry = this.handleClickOpenDataEntry.bind(this);
        this.handleClickOpenReports = this.handleClickOpenReports.bind(this);
        this.logout = this.logout.bind(this);
        this.username = getUserName()
    }

    handleClickOpenDataEntry() {
        this.props.history.replace('/Home')
    }

    handleClickOpenReports() {
        this.props.history.replace('/ReportsEntry')
    }

    logout() {
        auth.logout()
    }

    render() {
        return (
            <div>
                <AppBar position="fixed" style={{backgroundColor: '#5079c8'}}>
                    <Toolbar>
                        <Typography style={{paddingLeft: '1.5%', flexGrow: 1}} variant="h6" gutterBottom>
                            Election Result Tabulation
                        </Typography>
                        {/*<Typography variant="title" color='#4879d1'>*/}
                        {/*Election Result Tabulation*/}
                        {/*</Typography>*/}

                        <Typography variant="h6" gutterBottom>
                            |
                        </Typography>
                        <Button
                            color="inherit">
                            <AccountCircle style={{marginRight: '5px'}}/>
                            {this.username}
                        </Button>
                        <Button
                            onClick={this.logout}
                            color="inherit">
                            <ExitToAppIcon style={{marginRight: '5px'}}/> Logout
                        </Button>

                    </Toolbar>
                </AppBar>
                {this.renderMenu}
                {/*<div id="main_nav">*/}
                {/*<ul>*/}

                {/*<li>*/}
                {/*<a href="">Election Commission</a>*/}
                {/*<ul>*/}
                {/*<li><a href="">Ratites</a></li>*/}
                {/*<li><a href="">Fowl</a></li>*/}
                {/*<li><a href="">Neoaves</a></li>*/}
                {/*</ul>*/}
                {/*</li>*/}
                {/*<li>*/}
                {/*<a href="">District Result Centre</a>*/}
                {/*<ul>*/}
                {/*<li>*/}
                {/*<a href="">Data Entry</a>*/}
                {/*<ul>*/}
                {/*<li><a href="/issuing">Issuing</a></li>*/}
                {/*<li><a href="">Receiving</a></li>*/}
                {/*</ul>*/}
                {/*</li>*/}
                {/*<li>*/}
                {/*<a href="">Reports</a>*/}
                {/*<ul>*/}
                {/*<li><a href="">PRE-30-PD</a></li>*/}
                {/*<li><a href="">PRE-30-PV</a></li>*/}
                {/*</ul>*/}
                {/*</li>*/}
                {/*</ul>*/}
                {/*</li>*/}
                {/*<li>*/}
                {/*<a href="">Counting Centre</a>*/}
                {/*<ul>*/}
                {/*<li>*/}
                {/*<a href="">Data Entry</a>*/}
                {/*<ul>*/}
                {/*<li>*/}
                {/*<a href="">Votes</a>*/}
                {/*<ul>*/}
                {/*<li><a href="/PRE28">PRE-28</a></li>*/}
                {/*<li><a href="/PRE28A">PRE-28A</a></li>*/}
                {/*<li><a href="/CE201">CE-201</a></li>*/}
                {/*<li><a href="/PRE41">PRE-41</a></li>*/}
                {/*<li><a href="/PRE21">PRE-21</a></li>*/}
                {/*<li><a href="/PRE34CO">PRE-34-CO</a></li>*/}
                {/*</ul>*/}
                {/*</li>*/}
                {/*<li>*/}
                {/*<a href="">Postal Votes</a>*/}
                {/*<ul>*/}
                {/*<li><a href="/PRE21PV">PRE-21 PV</a></li>*/}
                {/*<li><a href="/PRE41PV">PRE-41 PV</a></li>*/}
                {/*<li><a href="/PRE34COPV">PRE-34-CO PV</a></li>*/}
                {/*</ul>*/}
                {/*</li>*/}
                {/*</ul>*/}
                {/*</li>*/}

                {/*<li>*/}
                {/*<a href="">Reports</a>*/}
                {/*<ul>*/}
                {/*<li><a href="/ReportsEntry">Report</a></li>*/}
                {/*</ul>*/}
                {/*</li>*/}

                {/*</ul>*/}
                {/*</li>*/}

                {/*</ul>*/}
                {/*</div>*/}

            </div>

        )
    }
}

export default withRouter(NavBar);
