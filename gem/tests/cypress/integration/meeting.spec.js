/// <reference types='Cypress' />

context('Meeting', () => {
  beforeEach(() => {
    cy.fixture('basic').then((json) => {
      cy.request('POST', 'http://localhost/api/debug/reset', json).then(() => {
        cy.login('root', 'root')
      })
    })
  })

  it('test', () => {
    cy.visit('http://localhost/dashboard/proposals')
  })
  
})
