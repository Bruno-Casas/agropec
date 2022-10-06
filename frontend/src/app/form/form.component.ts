import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { Earring } from '../model/Earring';
import { Bovine } from '../model/Bovine';
import { FormService } from './form.service';

declare global {
  interface Window { pywebview: any; }
}

type Message = {
  message: string;
};

@Component({
  selector: 'app-form',
  templateUrl: './form.component.html',
  styleUrls: ['./form.component.scss']
})
export class FormComponent {

  bovineRegForm = this.formBuilder.group({
    earringIdentifier: '',
    earringColor: null,
    sex: null,
    category: null,
    weight: null
  });

  constructor(
    private formBuilder: FormBuilder,
    private service: FormService
  ) {}


  onSubmit(): void {
    const data = this.bovineRegForm.value;

    const bovine = new Bovine();
    const earring = new Earring();

    earring.value = data.earringIdentifier;
    earring.color = data.earringColor;

    bovine.category = data.category;
    bovine.sex = data.sex;
    bovine.weight = data.weight;
    bovine.earring = earring;

    this.service.saveBovine(bovine)
  }

  onClick() {
    if (!window.hasOwnProperty('pywebview')) {
      console.warn('The python API is not present');
      return;
    }
  
    const input = document.getElementById('earringIdentifier') as HTMLInputElement;
    let api = window['pywebview'].api
    api.get_value()
      .then((x: Message) => {
        let tag: string = x['message'];
        this.bovineRegForm.patchValue({
          earringIdentifier: tag
        });
      })
  }

}
