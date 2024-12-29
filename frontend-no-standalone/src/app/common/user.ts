export class User {
    constructor(
      public id: number,
      public username: string,
      public firstName: string,
      public lastName: string,
      public email: string,
      public status: string,
      public birthDate: string,
      public sex: string,
      public phoneNumber: string,
      public photoUrl: string,
      public role: string
    ) {}
  
    static fromApiResponse(response: any): User {
      return new User(
        response.id,
        response.username,
        response.first_name,
        response.last_name,
        response.email,
        response.status,
        response.birth_date,
        response.sex,
        response.phone_number,
        response.photoГrl,
        response.role
      );
    }
  }
