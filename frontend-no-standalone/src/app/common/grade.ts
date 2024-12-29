import { getGradeResponse } from "../services/user.service";

export class Grade {
    id: number;
    value: string;
    timestamp: Date;
    student: number;
    gradeColumn: number;
    countToAvg: boolean;
  
    constructor(
      id: number,
      value: string,
      timestamp: string | Date,
      student: number,
      gradeColumn: number,
      countToAvg: boolean
    ) {
      this.id = id;
      this.value = value;
      this.timestamp = typeof timestamp === 'string' ? new Date(timestamp) : timestamp;
      this.student = student;
      this.gradeColumn = gradeColumn;
      this.countToAvg = countToAvg;
    }

    static fromApiResponse(response: getGradeResponse): Grade {
      return new Grade(
        response.id,
        response.value,
        response.timestamp,
        response.student,
        response.grade_column,
        response.count_to_avg
      );
    } 
  }