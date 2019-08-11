import React from 'react'
import { Link } from 'gatsby'

export default function PostLink({ post }) {
    return (
        <div>
            <div style={{ display: `flex`, justifyContent: `space-between`, alignItems: `flex-end`, marginBottom: `1.45rem`, borderBottom: `solid 1px #ddd` }}>
                <Link class="title" style={{ textDecoration: `none`, fontSize: `1.5rem` }} to={post.frontmatter.path}>
                    {post.frontmatter.title}
                </Link>
                <small><em>{post.frontmatter.date}</em></small>
            </div>
            <div>
                {post.excerpt}
            </div>
        </div>
    )
}