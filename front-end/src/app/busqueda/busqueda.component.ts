import { Component, OnInit } from '@angular/core';
import {NgForm} from '@angular/forms';

@Component({
  selector: 'app-busqueda',
  templateUrl: './busqueda.component.html',
  styleUrls: ['./busqueda.component.css']
})
export class BusquedaComponent implements OnInit {
  public hashtag="";
  public listaHashtags: string[] = [];
 
  constructor() { }

  ngOnInit() {
  }

  addHashtag(){
    //La lista habria q vaciarla luego de llamar a la funcion
    this.listaHashtags.push(this.hashtag)
    this.hashtag=""
    alert('elemento agregado a la lista: '+ this.listaHashtags)
  }

  getListaHashtags(){
    return this.listaHashtags;
  }

  onSubmit() {
    alert('Hashtag agregado !')
  }

  setHashtags(hashtag){
    this.hashtags = hashtag;
  }

  getHashtags(){
    return this.hashtags;
  }

}