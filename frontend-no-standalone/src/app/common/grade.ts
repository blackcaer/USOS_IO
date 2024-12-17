export class Grade {
    id: number;
    value: number;
    weight: number;
    timestamp: Date;
    student: number;
    gradeColumn: number;
    countToAvg: boolean;
  
    constructor(
      id: number,
      value: number,
      weight: number,
      timestamp: string | Date,
      student: number,
      gradeColumn: number,
      countToAvg: boolean
    ) {
      this.id = id;
      this.value = value;
      this.weight = weight;
      this.timestamp = typeof timestamp === 'string' ? new Date(timestamp) : timestamp;
      this.student = student;
      this.gradeColumn = gradeColumn;
      this.countToAvg = countToAvg;
    }
  }