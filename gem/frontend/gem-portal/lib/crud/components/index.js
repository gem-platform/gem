
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
    ]
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
    ]
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
    }
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
    ]
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
    ]
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
    ]
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
    ]
  }
};
