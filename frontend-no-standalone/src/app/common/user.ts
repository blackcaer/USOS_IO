export class User {
    constructor(
      public id: number,
      public username: string,
      public first_name: string,
      public last_name: string,
      public email: string,
      public status: string,
      public birth_date: string,
      public sex: string,
      public phone_number: string,
      public photo_url: string,
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
        response.photo_url,
        response.role
      );
    }
  }
