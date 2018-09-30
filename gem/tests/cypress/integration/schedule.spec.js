/// <reference types='Cypress' />

context('Schedules', () => {
  beforeEach(() => {
    cy.resetAndLogin('workflows', 'root', 'root')
    
    cy.visit('/dashboard')
    cy.get("#editable").click()
    cy.get("#add-day").click()
  })

  it('create new event', () => {
    // Fill first event
    cy.get("#event-0-0 [data-role='start']").clear().type("09:00")
    cy.get("#event-0-0 [data-role='end']").type("10:00")
    cy.get("#event-0-0 [data-role='title']").type("New Event")
    cy.get("#save").click()
    
    // Check notification
    cy.get('.snackbar').should('contain', '1 event(s) updated')
    
    // Check event has been saved properly
    cy.request("/api/meetings").then(res => {
      const item = res.body._items[0];

      expect(item).to.have.property("title", "New Event");
      expect(item.start).to.contain("T09:00");
      expect(item.end).to.contain("T10:00");
    })
  })

  it('create multiple events for one day', () => {
    // Add first event
    cy.get("#event-0-0 [data-role='start']").clear().type("09:00")
    cy.get("#event-0-0 [data-role='end']").type("10:00")
    cy.get("#event-0-0 [data-role='title']").type("New Event")

    // Add second event
    cy.get("#group-0 [data-role='add-event']").click()
    cy.get("#event-0-1 [data-role='start']").clear().type("10:00")
    cy.get("#event-0-1 [data-role='end']").type("11:00")
    cy.get("#event-0-1 [data-role='title']").type("New Event 2")

    cy.get("#save").click()
    
    cy.get('.snackbar').should('contain', '2 event(s) updated')
  })

  it('create events for different days', () => {
    cy.get("#add-day").click()

    // Add first event
    cy.get("#event-0-0 [data-role='start']").clear().type("09:00")
    cy.get("#event-0-0 [data-role='end']").type("10:00")
    cy.get("#event-0-0 [data-role='title']").type("New Event 01")

    // Add second event
    cy.get("#event-1-0 [data-role='start']").clear().type("10:00")
    cy.get("#event-1-0 [data-role='end']").type("11:00")
    cy.get("#event-1-0 [data-role='title']").type("New Event 02")

    cy.get("#save").click()
    
    cy.get('.snackbar').should('contain', '2 event(s) updated')
  })

  it('date saved correctly', () => {
    // Add first event
    cy.get("#event-0-0 [data-role='start']").clear().type("09:00")
    cy.get("#event-0-0 [data-role='end']").type("10:00")
    cy.get("#event-0-0 [data-role='title']").type("New Event")

    cy.get("#group-0 [data-role='date']").clear().type("2020/01/01")
    cy.get("#save").click()

    // Check event has been saved properly
    cy.request("/api/meetings").then(res => {
      const item = res.body._items[0];
      expect(item.start).to.contain("2020-01-01")
    });
  });

  it('events with same date are grouped into one block', () => {
    cy.get("#add-day").click()

    // Add first event
    cy.get("#event-0-0 [data-role='start']").clear().type("09:00")
    cy.get("#event-0-0 [data-role='end']").type("10:00")
    cy.get("#event-0-0 [data-role='title']").type("New Event")
    cy.get("#group-0 [data-role='date']").clear().type("2020/01/01")

    // Add second event
    cy.get("#event-1-0 [data-role='start']").clear().type("09:00")
    cy.get("#event-1-0 [data-role='end']").type("10:00")
    cy.get("#event-1-0 [data-role='title']").type("New Event")
    cy.get("#group-1 [data-role='date']").clear().type("2020/01/01")

    cy.get("#save").click()

    // Check events are displayed properly
    cy.visit('/dashboard')
    cy.get("#group-0 [data-role='date']").should("have.value", "2020/01/01")
    cy.get("#group-1").should('not.exist');

    // Check events has been saved properly
    cy.request("/api/meetings").then(res => {
      const item0 = res.body._items[0];
      const item1 = res.body._items[0];
      expect(item0.start).to.contain("2020-01-01")
      expect(item1.start).to.contain("2020-01-01")
    });
  });

  it('event present at /schedule page', () => {
    // Add new event
    cy.get("#event-0-0 [data-role='start']").clear().type("09:00")
    cy.get("#event-0-0 [data-role='end']").type("10:00")
    cy.get("#event-0-0 [data-role='title']").type("New Event")
    cy.get("#save").click()
    
    // Check event is present at schedule page
    cy.visit('/')
    cy.get("#event-0-0").should("contain", "New Event")    
  })

  it.only('delete is working', () => {
    // Add new event
    cy.get("#event-0-0 [data-role='start']").clear().type("09:00")
    cy.get("#event-0-0 [data-role='end']").type("10:00")
    cy.get("#event-0-0 [data-role='title']").type("New Event")
    cy.get("#save").click()
    
    // Delete event and save
    cy.get("#editable").click()
    cy.get("#event-0-0 [data-role='delete']").click()
    cy.get("#save").click()

    // Check nothing is displayed at schedule page
    cy.visit('/')
    cy.get("#group-0").should("not.exist")
    
    // Check events has been saved properly
    cy.request("/api/meetings").then(res => {
      const items = res.body._items;
      expect(items.length).to.eq(0)
    });
  })

})
