/**
 * School model
 */
export default class School {
  id?: number
  name: string
  description: string
  link: string

  constructor(name: string, description: string, link: string, id?: number) {
    this.id = id
    this.name = name
    this.description = description
    this.link = link
  }
}
