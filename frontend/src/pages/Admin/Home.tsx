/**
 * Home admin page
 */

import {Container} from "@mui/material"
import * as React from "react"
import Page from "./Page"
import {UndrawUnderConstruction} from "../../components/illustrations"

/**
 * Home admin page
 * @returns
 */
export default function HomePage(): JSX.Element {
  return (
    <Page title="Home">
      <Container className="flex justify-center items-center h-full flex-col mt-1">
        <UndrawUnderConstruction className="w-1/2 h-1/2" />
        <h3>This page is under construction</h3>
      </Container>
    </Page>
  )
}
