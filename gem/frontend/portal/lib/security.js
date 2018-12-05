export default {
  permissions: [
    // General
    {
      _id: '*',
      name: 'Superuser',
      desc: 'Have full rights',
      group: 'General'
    },

    // Access Dashboard
    {
      _id: 'dashboard',
      name: 'Dashboard',
      desc: 'Access Dashboard page',
      group: 'Dashboard Access'
    },
    {
      _id: 'dashboard.roles',
      name: 'Roles',
      desc: 'Access Roles page at dashboard',
      group: 'Dashboard Access'
    },
    {
      _id: 'dashboard.proposals',
      name: 'Proposals',
      desc: 'Access Proposals page at dashboard',
      group: 'Dashboard Access'
    },
    {
      _id: 'dashboard.comments',
      name: 'Comments',
      desc: 'Access Comments page at dashboard',
      group: 'Dashboard Access'
    },
    {
      _id: 'dashboard.users',
      name: 'Users',
      desc: 'Access Users page at dashboard',
      group: 'Dashboard Access'
    },
    {
      _id: 'dashboard.meetings',
      name: 'Meetings',
      desc: 'Access Meetings page at dashboard',
      group: 'Dashboard Access'
    },
    {
      _id: 'dashboard.laws',
      name: 'Laws',
      desc: 'Access Laws page at dashboard',
      group: 'Dashboard Access'
    },
    {
      _id: 'za.officials',
      name: 'Officials',
      desc: 'Access Officials page',
      group: 'Dashboard Access'
    },
    {
      _id: 'za.zones',
      name: 'Zones',
      desc: 'Access Zones page',
      group: 'Dashboard Access'
    },

    // Edit Entities
    {
      _id: 'roles.edit',
      name: 'Roles',
      group: 'Edit entities'
    },
    {
      _id: 'proposals.edit',
      name: 'Proposals',
      group: 'Edit entities'
    },
    {
      _id: 'users.edit',
      name: 'Users',
      group: 'Edit entities'
    },
    {
      _id: 'meetings.edit',
      name: 'Meetings',
      group: 'Edit entities'
    },
    {
      _id: 'laws.edit',
      name: 'Laws',
      group: 'Edit entities'
    },
    {
      _id: 'officials.edit',
      name: 'Officials',
      group: 'Edit entities'
    },
    {
      _id: 'zones.edit',
      name: 'Zones',
      group: 'Edit entities'
    },

    // Meeting
    {
      _id: 'meeting',
      name: 'Meetings',
      desc: 'Access Meeting page',
      group: 'Meeting'
    },
    {
      _id: 'meeting.vote',
      name: 'Vote',
      desc: 'Participate in ballot stage of meeting',
      group: 'Meeting'
    },
    {
      _id: 'meeting.comment',
      name: 'Comment',
      desc: 'Participate in commenting stage of meeting',
      group: 'Meeting'
    },
    {
      _id: 'meeting.discuss',
      name: 'Discuss',
      desc: 'Participate in discussion stage of meeting',
      group: 'Meeting'
    },
    {
      _id: 'meeting.join',
      name: 'Join Meeting',
      desc: 'Ability to join meeting',
      group: 'Meeting'
    },
    {
      _id: 'meeting.manage',
      name: 'Manage Meeting',
      desc: 'Mange meeting',
      group: 'Meeting'
    },
    {
      _id: 'meeting.presenter',
      name: 'Presenter',
      desc: 'Hide all controls',
      group: 'Meeting'
    },
    {
      _id: 'bar.manage',
      name: 'Manage Bar',
      desc: 'Manage Bar',
      group: 'Bar'
    },
    {
      _id: 'bar.orders',
      name: 'Vew bar orders',
      desc: 'Vew bar orders',
      group: 'Bar'
    },
    {
      _id: 'bar',
      name: 'Access Bar',
      desc: 'Access Bar',
      group: 'Bar'
    }
  ]
};
