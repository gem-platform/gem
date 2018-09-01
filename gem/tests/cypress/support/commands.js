// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************

Cypress.Commands.add("login", (login, password) => {
  cy.request('POST', 'http://localhost/api/auth/login', { login, password })
    .then((response) => {
      const token = response.body.token;
      cy.setCookie('auth._refresh_token.local', 'false')
      cy.setCookie('auth._token.local', 'Bearer%20'+token)
    })
});

Cypress.Commands.add("createEntity", (type, data) => {
    return cy.request('POST', 'http://localhost/api/' + type, data)
});