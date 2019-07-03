import { TestBed } from '@angular/core/testing';

import { TweetsListService } from './tweets-list.service';

describe('TweetsListService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: TweetsListService = TestBed.get(TweetsListService);
    expect(service).toBeTruthy();
  });
});
