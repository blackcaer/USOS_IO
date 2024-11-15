import { Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';
import { MainBlocksComponent } from "./components/main-blocks/main-blocks.component";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, MainBlocksComponent, RouterLink],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'USOS';
}
