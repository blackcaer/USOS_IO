import { User } from "./user";

export class Parent {
    userId: number;
    user: User;
    children: number[];
  
    constructor(userId: number, user: User, children: number[]) {
      this.userId = userId;
      this.user = user;
      this.children = children;
    }

    static fromApiResponse(response: any): Parent {
        return new Parent(
          response.user_id,
          User.fromApiResponse(response.user),
          response.children
        );
      }
}
