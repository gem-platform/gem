/// <reference types='Cypress' />

context('Schedules', () => {
  beforeEach(() => {
    cy.resetAndLogin('workflows', 'root', 'root')
    cy.visit('/dashboard')
  })

  it('create new event', () => {
    cy.get("#editable").click()
    cy.get("#add-day").click()
    cy.get("#event-0-0 [data-role='start']").clear().type("09:00")
    cy.get("#event-0-0 [data-role='end']").type("10:00")
    cy.get("#event-0-0 [data-role='title']").type("New Event")
    cy.get("#save").click()
    
    cy.get('.snackbar').should('contain', '1 event(s) updated')
  })

  it('create events for different days', () => {
    cy.get("#editable").click()
    
    cy.get("#add-day").click()
    cy.get("#event-0-0 [data-role='start']").clear().type("09:00")
    cy.get("#event-0-0 [data-role='end']").type("10:00")
    cy.get("#event-0-0 [data-role='title']").type("New Event 01")

    cy.get("#add-day").click()
    cy.get("#event-1-0 [data-role='start']").clear().type("10:00")
    cy.get("#event-1-0 [data-role='end']").type("11:00")
    cy.get("#event-1-0 [data-role='title']").type("New Event 02")

    cy.get("#save").click()
    
    cy.get('.snackbar').should('contain', '2 event(s) updated')
  })

  it('event present at /schedule page', () => {
    cy.get("#editable").click()
    cy.get("#add-day").click()
    cy.get("#event-0-0 [data-role='start']").clear().type("09:00")
    cy.get("#event-0-0 [data-role='end']").type("10:00")
    cy.get("#event-0-0 [data-role='title']").type("New Event")
    cy.get("#save").click()
    
    cy.visit('/')

    cy.get("#event-0-0").should("contain", "New Event")    
  })

})
