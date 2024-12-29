import { getSubjectResponse } from "../services/user.service";
import { StudentGroup } from "./student-group";

export class SchoolSubject {
    constructor(
        public id: number,
        public subjectName: string,
        public description: string,
        public isMandatory: boolean,
        public studentGroup: StudentGroup
    ) {

    }

    static fromApiResponse(response: getSubjectResponse): SchoolSubject {
      return new SchoolSubject(
        response.id,
        response.subject_name,
        response.description,
        response.is_mandatory,
        StudentGroup.fromApiResponse(response.student_group)
      );
    }
}
