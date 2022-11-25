/**
 * API utilities
 */
import axios from "axios"
import {ISchool} from "../models/School"
import {IUser} from "../models/User"

const API_URL = `${process.env.REACT_APP_URL ?? "http://localhost"}/api/v1`

/**
 * Authentication header with *Bearer* token
 * @param token Token to use
 * @returns headers object
 */
function authHeaders(token: string): {} {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }
}

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

  /**
   * Login as user
   * @param username User username
   * @param password User plain text password
   * @returns Access token or undefined
   */
  async logInGetToken(
    username: string,
    password: string
  ): Promise<string | undefined> {
    const params = new URLSearchParams()
    params.append("username", username)
    params.append("password", password)
    const response = await axios.post(`${API_URL}/login/access-token/`, params)
    return response.data.access_token
  },

  /**
   * Get current logged in user
   * @param token access token
   * @returns User model
   */
  async getMe(token: string): Promise<IUser | null> {
    const response = await axios.get<IUser | null>(
      `${API_URL}/users/me`,
      authHeaders(token)
    )
    return response.data
  },
}
