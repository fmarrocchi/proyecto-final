import { Component, OnInit } from '@angular/core';
import { TrendsService, TrendsResponse } from '../trends.service';

@Component({
  selector: 'app-trends',
  templateUrl: './trends.component.html',
  styleUrls: ['./trends.component.css']
})
export class TrendsComponent implements OnInit {

  public trends:Array<string> = ["#Topic", "#Topic", "#Topic", "#Topic", "#Topic"];
  error: any;
  //

  constructor(private trendsService:TrendsService){}

  ngOnInit() {
    this.trendsService.getTrends().subscribe((data:TrendsResponse) => {
      this.trends = data.trending_topics;
    },
    error => this.error = error)
  }

}
