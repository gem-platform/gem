import _ from 'lodash';

export default {
  /**
   * Proposals
   */
  proposals: {
    columns: [
      {
        field: 'title',
        label: 'Title'
      }
    ],
    indexLinkToEdit: false,
    searchColumn: 'title'
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
    indexLinkToEdit: true
  },

  /**
   * Laws
   */
  laws: {
    columns: [
      {
        field: 'title',
        label: 'Title'
      }
    ],
    indexLinkToEdit: false,
    searchColumn: 'title'
  },

  /**
   * Users
   */
  users: {
    columns: [
      {
        field: 'name',
        label: 'Name'
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
    searchColumn: 'name'
  },

  /**
   * Roles
   */
  roles: {
    columns: [
      {
        field: 'name',
        label: 'Name'
      }
    ],
    indexLinkToEdit: true,
    searchColumn: 'name'
  },

  /**
   * Meetings
   */
  meetings: {
    columns: [
      {
        field: 'title',
        label: 'Title'
      }
    ],
    indexLinkToEdit: true,
    searchColumn: 'title'
  },

  /**
   * Zones
   */
  zones: {
    columns: [
      {
        field: 'name',
        label: 'Name'
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
    searchColumn: 'name'
  },

  /**
   * Officials
   */
  officials: {
    columns: [
      {
        field: 'name',
        label: 'Name'
      }
    ],
    indexLinkToEdit: true,
    searchColumn: 'name'
  }
};
