/**
 * School model
 */
export default class School {
  /**
   * Unique identifier of the school.
   * Can be undefined if created in cache but not persisted in the backend.
   */
  id?: number

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

  constructor(name: string, description: string, link: string, id?: number) {
    this.id = id
    this.name = name
    this.description = description
    this.link = link
  }
}
