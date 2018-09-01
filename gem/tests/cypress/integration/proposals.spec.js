/// <reference types='Cypress' />

context('Dashboard / Proposals', () => {
  beforeEach(() => {
    cy.request('POST', 'http://localhost/api/debug/reset')

    cy.createEntity('workflowStages', {
      name: 'Initial',
      actions: ['ballot']
    })
    .its('body._id')
    .then((id) => {
      cy.createEntity('workflowTypes', {
        name: 'General',
        stages: [id]
      })
    })

    cy.login('root', 'root')
    cy.visit('http://localhost/dashboard/proposals/@new/edit')
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
    cy.route('/api/proposals').as('proposals')

    cy.get('#index').type('PRP-001')
    cy.get('#title').type('New Proposal')
    cy.get('#workflow > .control > .input').type('General')
    cy.get('#workflow > .dropdown-menu > .dropdown-content > .dropdown-item').first().click()
    cy.get('#stage > .control > .input').type('Initial')
    cy.get('#stage > .dropdown-menu > .dropdown-content > .dropdown-item').first().click()
    cy.get('#content > .ql-editor').type('Content')
    cy.get('#save').click()
    
    cy.wait('@proposals').then(() => {
      cy.get('.snackbar').should('contain', 'New proposal has been created')
      cy.location('pathname', {timeout: 1500})
        .should('match', /dashboard\/proposals$/);
      cy.get('.table').should('contain', 'New Proposal')
    })

    
    
    
    // asserts
    //
  });

})
