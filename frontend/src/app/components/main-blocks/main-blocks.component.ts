import { NgFor } from '@angular/common';
import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-main-blocks',
  standalone: true,
  imports: [RouterLink, NgFor],
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
