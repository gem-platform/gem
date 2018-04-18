import idProposals from '@/components/dashboard/proposals/id.vue';
import indexProposals from '@/components/dashboard/proposals/index.vue';
import editProposals from '@/components/dashboard/proposals/edit.vue';

import idUsers from '@/components/dashboard/users/id.vue';
import indexUsers from '@/components/dashboard/users/index.vue';
import editUsers from '@/components/dashboard/users/edit.vue';

export default {
  id: {
    proposals: idProposals,
    users: idUsers
  },
  index: {
    proposals: indexProposals,
    users: indexUsers
  },
  edit: {
    proposals: editProposals,
    users: editUsers
  },
  options: {
    proposals: {
      fields: ['_id', 'index', 'title', 'content']
    },
    users: {
      fields: ['_id', 'name', 'roles']
    }
  }
};
