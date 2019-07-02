import { Component, OnInit } from '@angular/core';
import { ApiResponse, EmotionsService } from '../emotions.service';
import {NgForm} from '@angular/forms';
import { Chart } from 'chart.js';

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
  public chart: any = null;
  public datos:any = [];
  error: any;

  //inicializo datos del grafico
  public chartData = [{
    label: 'Promedio emociones',
    data: [0,0,0,0,0,0,0,0,0,0],
    backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)'
    ],
    borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)'
    ],
    borderWidth: 1
  }];

  constructor(private emotionsService: EmotionsService) { }

  ngOnInit() {
    this.chart = new Chart("realtime", {
      type: 'bar',
      data: {
        labels: ['Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Negative', 'Positive', 'Sadness', 'Surprise', 'Trust'],
        datasets: this.chartData,
      } ,
      options: {
          scales: {
              yAxes: [{

                  ticks: {
                      beginAtZero: true,
                      fixedStepSize: 0.2
                  }
              }]
          }
      }

   });
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
          porcentaje_total : data["porcentaje_total"]},
          this.datos = data["porcentaje_total"],
          //muestro respuesta por consola
          console.log(this.resp)
        },
        error => this.error = error
        );
    
    console.log("Datos.......");
    console.log(this.datos); 
    
    console.log("----- chart data antes ------");
    console.log(this.chartData);

    this.chartData['data'] = this.datos; 
    console.log("----chart data ------");
    console.log(this.chartData);
    this.chart.data.datasets.pop(); //borro lo que habia antes
    this.chart.data.datasets.push(this.chartData); //inserto los unicos datos
    this.chart.update();

    
  }

  updateConfigByMutating(chart) {
    chart.options.title.text = 'new title';
    chart.update();
  }


  
}
