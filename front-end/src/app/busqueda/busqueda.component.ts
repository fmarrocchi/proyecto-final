import { Component, OnInit } from '@angular/core';
import { ApiResponse, EmotionsService } from '../emotions.service';
import {NgForm} from '@angular/forms';

@Component({
  selector: 'app-busqueda',
  templateUrl: './busqueda.component.html',
  styleUrls: ['./busqueda.component.css']
})
export class BusquedaComponent implements OnInit {
  public hashtags="";
  public fecha_hasta = new Date().toISOString().substring(0,10); 
  public resp: ApiResponse;
  error: any;

  constructor(private emotionsService: EmotionsService) { }

  ngOnInit() {
  }

  onSubmit(form) { 
    var keywords:string = form.value.keywords;
    var fecha:string = new Date(form.value.fecha_hasta).toISOString().substr(0,10);
    this.emotionsService.getEmotions(keywords, fecha)
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
