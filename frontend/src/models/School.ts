/**
 * School model
 */

/**
 * Basic school attributes
 */
export interface ISchool {
  /**
   * Unique identifier of the school.
   */
  id: number

  /**
   * Name of the school. Shall be unique.
   */
  name: string

  /**
   * Long description of the school.
   */
  description: string

  /**
   * Web link (reference) to the school website.
   */
  link: string
}

/**
 * Attributes for a school update
 */
export interface ISchoolUpdate {
  name?: string
  description?: string
  link?: string
}

/**
 * Attributes for a school creation
 */
export interface ISchoolCreate {
  name: string
  description?: string
  link?: string
}
