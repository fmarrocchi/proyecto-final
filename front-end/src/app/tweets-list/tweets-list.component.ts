import { Component, OnInit } from '@angular/core';
import { TweetsListService } from '../tweets-list.service';
import { EmotionDic } from '../emotions.service';

@Component({
  selector: 'app-tweets-list',
  templateUrl: './tweets-list.component.html',
  styleUrls: ['./tweets-list.component.css']
})


export class TweetsListComponent implements OnInit {
  //valores para el texto de los tweets
  readonly colores = {
    "Positive": 'black',
    "Negative": 'black',
    "Anger": 'red',
    "Anticipation": 'orange',
    "Disgust": 'fuchsia',
    "Fear": 'green',
    "Joy": 'yellow',
    "Sadness": 'blue',
    "Surprise": 'aqua',
    "Trust": 'lime',
    "Neutro": 'black'
  }

  public tweets: Array<string>;
  public emotions: Array<EmotionDic>;
  //arreglo que mantiene la emocion mas representativa de cada tweet
  public emo_col: Array<string>;

  constructor(private twList: TweetsListService) { }

  ngOnInit() {
    this.twList.currentTweets.subscribe(tweets => this.tweets = tweets);
    this.twList.currentEmotions.subscribe(emotions => {
      this.emotions = emotions;
      this.emo_col = new Array(this.emotions.length);
      for(var i=0; i<this.emotions.length; i++){   
        this.emo_col[i] = "Neutro";
        let cont = 0;     
        for(let e in this.emotions[i]){
          if(this.emotions[i][e] > cont){
            this.emo_col[i] = e;
            cont = this.emotions[i][e]
          }
        }
      }
    });    
  }

  getColor(indice){
    //retorna el color dependiendo de la emocion
    return this.colores[this.emo_col[indice]]
  }

}
