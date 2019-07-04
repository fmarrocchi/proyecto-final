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

        console.log("---datos pos y neg....");
        console.log(this.bardata);
        console.log("---datos emociones....");
        console.log(this.cdata);

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
          label: "Porcentaje emociones",
          data: [1, 1, 3, 5, 1, 0, 4, 2],
          backgroundColor: [
            'rgba(231, 76, 60, 0.2)', //enojo
            'rgba(234, 156, 18, 0.2)', //anticipacion
            'rgba(165, 105, 189, 0.2)', //repugnancia
            'rgba(34, 153, 84, 0.2)', //miedo
            'rgba(244, 208, 63, 0.2)', //alegria
            'rgba(121, 134, 203, 0.2)', //tristeza  
            'rgba(84, 153, 199, 0.2)', //sorpresa
            'rgba(46, 204, 113, 0.2)'  //confianza
          ],
          borderColor: [
              'rgba(231, 76, 60, 1)', //enojo
              'rgba(234, 156, 18, 1)', //anticipacion
              'rgba(165, 105, 189, 1)', //repugnancia
              'rgba(34, 153, 84, 1)',  //miedo
              'rgba(244, 208, 63, 1)', //alegria
              'rgba(121, 134, 203, 1)', //tristeza 
              'rgba(84, 153, 199, 1)', //sorpresa
              'rgba(46, 204, 113, 1)' //confianza
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
  }

  createBarChart(){
      this.barChart = new Chart("horizontalBar", {
      type: 'horizontalBar',
      data: {
        labels: ['Positivo', 'Negativo'],
        datasets: [{
            data: [1,5],
            label: "Polaridad tweets",
            backgroundColor: [ 'rgba(197, 17, 98, 0.2)','rgba(38, 198, 218, 0.2)'],
            borderColor: ['rgba(197, 17, 98, 1)', 'rgba(38, 198, 218, 1)'],
            borderWidth: 1
            }]
      }
    });
    }

  updateRadarChart(cdata){
      //Actualiza solo los valores de los datos
      this.chart.data.datasets[0]['data'] = cdata;
      this.chart.update()
  }

  updateBarChart(datosPieChart){
    //Actualiza solo los valores de los datos
    this.barChart.data.datasets[0]['data'] = datosPieChart;
    this.barChart.update()
  }
}
