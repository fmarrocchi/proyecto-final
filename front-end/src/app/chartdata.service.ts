import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ChartdataService {

  private dataSource = new BehaviorSubject([0.1, 0.3, 0.1, 0.1, 0.2, 0.1, 0.2, 0.3, 0.001, 0.3]);
  currentData = this.dataSource.asObservable();

  constructor() { }

  changeData(chartData: Array<number>){
    this.dataSource.next(chartData);
  }
}
