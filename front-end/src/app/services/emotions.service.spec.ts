import { TestBed } from '@angular/core/testing';

import { EmotionsService } from './emotions.service';

describe('EmotionsService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: EmotionsService = TestBed.get(EmotionsService);
    expect(service).toBeTruthy();
  });
});
