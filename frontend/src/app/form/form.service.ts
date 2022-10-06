import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Bovine } from '../model/Bovine'

@Injectable({
  providedIn: 'root'
})
export class FormService {
  constructor() { }

  saveBovine(bovine: Bovine) {
    console.log(bovine);
    
    fetch('http://localhost:3000/', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(bovine)
    })
    .then(response => response.text())
    .then(console.log)
    .catch(console.error)
  }

  async getAll() {
    let resp = await fetch('http://localhost:3000/', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
    
    let r = await resp.json()
    return r
  }
}
