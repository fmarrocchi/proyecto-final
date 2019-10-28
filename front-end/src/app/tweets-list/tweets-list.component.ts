import { Component, OnInit, OnDestroy } from '@angular/core';
import { TweetsListService } from '../services/tweets-list.service';
import { EmotionDic } from '../services/emotions.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-tweets-list',
  templateUrl: './tweets-list.component.html',
  styleUrls: ['./tweets-list.component.css']
})


export class TweetsListComponent implements OnInit, OnDestroy {
  //valores para el texto de los tweets
  readonly colores = {
    "Positive": 'rgba(197, 17, 98, 1)',
    "Negative": 'rgba(38, 198, 218, 1)',
    "Anger": 'rgba(231, 76, 60, 1)',
    "Anticipation": 'rgba(245, 127, 23, 1)',
    "Disgust": 'rgba(165, 105, 189, 1)',
    "Fear": 'rgba(34, 153, 84, 1)',
    "Joy": 'rgba(255, 234, 0, 1)',
    "Sadness": 'rgba(101, 31, 255, 1)',
    "Surprise": 'rgba(84, 153, 199, 1)',
    "Trust": 'rgba(174, 234, 0, 1)',
    "Neutro": 'black'
  }

  public tweets: Array<string>;
  public emotions: Array<EmotionDic>;
  //arreglo que mantiene la emocion mas representativa de cada tweet
  public emo_col: Array<string>;
  subscriptions: Subscription;

  constructor(private twList: TweetsListService) { 
    this.subscriptions = new Subscription();
  }

  ngOnInit() {
    this.subscriptions.add(this.twList.currentTweets.subscribe(tweets => this.tweets = tweets));
    this.subscriptions.add(this.twList.currentEmotions.subscribe(emotions => {
      this.emotions = emotions;
      this.emo_col = new Array(this.emotions.length);
      for(var i=0; i<this.emotions.length; i++){   
        this.emo_col[i] = "Neutro";
        let cont = 0;   
        for(let e in this.emotions[i]){
          if(e != 'Negative' && e != 'Positive' && this.emotions[i][e] > cont){ //Solo incluimos emociones de plutchik
            this.emo_col[i] = e;
            cont = this.emotions[i][e]
          }
        }
      }
    }));    
  }

  ngOnDestroy(){
    this.subscriptions.unsubscribe();
  }

  getColor(indice){
    //retorna el color dependiendo de la emocion
    return this.colores[this.emo_col[indice]]
  }

}
