import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ToastrService } from 'ngx-toastr';

export interface ApiResponse {
  tweets: Array<string>;
  emotions: Array<EmotionDic>;
  average: Array<number>
}
export interface EmotionDic {
  Positive: number;
  Negative: number;
  Anger: number;
  Anticipation: number;
  Disgust: number;
  Fear: number;
  Joy: number;
  Sadness: number;
  Surprise: number;
  Trust: number
}

@Injectable({ 
  providedIn: 'root'
})
export class EmotionsService {

  constructor(private http: HttpClient,
    private toastr: ToastrService) { }

  //fecha es un string con el formato YYYY-MM-DD
  //keywords es un string con la palabra clave a buscar
  getEmotions(keywords: Array<string>, fecha: string, cant_tweets: number, operacion: number): Observable<ApiResponse>{
    var params = new HttpParams().set('until-date',fecha).set('limit','50').set('limit',cant_tweets.toString()).set('operation',operacion.toString());
    keywords.forEach(key => {
      params = params.append("keywords", key)
    })
    return this.http.get<ApiResponse>("http://127.0.0.1:5000/emotions-analyzer",{params})
  }
}
