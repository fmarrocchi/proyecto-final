import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-trends',
  templateUrl: './trends.component.html',
  styleUrls: ['./trends.component.css']
})
export class TrendsComponent implements OnInit {

  trends: Array<string> = ["#Topic", "#Topic", "#Topic", "#Topic", "#Topic"]

  ngOnInit() {
  }

}
