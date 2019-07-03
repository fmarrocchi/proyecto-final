import { Component, OnInit } from '@angular/core';
import { TweetsListService } from '../tweets-list.service';

@Component({
  selector: 'app-tweets-list',
  templateUrl: './tweets-list.component.html',
  styleUrls: ['./tweets-list.component.css']
})
export class TweetsListComponent implements OnInit {

  //tweets:string[]=["hola","que","tal","estas"];
  public tweets: Array<string>;

  constructor(private twList: TweetsListService) { }

  ngOnInit() {
    this.twList.currentData.subscribe(tweets => this.tweets = tweets)
  }

}
