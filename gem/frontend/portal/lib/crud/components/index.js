import _ from 'lodash';

export default {
  /**
   * Proposals
   */
  proposals: {
    columns: [
      {
        field: 'title',
        label: 'Title',
        sortable: true
      }
    ],
    indexLinkToEdit: false,
    searchColumn: 'title',
    defaultSort: ['title', 'asc'],
    canCreate: true
  },

  /**
   * Comments
   */
  comments: {
    columns: [
      {
        field: 'content',
        label: 'Content'
      },
      {
        label: 'Proposal',
        field(row, options) {
          const proposals = options.$store.getters['dashboard/proposals/keyed'];
          return proposals[row.proposal] ? proposals[row.proposal].title : '<Deleted>';
        }
      },
      {
        field: 'mark',
        label: 'Mark'
      }
    ],
    async fetch(context, entities) {
      const ids = _.chain(entities._items).map(x => x.proposal).uniq().value();
      await context.store.dispatch('dashboard/proposals/fetchList', { ids });
    },
    indexLinkToEdit: true,
    searchColumn: 'content'
  },

  /**
   * Laws
   */
  laws: {
    columns: [
      {
        field: 'title',
        label: 'Title',
        sortable: true
      }
    ],
    indexLinkToEdit: false,
    searchColumn: 'title',
    defaultSort: ['title', 'asc'],
    canCreate: true
  },

  /**
   * Users
   */
  users: {
    columns: [
      {
        field: 'name',
        label: 'Name',
        sortable: true
      },
      {
        label: 'Roles',
        field(row, options) {
          const { roles } = options.$store.getters['names/get'];
          return (row.roles || [])
            .map(id => (roles[id] || '<Unknown Role>'))
            .join(', ');
        }
      }
    ],
    async fetch(context) {
      await context.store.dispatch('names/fetch', { collection: 'roles', field: 'name' });
    },
    indexLinkToEdit: true,
    searchColumn: 'name',
    defaultSort: ['name', 'asc'],
    canCreate: true
  },

  /**
   * Roles
   */
  roles: {
    columns: [
      {
        field: 'name',
        label: 'Name',
        sortable: true
      }
    ],
    indexLinkToEdit: true,
    searchColumn: 'name',
    defaultSort: ['name', 'asc'],
    canCreate: true
  },

  /**
   * Meetings
   */
  meetings: {
    columns: [
      {
        field: 'title',
        label: 'Title',
        sortable: true
      }
    ],
    indexLinkToEdit: true,
    searchColumn: 'title',
    defaultSort: ['title', 'asc'],
    canCreate: true
  },

  /**
   * Zones
   */
  zones: {
    columns: [
      {
        field: 'name',
        label: 'Name',
        sortable: true
      },
      {
        label: 'Path',
        field(row) {
          return row.path && row.path.length > 0
            ? row.path.join(' / ')
            : '<Root>';
        }
      }
    ],
    indexLinkToEdit: true,
    searchColumn: 'name',
    defaultSort: ['name', 'asc'],
    canCreate: true
  },

  /**
   * Officials
   */
  officials: {
    columns: [
      {
        field: 'name',
        label: 'Name',
        sortable: true
      }
    ],
    indexLinkToEdit: true,
    searchColumn: 'name',
    defaultSort: ['name', 'asc'],
    canCreate: true
  },

  workflowTypes: {
    columns: [
      {
        field: 'name',
        label: 'Name',
        sortable: true
      }
    ],
    indexLinkToEdit: true,
    searchColumn: 'name',
    defaultSort: ['name', 'asc'],
    canCreate: true
  },

  workflowStages: {
    columns: [
      {
        field: 'name',
        label: 'Name',
        sortable: true
      }
    ],
    indexLinkToEdit: true,
    searchColumn: 'name',
    defaultSort: ['name', 'asc'],
    canCreate: true
  },

  barItems: {
    columns: [
      {
        field: 'name',
        label: 'Name',
        sortable: true
      }
    ],
    indexLinkToEdit: true,
    searchColumn: 'name',
    defaultSort: ['name', 'asc'],
    canCreate: true
  }
};
