/// <reference types="Cypress" />

context('Dashboard / Proposals', () => {
  beforeEach(() => {
    cy.login('root', 'root')
    cy.visit('http://localhost/dashboard/proposals')
  })

  it('index required', () => {
    cy.visit('http://localhost/dashboard/proposals/@new/edit')
    cy.get('#index').type('_').clear()
    cy.get('#index-field').find('.help').first().should('contain', 'Value is required')
  });

  it('index too short', () => {
    cy.visit('http://localhost/dashboard/proposals/@new/edit')
    cy.get('#index').type('_')
    cy.get('#index-field').find('.help').first().should('contain', 'Value is too short')
  });

  it('title required', () => {
    cy.visit('http://localhost/dashboard/proposals/@new/edit')
    cy.get('#title').type('_').clear()
    cy.get('#title-field').find('.help').first().should('contain', 'Value is required')
  });

  it('title too short', () => {
    cy.visit('http://localhost/dashboard/proposals/@new/edit')
    cy.get('#title').type('_')
    cy.get('#title-field').find('.help').first().should('contain', 'Value is too short')
  });

  it('create', () => {
    cy.visit('http://localhost/dashboard/proposals/@new/edit')
    
    // fill index
    cy.get('#index').type('proposal-index')

    // fill title
    cy.get('#title').type('Proposal Title')
    
    // select workflow
    cy.get('#workflow > .control > .input').type('General')
    cy.get('#workflow > .dropdown-menu > .dropdown-content > .dropdown-item').first().click()

    // select stage
    cy.get('#stage > .control > .input').type('Initial')
    cy.get('#stage > .dropdown-menu > .dropdown-content > .dropdown-item').first().click({multiple: true})
    
    // fill content
    cy.get('#content > .ql-editor').type('Some content')
    
    // save
    cy.get('#save').click()

    cy.location('pathname', {timeout: 60000})
      .should('match', /dashboard\/proposals$/);

    cy.get('.table').should('contain', 'Proposal Title')

    // asserts
    //cy.get('.snackbar').should('contains', 'New proposal has been created')
  });
})
