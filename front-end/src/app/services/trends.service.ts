import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

export interface TrendsResponse {
  trending_topics:Array<string>
}
@Injectable({
  providedIn: 'root'
})
export class TrendsService {

  constructor(private http: HttpClient) { }

  getTrends():Observable<TrendsResponse>{
    return this.http.get<TrendsResponse>("http://127.0.0.1:5000/emotions-analyzer/trends");

  }
}
