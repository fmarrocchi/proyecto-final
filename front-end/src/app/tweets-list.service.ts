import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { EmotionDic } from './emotions.service';

@Injectable({
  providedIn: 'root'
})
export class TweetsListService {

  private tweetsSource = new BehaviorSubject([""]);
  private emotionsSource = new BehaviorSubject([]);
  currentTweets = this.tweetsSource.asObservable();
  currentEmotions = this.emotionsSource.asObservable();

  constructor() { }

  changeData(tweets: Array<string>, emotions: Array<EmotionDic>){
    this.tweetsSource.next(tweets);
    this.emotionsSource.next(emotions);
  }
}
