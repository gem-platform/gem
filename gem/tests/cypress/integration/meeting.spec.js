/// <reference types='Cypress' />

context('Meeting', () => {
  beforeEach(() => {
    cy.resetAndLogin('basic', 'root', 'root')
  })

  it('test', () => {
    // id got from basic.json fixture
    cy.visit('http://localhost/meeting/5b476cb4a872bf00105e13d2')
    cy.get("#next").click()
    cy.get('#stage-type').should("contain", "Acquaintance")
  })
  
})
