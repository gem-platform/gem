import idProposals from '@/components/dashboard/proposals/id.vue';
import indexProposals from '@/components/dashboard/proposals/index.vue';
import editProposals from '@/components/dashboard/proposals/edit.vue';

import idLaws from '@/components/dashboard/laws/id.vue';
import indexLaws from '@/components/dashboard/laws/index.vue';
import editLaws from '@/components/dashboard/laws/edit.vue';


import indexUsers from '@/components/dashboard/users/index.vue';
import editUsers from '@/components/dashboard/users/edit.vue';

import indexRoles from '@/components/dashboard/roles/index.vue';
import editRoles from '@/components/dashboard/roles/edit.vue';

import indexMeetings from '@/components/dashboard/meetings/index.vue';
import editMeetings from '@/components/dashboard/meetings/edit.vue';

export default {
  id: {
    proposals: idProposals,
    laws: idLaws
  },
  index: {
    proposals: indexProposals,
    laws: indexLaws,
    users: indexUsers,
    roles: indexRoles,
    meetings: indexMeetings
  },
  edit: {
    proposals: editProposals,
    laws: editLaws,
    users: editUsers,
    roles: editRoles,
    meetings: editMeetings
  },
  options: {
    proposals: {
      fields: ['_id', 'index', 'title', 'content']
    },
    laws: {
      fields: ['_id', 'index', 'title', 'content']
    },
    users: {
      fields: ['_id', 'name', 'roles']
    },
    roles: {
      fields: ['_id', 'name', 'permissions']
    },
    meetings: {
      fields: ['_id', 'title', 'agenda', 'start', 'end', 'proposals', 'permissions']
    }
  }
};
