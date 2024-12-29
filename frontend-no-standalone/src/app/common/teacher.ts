import { User } from "./user";

export class Teacher {
    constructor(
        public userId: number,
        public user: User
      ) {}
    
      static fromApiResponse(response: any): Teacher {
        return new Teacher(
          response.user_id,
          User.fromApiResponse(response.user)
        );
      }
}
