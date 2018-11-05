import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
import { Observable, of } from 'rxjs';
import { CookieService } from 'ngx-cookie-service';

import { Token } from '../shared/token';
import { User } from '../shared/user';
import { Newuser } from '../shared/newuser';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private url = 'http://127.0.0.1:8000';

  private csrfToken = this.cookieService.get('csrftoken')

  private httpOptions = {
  	headers: new HttpHeaders(
      {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.csrfToken
      }
    )
  };

  public token: Token;

  constructor(
    private http: HttpClient,
    private cookieService: CookieService
  ) { }

  // login method using djoser endpoint
  login(user: User): Observable<Token> {
  	const loginUrl = this.url + '/login/';
    console.log(this.cookieService.get('csrftoken'))

  	return this.http.post<Token>(loginUrl, JSON.stringify(user), this.httpOptions)
  		.pipe(
  			catchError(this.handleError<Token>(`login error for Username=${user.username}`))
  		)
  }

  // user create method
  register(user: Newuser) {
  	const registerUrl = this.url + '/auth/users/create/';

  	return this.http.post(registerUrl, JSON.stringify(user), this.httpOptions)
  		.pipe(
  			catchError(this.handleError<Newuser>(`register error for Username=${user.username}`))
  		)
  }

  // logout the user
  logout(): Observable<Token> {
  	const logoutUrl = this.url + '/logout/';

  	return this.http.post<Token>(logoutUrl, JSON.stringify(this.token.auth_token), this.httpOptions)
  		.pipe(
  			catchError(this.handleError<Token>(`logout error`))
  		)
  }


 /**
 * Handle Http operation that failed.
 * Let the app continue.
 * @param operation - name of the operation that failed
 * @param result - optional value to return as the observable result
 */
  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption
      // this.log(`${operation} failed: ${error.message}`);

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  } 

}
