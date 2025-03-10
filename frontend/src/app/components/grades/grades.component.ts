import { NgFor } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-grades',
  standalone: true,
  imports: [NgFor],
  templateUrl: './grades.component.html',
  styleUrl: './grades.component.css'
})
export class GradesComponent {
  subjects = [
    { name: 'Biologia', grades: [-4, 3, -2, -5] },
    { name: 'Matematyka', grades: [3, 1, -2] },
    { name: 'Informatyka', grades: [-4, 3, -2, -5, 4] },
    { name: 'Historia', grades: [-5, 3] },
    { name: 'Wychowanie Fizyczne', grades: [-5, 4, 2, 4, 5] },
    { name: 'Angielski', grades: [-3, 3, 2, 4, 4] },
    { name: 'Chemia', grades: [2, 2, 2 ,2] }
  ];


}
