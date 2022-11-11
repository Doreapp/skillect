/**
 * API utilities
 */
import axios from "axios"
import {ISchool} from "../models/School"

const API_URL = `${process.env.REACT_APP_URL ?? "http://localhost"}/api/v1`

/**
 * API object, to make request on backend server
 */
export const api = {
  /**
   * Get all the schools
   */
  async getSchools(): Promise<ISchool[]> {
    const response = await axios.get<ISchool[]>(`${API_URL}/school/`)
    return response.data
  },
}
