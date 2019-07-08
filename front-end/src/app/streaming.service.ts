import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import io from 'socket.io-client';

export interface StreamResponse {
  stream_tweet: string
}


@Injectable({ 
    providedIn: 'root'
})
export class StreamingService {
    private socket;
    private count: number;

    constructor() {
        this.count =0;
     }
    public initSocket(): void {
        this.socket = io('http://127.0.0.1:5000/emotions-analyzer/streaming')
    }

    public send(keyword: string, limit: number ): void {
        var data = {
            'keywords': keyword,
            'limit': limit
        }
        //this.socket.emit('stream', keyword);
        this.socket.emit('stream', data);
    }
    //observer.next(data)
    public onMessage(): Observable<StreamResponse> {
        return new Observable<StreamResponse>(observer => {
            this.socket.on('streamresponse', (data: StreamResponse) => 
            {this.count = this.count+1; 
                console.log(this.count);
                observer.next(data)});
        });
    }
}