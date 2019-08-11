import { Link } from "gatsby"
import PropTypes from "prop-types"
import React from "react"

import MenuLink from "./menu-link";

const Header = ({ siteTitle }) => (
  <header className="site-title">
    <div
      style={{
        margin: `0`,
        padding: `1.45rem 1.0875rem`,
      }}
    >
      <h1 style={{ margin: 0 }}>
        <Link
          to="/"
          style={{
            color: `white`,
            textDecoration: `none`,
          }}
        >
          {siteTitle}
        </Link>
      </h1>
    </div>
    <div>
      <MenuLink path="/blog" title="Blog" />
    </div>
  </header>
)

Header.propTypes = {
  siteTitle: PropTypes.string,
}

Header.defaultProps = {
  siteTitle: ``,
}

export default Header
