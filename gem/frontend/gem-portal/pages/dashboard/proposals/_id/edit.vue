<template>
  <div class="content">
    <form v-on:submit.prevent='submit'>
      <div class="field is-grouped is-grouped-multiline">
        <p class="control">
          <button type="submit" class="button is-light" :class="{'is-loading':isBusy}">Save changes</button>
        </p>
      </div>

      <b-field label="Index">
          <b-input v-model="proposal.index" placeholder="Index" size="is-large"/>
      </b-field>

      <b-field label="Title">
        <b-input v-model="proposal.title" placeholder="Title" size="is-large"/>
      </b-field>

      <b-field label="Content">
        <b-input v-model="proposal.content" type="textarea" placeholder="Content"/>
      </b-field>
    </form>
  </div>
</template>

<script>
const FIELDS = ['_id', 'title', 'index', 'content'];
const STORE_FETCH_METHOD = 'dashboard/proposals/fetch';
const STORE_GET_METHOD = 'dashboard/proposals/all';
const STORE_UPDATE_METHOD = 'dashboard/proposals/update';
const POST_URL = '/api/proposal/';
const REDIRECT_URL = '/dashboard/proposals';

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

      if (id == '@new') {
        return _.zipObject(FIELDS);
      }

      const proposal = proposals(this.$store).find(i => i.index == id);
      return _.pick({ ...proposal }, FIELDS);
    }
  },
  methods: {
    async submit() {
      try {
        this.isBusy = true;
        const id = this.proposal._id;

        if (id) {
          const res = await this.$axios.put(POST_URL + id, this.proposal);
          this.$store.dispatch(STORE_UPDATE_METHOD, this.proposal);
        } else {
          const res = await this.$axios.post(POST_URL, this.proposal);
        }

        this.$router.push(REDIRECT_URL);
        this.$snackbar.open({ message: 'Proposal has been updated' });
      } catch (e) {
        console.error(e);
      } finally {
        this.isBusy = false;
      }
    }
  },
  async fetch({ store, params, error }) {
    if (params.id == '@new') {
      return;
    }

    await store.dispatch(STORE_FETCH_METHOD, { index: params.id });

    const proposal = proposals(store).find(i => i.index == params.id);
    if (!proposal) {
      error({ message: 'Proposal not found', statusCode: 404 });
    }
  }
};
</script>
