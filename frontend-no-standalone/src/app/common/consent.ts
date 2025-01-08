import { Teacher } from "./teacher";

export class Consent {
    id: number;
    title: string;
    description: string;
    endDate: Date;
    author: Teacher;
    parentSubmission: boolean;

    constructor(
        id: number,
        title: string,
        description: string,
        endDate: Date,
        author: Teacher,
        parentSubmission: boolean
    ) {
        this.id = id;
        this.title = title;
        this.description = description;
        this.endDate = endDate;
        this.author = author;
        this.parentSubmission = parentSubmission;
    }

    static fromApiResponse(response: any): Consent {
        return new Consent(
            response.id,
            response.title,
            response.description,
            new Date(response.end_date),
            Teacher.fromApiResponse(response.author),
            response.parent_submission
        );
    }
}