import { Component, OnInit } from '@angular/core';
import { Chart } from 'chart.js';
import { ChartdataService } from '../chartdata.service';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.css']
})
export class ChartComponent implements OnInit {

    public chart: any;
    cdata: Array<number>=[];

    public barChart: any;
    bardata: Array<number>=[];
  
  constructor(private chartData: ChartdataService) { }

  ngOnInit() {

      this.createRadarChart();
      this.createBarChart();

      this.chartData.currentData.subscribe(data => {
        //separo valores en dos arreglos segun cada grafico
        //los primeros dos valores son pos y neg para el grafico de barra
        this.bardata[0] = data[0];
        this.bardata[1] = data[1];

        //los valores restantes son las 8 emociones para el grafico de radar
        for (var i = 2; i < data.length; i++) {
          this.cdata[i-2] = data[i];
        }

        this.updateRadarChart(this.cdata);
        this.updateBarChart(this.bardata)
      });

  }

  createRadarChart(){
    this.chart = new Chart("realtime", {
      type: 'radar',
      data: {
        labels: ['Enojo', 'Anticipacion', 'Repugnancia', 'Miedo', 'Alegria', 'Tristeza', 'Sorpresa', 'Confianza'],
        datasets: [{
          //Enojo
          data: [0, 0, 0, 0, 0, 0, 0, 0],
          backgroundColor: [
            'rgba(231, 76, 60, 0.4)' 
          ],
          pointBackgroundColor: "transparent",
          pointBorderColor: "transparent",
          borderWidth: 1
          },
          {
            //Anticipacion
            data: [0, 0, 0, 0, 0, 0, 0, 0],
            backgroundColor: [
              'rgba(245, 127, 23, 0.4)'
            ],
            pointBackgroundColor: "transparent",
            pointBorderColor: "transparent",
            borderWidth: 1
          },
          {
            //Repugnancia
            data: [0, 0, 0, 0, 0, 0, 0, 0],
            backgroundColor: [
              'rgba(165, 105, 189, 0.4)'
            ],
            pointBackgroundColor: "transparent",
            pointBorderColor: "transparent",
            borderWidth: 1
          },  
          {
            //Miedo
            data: [0, 0, 0, 0, 0, 0, 0, 0],
            backgroundColor: [
              'rgba(34, 153, 84, 0.4)'
            ],
            pointBackgroundColor: "transparent",
            pointBorderColor: "transparent",
            borderWidth: 1
          },    
          {
            //Alegria
            data: [0, 0, 0, 0, 0, 0, 0, 0],
            backgroundColor: [
              'rgba(255, 234, 0, 0.4)'
            ],
            pointBackgroundColor: "transparent",
            pointBorderColor: "transparent",
            borderWidth: 1
          },
          {
            //Tristeza
            data: [0, 0, 0, 0, 0, 0, 0, 0],
            backgroundColor: [
              'rgba(101, 31, 255, 0.4)'    
            ],
            pointBackgroundColor: "transparent",
            pointBorderColor: "transparent",
            borderWidth: 1
          },
          {
            //Sorpresa
            data: [0, 0, 0, 0, 0, 0, 0, 0],
            backgroundColor: [
              'rgba(84, 153, 199, 0.4)'
            ],
            pointBackgroundColor: "transparent",
            pointBorderColor: "transparent",
            borderWidth: 1
          },
          {
            //Confianza
            data: [0, 0, 0, 0, 0, 0, 0, 0],
            backgroundColor: [
              'rgba(174, 234, 0, 0.4)'  
            ],
            pointBackgroundColor: "transparent",
            pointBorderColor: "transparent",
            borderWidth: 1
          }
        ]
        },
        options: {
          scale: {
            ticks: {
              min: -0.08
            }
          },
          legend: {
              display: false
          }
        }    
    });
  }

  createBarChart(){
      this.barChart = new Chart("horizontalBar", {
      type: 'horizontalBar',
      data: {
        labels: ['Positivo', 'Negativo'],
        datasets: [{
            data: [0,0],
            backgroundColor: [ 'rgba(197, 17, 98, 0.4)','rgba(38, 198, 218, 0.4)'],
            borderColor: ['rgba(197, 17, 98, 1)', 'rgba(38, 198, 218, 1)'],
            borderWidth: 0.5
        }]
      },
      options: {
        legend: {
            display: false
        },
        scales: {
          yAxes: [{
            barPercentage: 1,
            
          }],
          xAxes: [{
            ticks: {
              min: 0,
              max:5
            }
          }]
        }
      } 
    });
    }

  updateRadarChart(cdata){
      //Actualiza solo los valores de los datos
      for (var i = 0; i < cdata.length; i++) {
        this.chart.data.datasets[i]['data'][i] = cdata[i];        
      }
      this.chart.update()
  }

  updateBarChart(datosPieChart){
    //Actualiza solo los valores de los datos
    this.barChart.data.datasets[0]['data'] = datosPieChart;
    this.barChart.update()
  }
}
