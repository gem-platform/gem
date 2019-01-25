/// <reference types='Cypress' />

context('Meeting', () => {
  beforeEach(() => {
    cy.resetAndLogin('general', 'root', 'root');

    cy.visit('dashboard/meetings/');
    cy.get('#create').click();
  });

  it('create new meeting with minimal data', () => {
    cy.get('#title').type('Proposal 001');

    cy.get('#save').click();
  });

  it('create new meeting', () => {
    // Title
    cy.get('#title').type('Meeting 001');

    // Start date
    cy.get('#startDate').click();
    cy.get('.datepicker .is-selected')
      .first()
      .click();

    // End date
    cy.get('#endDate').click();
    cy.get('.datepicker .is-selected')
      .last()
      .click();

    // Start time
    cy.get('#startTime').click();
    cy.get('#startTime')
      .parents('.timepicker')
      .find('select')
      .first()
      .select('09');
    cy.get('#startTime')
      .parents('.timepicker')
      .find('select')
      .last()
      .select('10');
    cy.get('body').click();

    // End time
    cy.get('#endTime').click();
    cy.get('#endTime')
      .parents('.timepicker')
      .find('select')
      .first()
      .select('10');
    cy.get('#endTime')
      .parents('.timepicker')
      .find('select')
      .last()
      .select('30');

    cy.get('body').click();

    // Agenda
    cy.get('#agenda').type('Agenda');

    // Join permissions
    cy.get('#join-permissions input').type('Tester');
    cy.get('#join-permissions .dropdown-item :not(.is-disabled)')
      .first()
      .click();

    // Vote permissions
    cy.get('#vote-permissions input').type('Tester');
    cy.get('#vote-permissions .dropdown-item :not(.is-disabled)')
      .first()
      .click();

    // Proposals
    cy.get('#proposals input').type('Proposal');
    cy.get('#proposals .dropdown-item')
      .first()
      .click();

    // Save
    cy.get('#save').click();

    // Check meeting is saved correctly
    cy.request('api/meetings').then(res => {
      const item0 = res.body._items[0];

      expect(item0).to.have.property('title', 'Meeting 001');
      expect(item0).to.have.property('agenda', 'Agenda');

      expect(item0.startTime).to.contain('T09:10');
      expect(item0.endTime).to.contain('T10:30');

      expect(item0.proposals).eqls(['5a5deebeb5385609a9c9cea4']);
      expect(item0.permissions).eqls([
        { scope: 'meeting.join', role: '5a5deebeb5385609a9c9cea5' },
        { scope: 'meeting.vote', role: '5a5deebeb5385609a9c9cea5' }
      ]);
    });
  });
});
