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
    cy.visit('http://localhost/login')
    cy.get('#login').type(login)
    cy.get('#password').type(password, {force: true})
    cy.get('#submit').click()
    
    cy.location().should((loc) => {
        expect(loc.pathname).to.eq('/');
    });
});
