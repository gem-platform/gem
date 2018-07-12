<template>
  <div class="content">
    <div
      v-if="canEdit"
      class="field is-grouped is-grouped-multiline">

      <p class="control">
        <nuxt-link
          :to="linkToEdit(entity._id)"
          class="button is-light">Edit</nuxt-link>
      </p>
      <p class="control">
        <nuxt-link
          :to="linkToDelete(entity._id)"
          class="button is-light">Delete</nuxt-link>
      </p>
    </div>

    <div
      :is="component"
      :entity="entity"/>
  </div>
</template>

<script>
import CrudViewComponents from '@/lib/crud/components/view';
import AuthMixin from '@/components/AuthMixin';
import CrudLinksComponentMixin from '@/components/CrudLinksComponentMixin';

export default {
  layout: 'dashboard',
  components: CrudViewComponents,
  mixins: [AuthMixin, CrudLinksComponentMixin],
  computed: {
    id() {
      return this.$route.params.id;
    },
    component() {
      return this.$route.params.entities;
    },
    entity() {
      return this.$store.getters[`dashboard/${this.component}/keyed`][this.id];
    },
    canEdit() {
      return this.haveAccess(`${this.component}.edit`);
    }
  },
  async fetch(opt) {
    const method = `dashboard/${opt.params.entities}/fetchOne`;
    await opt.store.dispatch(method, opt.params.id);
  }
};
</script>
