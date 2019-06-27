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
  error: any;

  constructor(private emotionsService: EmotionsService) { }

  ngOnInit() {
    this.chart = new Chart("realtime", {
      type: 'bar',
      data: {
          labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
          datasets: [{
              label: '# of Votes',
              data: [12, 19, 3, 5, 2, 3],
              backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(255, 206, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)',
                  'rgba(153, 102, 255, 0.2)',
                  'rgba(255, 159, 64, 0.2)'
              ],
              borderColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                  'rgba(255, 159, 64, 1)'
              ],
              borderWidth: 1
          }]
      },
      options: {
          scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero: true
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
          emotions: data["emotions"]};
          //muestro respuesta por consola
          console.log(this.resp)
        },
        error => this.error = error
        );
    console.log(form.value)
  }

}
