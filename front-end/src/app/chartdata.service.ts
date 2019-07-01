import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChartdataService {

  private dataSource = new BehaviorSubject([0, 1, 3, 5, 1, 0, 4, 2, 2, 1]);
  currentData = this.dataSource.asObservable();

  constructor() { }

  changeData(chartData: Array<number>){
    this.dataSource.next(chartData);
  }
}
