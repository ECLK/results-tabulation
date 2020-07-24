import React from "react";
import {Link} from 'react-router-dom';

export default function BreadCrumb({links}) {
    return <ul className="bread-crumb">
        {links.map((link, linkIndex) => {
            return <li key={linkIndex} className="bread-crumb-list-item">
                <Link to={link.to}>{link.label} </Link> /
            </li>
        })}
    </ul>
}