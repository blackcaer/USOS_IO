import { User } from "./user";

export class Student {
    constructor(public userId: number,
                public user: User,
                public parents: number[]
    ) {

    }

    static fromApiResponse(response: any): Student {
        return new Student(
          response.user_id,
          User.fromApiResponse(response.user),
          response.parents
        );
      }
}
