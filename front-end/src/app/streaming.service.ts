import { Injectable } from '@angular/core';
import * as io from 'socket.io-client';
import { HttpClient, HttpParams, HttpErrorResponse} from '@angular/common/http';
import { Observable, throwError, Subject  } from 'rxjs';
import * as socketIo from 'socket.io-client';
import { Message } from '@angular/compiler/src/i18n/i18n_ast';

export interface ApiResponse {
  streaming_tweets: Array<string>
}

@Injectable()
export class StreamingService {
    private socket;

    public initSocket(): void {
        this.socket = socketIo('http://127.0.0.1:5000/emotions-analyzer/streaming');
    }

    public send(message: Message): void {
        this.socket.emit('message', message);
    }

    public onMessage(): Observable<Message> {
        return new Observable<Message>(observer => {
            this.socket.on('message', (data: Message) => observer.next(data));
        });
    }
  }