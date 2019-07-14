import { Component, OnInit } from '@angular/core';
import { ApiResponse, EmotionsService } from '../emotions.service';
import {NgForm} from '@angular/forms';
import { ChartdataService } from '../chartdata.service';
import { TweetsListService } from '../tweets-list.service';

@Component({
  selector: 'app-busqueda',
  templateUrl: './busqueda.component.html',
  styleUrls: ['./busqueda.component.css']
})
export class BusquedaComponent implements OnInit {
  public fecha_hasta = new Date().toISOString().substring(0,10);
  public key="";
  public keywords: Array<string>;
  public limite = 100; 
  public operacion = 0;
  public resp: ApiResponse;  
  error: any;
  public cdata: Array<number>;
  public tweets: Array<string>;
  public disable: number =0;
  

  constructor(private emotionsService: EmotionsService,
    private chartData: ChartdataService,
    private twList:TweetsListService) { }

  ngOnInit() {
    this.keywords = new Array();
    this.chartData.currentData.subscribe(chart => this.cdata = chart);
    this.twList.currentTweets.subscribe(tweets => this.tweets = tweets)
  }

onSubmit(form) { 
    var keywords:string = form.value.key;
    if (keywords !== ""){
      this.keywords.push(keywords)
    }
    var fecha:string = new Date(form.value.fecha_hasta).toISOString().substr(0,10);
    var cant:number = form.value.limite;
    var op:number = form.value.operacion;
    form.value.key = "";
    this.emotionsService.getEmotions(this.keywords, fecha, cant, op)
      .subscribe(
        (data:ApiResponse) => {
          this.resp = {
          tweets: data["tweets"],
          emotions: data["emotions"],
          average: data["porcentaje_total"]};
          //muestro respuesta por consola
          console.log(this.resp);
          this.updateChart();
          this.updateTweetsList();
        },
        error => this.error = error
        );    
  }

  updateChart(){    
    this.chartData.changeData(this.resp.average);
  }

  updateTweetsList(){
    this.twList.changeData(this.resp.tweets, this.resp.emotions)
  }

  agregarKeyword(){
    if(this.key !== "")
      this.disable = this.keywords.push(this.key);
    this.key="";
    console.log(this.keywords);
    
  }
  
}
