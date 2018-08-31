/// <reference types="Cypress" />

context('Actions', () => {
  beforeEach(() => {
    cy.visit('http://localhost')
  })

  // https://on.cypress.io/interacting-with-elements

  it('login', () => {
    cy.get('#login')
      .type('root').should('have.value', 'root')

    cy.get('#password')
      .type('root', {force: true}).should('have.value', 'root')
    
    cy.get('#submit')
      .click()

    cy.get('#greetings')
      .contains('Welcome back, root!')
  })

})
