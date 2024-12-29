export class StudentGroup {
    constructor(
      public id: number,
      public name: string,
      public description: string,
      public level: number,
      public section: string,
      public students: number[]
    ) {}
  
    static fromApiResponse(response: any): StudentGroup {
      return new StudentGroup(
        response.id,
        response.name,
        response.description,
        response.level,
        response.section,
        response.students
      );
    }
  }
