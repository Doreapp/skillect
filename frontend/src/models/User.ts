/**
 * User model
 */

/**
 * Base of user model
 */
export interface IUser {
  email: string
  is_active: boolean
  is_superuser: boolean
  full_name: string
  id: number
}

/**
 * User update
 */
export interface IUserUpdate {
  email?: string
  full_name?: string
  password?: string
  is_active?: boolean
  is_superuser?: boolean
}
