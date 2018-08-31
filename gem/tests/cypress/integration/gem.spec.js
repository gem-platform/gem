/// <reference types="Cypress" />

context('Actions', () => {
  beforeEach(() => {
    cy.visit('http://localhost')
  })

  
  it('login', () => {
    cy.get('#login').type('root').should('have.value', 'root')
    cy.get('#password').type('root', {force: true}).should('have.value', 'root')
    cy.get('#submit').click()

    cy.get('#greetings')
      .contains('Welcome back, root!')
  })


  it('login failure', () => {
    cy.get('#login').type('root')
    cy.get('#password').type('wrong', {force: true})
    cy.get('#submit').click()

    cy.get('#error')
      .contains('Wrong login/password')
  })


  it('login not found', () => {
    cy.get('#login').type('not-found')
    cy.get('#password').type('wrong', {force: true})
    cy.get('#submit').click()

    cy.get('#error')
      .contains('No specified login found')
  })

  
  it('no password provided', () => {
    cy.get('#login').type('not-found')
    cy.get('#submit').click()

    cy.get('#error')
      .contains('Login and password required')
  })
})
