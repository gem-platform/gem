<template>
  <div class="content">
    Do you really want to delete?
    {{ proposal.title }}
    <a class="button is-danger" @click="submit">Confirm</a>
  </div>
</template>

<script>
const FIELDS = ['_id', 'title', 'index', 'content'];
const STORE_GET_METHOD = 'dashboard/proposals/all';
const STORE_FETCH_METHOD = 'dashboard/proposals/fetch';

const proposals = store => {
  return store.getters[STORE_GET_METHOD];
};

export default {
  layout: 'portal',
  data() {
    return {
      isBusy: false
    };
  },
  computed: {
    proposal() {
      const id = this.$route.params.id;
      const proposal = proposals(this.$store).find(i => i.index == id);
      return _.pick({ ...proposal }, FIELDS);
    }
  },
  methods: {
    async submit() {
      try {
        const id = this.proposal._id;
        const res = await this.$axios.delete('/api/proposal/' + id);
        this.$router.push('/dashboard/proposals');
      } catch (e) {
        console.error(e);
      }
    }
  },
  async fetch({ store, params, error }) {
    await store.dispatch(STORE_FETCH_METHOD, { index: params.id });
    const proposal = proposals(store).find(i => i.index == params.id);
    if (!proposal) {
      error({ message: 'Proposal not found', statusCode: 404 });
    }
  }
};
</script>
