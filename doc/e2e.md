# End to end testing
Install [cypress](https://www.cypress.io/) first

## Run tests
Go to folder and run _cypress_
```
cd gem/tests
npx cypress open
```
For windows just run _cypress_ and drag _gem/tests_ folder into window.

## Change domain to test
To run _e2e_ tests for specified domain (like staging server, not development) just pass url to _CYPRESS_baseUrl_ environment variable:
```sh
CYPRESS_baseUrl=https://staging.gem.iskcon.com npx cypress open
```