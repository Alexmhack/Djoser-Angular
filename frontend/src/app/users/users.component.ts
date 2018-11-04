import { Component, OnInit } from '@angular/core';

import { User } from '../shared/user';
import { UserService } from '../core/user.service';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss']
})
export class UsersComponent implements OnInit {

  constructor(private userService: UserService) { }
  
  public user: User;

  ngOnInit() {
  	this.user = {
  		username: '',
  		password: ''
  	}
  }
  

  login(): void {
  	this.userService.login(
  		{ 'username': this.user.username, 'password': this.user.password }
  	).subscribe(token => this.userService.token = token)
  }

  logout(): void {
  	this.userService.logout();
  }

}
