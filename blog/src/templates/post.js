import React from 'react'
import { graphql } from 'gatsby'

import Layout from "../components/layout"
import SEO from "../components/seo"

import "katex/dist/katex.min.css"

export default function Template({ data }) {
  const { markdownRemark } = data
  const { frontmatter, html } = markdownRemark

  return (
    <Layout>
      <SEO title={ frontmatter.title }/>
      <div className="blog-post">
        <h1 style={{ textAlign: `center`, marginBottom: `0` }}>{frontmatter.title}</h1>
        <h6 style={{ color: `#aaa`, textAlign: `center` }}>--{frontmatter.date} --</h6>

        <div className="blog-post-content" dangerouslySetInnerHTML={{ __html: html }} />
      </div>
    </Layout>
  )
}

export const paeQuery = graphql`
  query($path: String!) {
    markdownRemark(frontmatter: {path: {eq: $path} }) {
      html
      frontmatter {
        date(formatString: "MMMM DD, YYYY")
        path
        title
      }
    }
  }
`
