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
    "Positive": 'rgba(197, 17, 98, 1)',
    "Negative": 'rgba(38, 198, 218, 1)',
    "Anger": 'rgba(231, 76, 60, 1)',
    "Anticipation": 'rgba(234, 156, 18, 1)',
    "Disgust": 'rgba(165, 105, 189, 1)',
    "Fear": 'rgba(34, 153, 84, 1)',
    "Joy": 'rgba(244, 208, 63, 1)',
    "Sadness": 'rgba(121, 134, 203, 1)',
    "Surprise": 'rgba(84, 153, 199, 1)',
    "Trust": 'rgba(46, 204, 113, 1)',
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
