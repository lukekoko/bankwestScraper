import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of, Subject } from 'rxjs';
import { tap, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  constructor(private http: HttpClient) { }

  private transactionsUrl = 'http://127.0.0.1:8000';
  private data: any;

  getTransactions(): Observable<any> {
    return this.http.get<Observable<any>>(this.transactionsUrl + `/transactions/`)
    .pipe(map((response) => response), tap(data => this.data = data));
  }
}
