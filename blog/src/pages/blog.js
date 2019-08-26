import React from 'react'
import { graphql } from 'gatsby'

import PostLink from '../components/post-link'
import Layout from "../components/layout"
import SEO from "../components/seo"

export default function BlogIndex({ data: { allMarkdownRemark: { edges }, }, }) {

  const Posts = edges
    .map(edge => <PostLink key={edge.node.id} post={edge.node} />);

  return (
    <Layout>
      <SEO title="Development Blog" />
      <h1>Development Blog</h1>
      <div>{Posts}</div>
    </Layout >
  )
}

export const pageQuery = graphql`
  query {
    allMarkdownRemark(sort: {order: DESC, fields: [frontmatter___date]}) {
      edges {
        node {
          id
          excerpt(pruneLength: 250)
          frontmatter {
            date(formatString: "MMMM DD, YYYY")
            path
            title
          }
        }
      }
    }
  }
`
