import idProposals from '@/components/dashboard/proposals/id.vue';
import indexProposals from '@/components/dashboard/proposals/index.vue';
import editProposals from '@/components/dashboard/proposals/edit.vue';

export default {
  id: {
    proposals: idProposals
  },
  index: {
    proposals: indexProposals
  },
  edit: {
    proposals: editProposals
  },
  options: {
    proposals: {
      fields: ['_id', 'index', 'title', 'content']
    }
  }
};
