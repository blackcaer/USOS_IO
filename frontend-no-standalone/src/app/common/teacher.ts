import { User } from "./user";

export class Teacher {
    constructor(
        public user_id: number,
        public user: User
      ) {}
    
      static fromApiResponse(response: any): Teacher {
        return new Teacher(
          response.user_id,
          User.fromApiResponse(response.user)
        );
      }
}
