## A11 Part 2: Authentication & Access Control 

- Authentication protects my application from accidentally/unknowingly granting unauthorized users with C.R.U.D privileges. 

- LoginRequiredMixin and @login_required help me do that by locking down cbv's and fbv's respectively. (Requires a user to login before proceeding to a "locked" view)

- The next query parameter changes the "success url" after a valid login attempt. If it exists, the browser will redirect to the value of this parameter. 

### Login Related Settings:

```
LOGIN_URL = 'login_view'
LOGIN_REDIRECT_URL = 'dashboard_view'
LOGOUT_URL = 'logout_view'
LOGOUT_REDIRECT_URL = 'login_view'
```
