<template>
  <div class="content">
    <form v-on:submit.prevent='submit'>
      <div class="field is-grouped is-grouped-multiline">
        <p class="control">
          <button type="submit" class="button is-light" :class="{'is-loading':busy}">Save changes</button>
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
import CrudController from '@/lib/crud';

const REDIRECT_URL = '/dashboard/proposals';

const controller = new CrudController({
  apiPrefix: '/api/proposal/',
  storePrefix: 'dashboard/proposals/',
  idField: 'index',
  fields: ['_id', 'title', 'index', 'content']
});

export default {
  layout: 'portal',
  computed: {
    proposal() {
      return controller.entity({
        id: this.$route.params.id
      });
    },
    busy() {
      return this.$store.getters['busy'];
    }
  },
  methods: {
    async submit() {
      await controller.submit({
        id: this.proposal._id,
        data: this.proposal
      });

      this.$router.push(REDIRECT_URL);
      this.$snackbar.open({ message: 'Proposal has been updated' });
    }
  },
  async fetch({ store, params, error }) {
    await controller.fetch({ store, id: params.id });
  },
  created() {
    controller.set({ store: this.$store });
  }
};
</script>
