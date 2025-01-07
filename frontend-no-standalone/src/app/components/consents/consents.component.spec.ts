import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConsentsComponent } from './consents.component';

describe('ConsentsComponent', () => {
  let component: ConsentsComponent;
  let fixture: ComponentFixture<ConsentsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ConsentsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ConsentsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
