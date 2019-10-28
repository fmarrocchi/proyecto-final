import { Component, OnInit, OnDestroy } from '@angular/core';
import { TrendsService, TrendsResponse } from '../services/trends.service';
import { ToastrService } from 'ngx-toastr';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-trends',
  templateUrl: './trends.component.html',
  styleUrls: ['./trends.component.css']
})
export class TrendsComponent implements OnInit, OnDestroy {

  public trends:Array<string> = ["#Topic", "#Topic", "#Topic", "#Topic", "#Topic"];
  error: any;
  subscriptions: Subscription;

  constructor(private trendsService:TrendsService, private toastr: ToastrService){
    this.subscriptions = new Subscription();
  }

  ngOnInit() {
    this.subscriptions.add(this.trendsService.getTrends().subscribe((data:TrendsResponse) => {
      this.trends = data.trending_topics;
    },
    error => this.toastr.error("Ha ocurrido un error. Por favor recargue la pagina.", "Error")));
  }

  ngOnDestroy(){
    this.subscriptions.unsubscribe();
  }

}
