import { Component, OnInit } from '@angular/core';
import { ApiResponse, EmotionsService } from '../emotions.service';
import{ StreamingService} from '../streaming.service';
import {NgForm} from '@angular/forms';
import { ChartdataService } from '../chartdata.service';
import { Message } from '@angular/compiler/src/i18n/i18n_ast';

@Component({
  selector: 'app-busqueda',
  templateUrl: './busqueda.component.html',
  styleUrls: ['./busqueda.component.css']
})
export class BusquedaComponent implements OnInit {
  public hashtags="";
  public fecha_hasta = new Date().toISOString().substring(0,10);
  public limite = 100; 
  public resp: ApiResponse;  
  error: any;
  public cdata: Array<number>;
  public tweets: any;
  

  constructor(private emotionsService: EmotionsService,
    private chartData: ChartdataService, 
    private streamingService: StreamingService) { }

  ngOnInit() {
    this.chartData.currentData.subscribe(chart => this.cdata = chart)
  }

onSubmit(form) { 
    var keywords:string = form.value.keywords;
    var fecha:string = new Date(form.value.fecha_hasta).toISOString().substr(0,10);
    var cant:number = form.value.limite;
    this.emotionsService.getEmotions(keywords, fecha, cant)
      .subscribe(
        (data:ApiResponse) => {
          this.resp = {
          tweets: data["tweets"],
          emotions: data["emotions"],
          average: data["porcentaje_total"]};
          //muestro respuesta por consola
          console.log(this.resp);
          this.chartData.changeData(this.resp.average);
         
        },
        error => this.error = error
        ); 
    this.streamingService.initSocket();
    this.streamingService.onMessage().subscribe((message:Message) =>
    {
      console.log("Mensaje...");
      console.log(message)
    } );
  }
}