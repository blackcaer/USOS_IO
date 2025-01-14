import { getGradeColumnResponse } from "../services/meeting.service";
import { SchoolSubject } from "./school-subject";

export class GradeColumn {
  id: number;
  title: string;
  weight: number;
  description: string;
  school_subject: number;

  constructor(id: number, title: string, weight: number, description: string, schoolSubject: number) {
    this.id = id;
    this.title = title;
    this.weight = weight;
    this.description = description;
    this.school_subject = schoolSubject;
  }

  static fromApiResponse(response: getGradeColumnResponse): GradeColumn {
    return new GradeColumn(
        response.id,
        response.title,
        response.weight,
        response.description,
        response.school_subject
    );
  }
}
