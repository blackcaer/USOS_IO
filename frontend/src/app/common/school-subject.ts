export class SchoolSubject {
    constructor(
        public id: number,
        public subjectName: string,
        public description: string,
        public isMandatory: boolean,
        public studentGroup: number
      ) {

      }
}
