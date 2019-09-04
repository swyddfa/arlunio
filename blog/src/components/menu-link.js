import React from 'react'
import { Link } from 'gatsby'

export default function MenuLink({ title, path }) {
    return (
        <div style={{ padding: `1rem` }}>
            <Link style={{ color: `white`, textDecoration: `none`, fontSize: `1.45rem` }}
                className="title" to={path}>
                {title}
            </Link>
        </div>
    )
}