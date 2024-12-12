import { Component } from '@angular/core';

@Component({
  selector: 'app-main-blocks',
  templateUrl: './main-blocks.component.html',
  styleUrl: './main-blocks.component.css'
})
export class MainBlocksComponent {
  lastGrades = [
    { name: 'Matematyka', grade: -2 },
    { name: 'Informatyka', grade: 4 },
    { name: 'Angielski', grade: 4 },
    { name: 'Matematyka', grade: 1 },
    { name: 'Chemia', grade: 2 }
  ];
}
