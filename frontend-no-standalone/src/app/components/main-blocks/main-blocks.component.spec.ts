import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MainBlocksComponent } from './main-blocks.component';

describe('MainBlocksComponent', () => {
  let component: MainBlocksComponent;
  let fixture: ComponentFixture<MainBlocksComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MainBlocksComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MainBlocksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
