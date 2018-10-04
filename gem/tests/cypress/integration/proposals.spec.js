/// <reference types='Cypress' />

context('Dashboard / Proposals', () => {
  beforeEach(() => {
    cy.resetAndLogin('workflows', 'root', 'root')
    cy.visit('/dashboard/proposals/@new/edit')
  })

  it('creation page is available', () => {
    cy.location('pathname')
      .should('match', /dashboard\/proposals\/@new\/edit$/);
  })

  it('index required', () => {
    cy.get('#index').type('_').clear()
    cy.get('#index-field').find('.help').should('contain', 'Value is required')
  });

  it('index is too short', () => {
    cy.get('#index').type('_')
    cy.get('#index-field').find('.help').should('contain', 'Value is too short')
  });

  it('title required', () => {
    cy.get('#title').type('_').clear()
    cy.get('#title-field').find('.help').should('contain', 'Value is required')
  });

  it('title is too short', () => {
    cy.get('#title').type('_')
    cy.get('#title-field').find('.help').should('contain', 'Value is too short')
  });

  it('proposal created', () => {
    cy.server()
    cy.route('GET', '/api/proposals').as('proposals')

    cy.get('#index').type('PRP-001')
    cy.get('#title').type('New Proposal')
    cy.get('#workflow > .control > .input').type('General')
    cy.get('#workflow > .dropdown-menu > .dropdown-content > .dropdown-item :not(.is-disabled)').first().click()
    cy.get('#stage > .control > .input').type('Initial')
    cy.get('#stage > .dropdown-menu > .dropdown-content > .dropdown-item :not(.is-disabled)').first().click()
    cy.get('#content > .ql-editor').type('Content')
    cy.get('#save').click()
    
    cy.wait('@proposals').then(() => {
      cy.get('.snackbar').should('contain', 'New proposal has been created')
      cy.location('pathname', {timeout: 1500})
        .should('match', /dashboard\/proposals$/);
      cy.get('.table', {timeout: 5000}).should('contain', 'New Proposal')
    })
  })
})
