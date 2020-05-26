import React from "react";
import {Link} from 'react-router-dom';

export default function BreadCrumb({links}) {
    return <ul className="bread-crumb">
        {links.map((link) => {
            return <li key={link.to} className="bread-crumb-list-item">
                <Link to={link.to}>{link.label} </Link> /
            </li>
        })}
    </ul>
}