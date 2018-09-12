Cypress.Commands.add("login", (login, password) => {
  cy.request('POST', '/api/auth/login', { login, password })
    .then((response) => {
      const token = response.body.token;
      cy.setCookie('auth._refresh_token.local', 'false')
      cy.setCookie('auth._token.local', 'Bearer%20'+token)
    })
});

Cypress.Commands.add("createEntity", (type, data) => {
    return cy.request('POST', '/api/' + type, data)
});

Cypress.Commands.add("resetAndLogin", (fixture, login, password) => {
  cy.fixture(fixture).then((json) => {
    cy.request('POST', '/api/debug/reset', json).then(() => {
      cy.login(login, password)
    })
  })
});

Cypress.Commands.add("resetDb", () => {
  cy.request('POST', '/api/debug/reset', {});
});
