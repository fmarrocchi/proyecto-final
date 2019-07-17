import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpErrorResponse} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
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
    console.log(params.toString())
    return this.http.get<ApiResponse>("http://127.0.0.1:5000/emotions-analyzer",{params})
  }

  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error.message);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong,
      
      console.error(
        `Backend returned code ${error.status}, ` +
        `body was: ${error.error}`);
    }
    // return an observable with a user-facing error message
    return throwError(
      'Something bad happened; please try again later.');
  };
}
