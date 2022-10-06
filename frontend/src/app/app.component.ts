import { Component } from '@angular/core';
import { FormService } from './form/form.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'frontend';
  pizzas: Array<any>;

  constructor(
    public service: FormService
  ) {
    this.pizzas = []
  }

  ngOnInit() {
    setInterval(() => {
      this.service.getAll().then(r => {this.pizzas = r})
    }, 3000);
  }
}
