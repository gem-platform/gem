<template>
  <div class="content">
    <div class="field is-grouped is-grouped-multiline">
      <p class="control">
        <nuxt-link
          :to="editUrl(entity._id)"
          class="button is-light">Edit</nuxt-link>
      </p>
      <p class="control">
        <nuxt-link
          :to="deleteUrl"
          class="button is-light">Delete</nuxt-link>
      </p>
    </div>

    <div
      :is="component"
      :entity="entity"/>
  </div>
</template>

<script>
import CrudComponentMixin from '@/components/CrudComponentMixin';
import CrudComponents from '@/lib/crud/components';

export default {
  layout: 'dashboard',
  components: CrudComponents.id,
  mixins: [CrudComponentMixin],
  computed: {
    component() {
      return this.$route.params.entities;
    }
  }
};
</script>
