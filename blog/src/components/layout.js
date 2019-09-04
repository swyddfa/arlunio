/**
 * Layout component that queries for data
 * with Gatsby's useStaticQuery component
 *
 * See: https://www.gatsbyjs.org/docs/use-static-query/
 */

import Helmet from 'react-helmet'
import React from "react"
import PropTypes from "prop-types"
import { useStaticQuery, graphql } from "gatsby"

import Header from "./header"
import "./layout.css"

const Layout = ({ children }) => {
  const data = useStaticQuery(graphql`
    query SiteTitleQuery {
      site {
        siteMetadata {
          title
        }
      }
    }
  `)

  return (
    <>
      <Helmet>
         <link href="https://fonts.googleapis.com/css?family=Caveat|Open+Sans:300&display=swap" rel="stylesheet" />
      </Helmet>
      <Header siteTitle={data.site.siteMetadata.title} />
      <div className="site-content">
        <main style={{ padding: `1rem` }}>{children}</main>
        <footer
          style={{
            textAlign: `center`,
            color: `#aaa`
          }}>
          <small>
            © {new Date().getFullYear()} Swyddfa Developers, Built with {` `}
            <a href="https://www.gatsbyjs.org">Gatsby</a>
          </small>
        </footer>
      </div>
    </>
  )
}

Layout.propTypes = {
  children: PropTypes.node.isRequired,
}

export default Layout
