/**
 * Home page
 */

import {Container} from "@mui/material"
import * as React from "react"
import {UndrawUnderConstruction} from "../components/illustrations"

/**
 * Home page
 * @returns
 */
export default function HomePage(): JSX.Element {
  return (
    <Container
      className="p-0 h-screen flex justify-center items-center flex-col"
      maxWidth={false}>
      <UndrawUnderConstruction className="w-1/2 h-1/2" />
      <h3>This page is under construction</h3>
    </Container>
  )
}
