import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TweetsListService {

  private dataSource = new BehaviorSubject([""]);
  currentData = this.dataSource.asObservable();

  constructor() { }

  changeData(tweets: Array<string>){
    this.dataSource.next(tweets);
  }
}
