import idProposals from '@/components/dashboard/proposals/id.vue';
import indexProposals from '@/components/dashboard/proposals/index.vue';
import editProposals from '@/components/dashboard/proposals/edit.vue';

import idUsers from '@/components/dashboard/users/id.vue';
import indexUsers from '@/components/dashboard/users/index.vue';
import editUsers from '@/components/dashboard/users/edit.vue';

import idRoles from '@/components/dashboard/roles/id.vue';
import indexRoles from '@/components/dashboard/roles/index.vue';
import editRoles from '@/components/dashboard/roles/edit.vue';

export default {
  id: {
    proposals: idProposals,
    users: idUsers,
    roles: idRoles
  },
  index: {
    proposals: indexProposals,
    users: indexUsers,
    roles: indexRoles
  },
  edit: {
    proposals: editProposals,
    users: editUsers,
    roles: editRoles
  },
  options: {
    proposals: {
      fields: ['_id', 'index', 'title', 'content']
    },
    users: {
      fields: ['_id', 'name', 'roles']
    },
    roles: {
      fields: ['_id', 'name', 'permissions']
    }
  }
};
