import { Component, OnInit } from '@angular/core';
import { ApiResponse, EmotionsService } from '../emotions.service';
import {NgForm} from '@angular/forms';

import { ToastrService } from 'ngx-toastr';
import { ChartdataService } from '../chartdata.service';
import { TweetsListService } from '../tweets-list.service';
import { NgbDate, NgbCalendar, NgbDateParserFormatter } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-busqueda',
  templateUrl: './busqueda.component.html',
  styleUrls: ['./busqueda.component.css']
})
export class BusquedaComponent implements OnInit {
  readonly mensaje_info = "No se obtuvieron resultados. Verifique que su busqueda sea correcta o espere 15 minutos y vuelva a intentarlo";
  readonly titulo_info = "Atención";
  public fecha_hasta: NgbDate ;
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
    private twList:TweetsListService,
    private ngbcal: NgbCalendar,
    private parserFormatter: NgbDateParserFormatter,
    private toastr: ToastrService) { }

  ngOnInit() {
    this.keywords = new Array();
    this.fecha_hasta = this.ngbcal.getToday();
    this.chartData.currentData.subscribe(chart => this.cdata = chart);
    this.twList.currentTweets.subscribe(tweets => this.tweets = tweets)
  }

onSubmit(form) { 
    var keywords:string = form.value.key;
    if (keywords !== ""){
      this.keywords.push(keywords)
    }
    var fecha: NgbDate = form.value.fecha_hasta;
    var cant:number = form.value.limite;
    var op:number = form.value.operacion;
    form.value.key = "";
    this.emotionsService.getEmotions(this.keywords, this.parserFormatter.format(fecha), cant, op)
      .subscribe(
        (data:ApiResponse) => {
          this.resp = {
          tweets: data["tweets"],
          emotions: data["emotions"],
          average: data["porcentaje_total"]};
          //muestro respuesta por consola
          console.log(this.resp);
          if(this.resp.tweets.length == 0)
            this.toastr.info(this.mensaje_info, this.titulo_info);
          else 
            this.updateChart();
          
          this.updateTweetsList();
        },
        error => this.toastr.error("Revise su consulta o intentelo de nuevo en unos minutos", "Error")
      );    
    this.keywords = new Array();
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
    
  }
  eliminarKey(indice){
    console.log(indice);
    this.keywords.splice(indice,1);
    console.log(this.keywords)
  }
  
}
