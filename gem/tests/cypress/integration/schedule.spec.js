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

  it.only('create multiple events for one day', () => {
    cy.get("#editable").click()
    cy.get("#add-day").click()
    cy.get("#event-0-0 [data-role='start']").clear().type("09:00")
    cy.get("#event-0-0 [data-role='end']").type("10:00")
    cy.get("#event-0-0 [data-role='title']").type("New Event")

    cy.get("#group-0 [data-role='add-event']").click()
    cy.get("#event-0-1 [data-role='start']").clear().type("10:00")
    cy.get("#event-0-1 [data-role='end']").type("11:00")
    cy.get("#event-0-1 [data-role='title']").type("New Event 2")

    cy.get("#save").click()
    
    cy.get('.snackbar').should('contain', '2 event(s) updated')
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

  it('date saved correctly', () => {
    cy.get("#editable").click()
    cy.get("#add-day").click()

    cy.get("#event-0-0 [data-role='start']").clear().type("09:00")
    cy.get("#event-0-0 [data-role='end']").type("10:00")
    cy.get("#event-0-0 [data-role='title']").type("New Event")

    cy.get("#group-0 [data-role='date']").clear().type("2020/01/01")

    cy.get("#save").click()

    cy.visit('/dashboard')
    cy.get("#group-0 [data-role='date']").should("have.value", "2020/01/01")
  });


  it('events with same date are grouped into one block', () => {
    cy.get("#editable").click()
    
    cy.get("#add-day").click()
    cy.get("#event-0-0 [data-role='start']").clear().type("09:00")
    cy.get("#event-0-0 [data-role='end']").type("10:00")
    cy.get("#event-0-0 [data-role='title']").type("New Event")
    cy.get("#group-0 [data-role='date']").clear().type("2020/01/01")

    cy.get("#add-day").click()
    cy.get("#event-1-0 [data-role='start']").clear().type("09:00")
    cy.get("#event-1-0 [data-role='end']").type("10:00")
    cy.get("#event-1-0 [data-role='title']").type("New Event")
    cy.get("#group-1 [data-role='date']").clear().type("2020/01/01")

    cy.get("#save").click()

    cy.visit('/dashboard')
    cy.get("#group-0 [data-role='date']").should("have.value", "2020/01/01")
    cy.get("#group-1").should('not.exist');
  });


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

  it('delete is working', () => {
    cy.get("#editable").click()
    cy.get("#add-day").click()
    cy.get("#event-0-0 [data-role='start']").clear().type("09:00")
    cy.get("#event-0-0 [data-role='end']").type("10:00")
    cy.get("#event-0-0 [data-role='title']").type("New Event")
    cy.get("#save").click()
    
    cy.get("#editable").click()
    cy.get("#event-0-0 [data-role='delete']").click()
    cy.get("#save").click()

    cy.visit('/')
    cy.get("#group-0").should("not.exist")    
  })

})
