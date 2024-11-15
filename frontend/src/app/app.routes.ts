import { Routes } from '@angular/router';
import { MainBlocksComponent } from './components/main-blocks/main-blocks.component';
import { ScheduleComponent } from './components/schedule/schedule.component';
import { StatisticsComponent } from './components/statistics/statistics.component';
import { GradesComponent } from './components/grades/grades.component';

export const routes: Routes = [
    {path: 'statistics', component: StatisticsComponent},
    {path: 'grades', component: GradesComponent},
    {path: 'schedule', component: ScheduleComponent},
    {path: 'main', component: MainBlocksComponent},
    {path: '', redirectTo: 'main', pathMatch: 'full'},
    {path: '**', redirectTo: 'main', pathMatch: 'full'}
];
