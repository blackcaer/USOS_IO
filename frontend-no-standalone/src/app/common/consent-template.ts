import { Consent } from "./consent";
import { ParentConsent } from "./parent-consent";
import { Teacher } from "./teacher";

export class ConsentTemplate {
    id: number;
    title: string;
    description: string;
    endDate: Date;
    students: number[];
    parentConsents: ParentConsent[];
    author: Teacher;
    parentSubmission: boolean | null;

    constructor(
        id: number,
        title: string,
        description: string,
        endDate: Date,
        students: number[],
        parentConsents: ParentConsent[],
        author: Teacher,
        parentSubmission: boolean
    ) {
        this.id = id;
        this.title = title;
        this.description = description;
        this.endDate = endDate;
        this.students = students;
        this.parentConsents = parentConsents;
        this.author = author;
        this.parentSubmission = parentSubmission;
    }

    static fromApiResponse(response: any): ConsentTemplate {
        return new ConsentTemplate(
            response.id,
            response.title,
            response.description,
            new Date(response.end_date),
            response.students,
            response.parent_consents.map((consent: any) => ParentConsent.fromApiResponse(consent)),
            Teacher.fromApiResponse(response.author),
            response.parent_submission
        );
    }
}
