/// <reference types='Cypress' />

context('Meeting', () => {
  beforeEach(() => {
    cy.resetAndLogin('basic', 'root', 'root')
  })

  it('test', () => {
    cy.visit('http://localhost/dashboard/proposals')
  })
  
})
