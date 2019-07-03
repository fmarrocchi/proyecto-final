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
    cdata: Array<number>;
  
  constructor(private chartData: ChartdataService) { }

  ngOnInit() {

       this.chart = new Chart("realtime", {
        type: 'radar',
        data: {
          labels: ['Positive', 'Negative', 'Anger', 'Anticipation', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Surprise', 'Trust'],
          datasets: [{
            label: "Porcentaje emociones",
            data: [1, 0.1, 0.3, 0.5, 0.1, 0.0, 0.4, 0.2, 0.2, 0.1],
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
                'rgba(75, 192, 192, 1)',
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
      }});

      this.chartData.currentData.subscribe(data => {
        this.cdata = data;
        this.updateChart()
      })
  }

  updateChart(){
      //Actualiza solo los valores de los datos
      this.chart.data.datasets[0]['data'] = this.cdata;
      this.chart.update()
  }
}
