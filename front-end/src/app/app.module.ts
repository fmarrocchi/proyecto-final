import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ToastrModule } from 'ngx-toastr';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BusquedaComponent } from './busqueda/busqueda.component';
import { HttpClientModule }    from '@angular/common/http';
import { ChartComponent } from './chart/chart.component';
import { TweetsListComponent } from './tweets-list/tweets-list.component';
import { TrendsComponent } from './trends/trends.component';

import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import { HelpComponent } from './help/help.component';


@NgModule({
  declarations: [
    AppComponent,
    BusquedaComponent,
    ChartComponent,
    TweetsListComponent,
    TrendsComponent,
    HelpComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    ToastrModule.forRoot(),
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    NgbModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
