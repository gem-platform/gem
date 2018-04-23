<template>
  <div>
    <div class="field is-grouped is-grouped-multiline">
      <p class="control">
        <nuxt-link
          :to="newUrl"
          class="button is-light">Create new</nuxt-link>
      </p>
    </div>

    <div
      :is="component"
      :entities="entities"
      :view-url="viewUrl"/>
  </div>
</template>

<script>
import CrudComponentMixin from '@/components/CrudComponentMixin';
import CrudComponents from '@/lib/crud/components';

export default {
  layout: 'dashboard',
  components: CrudComponents.index,
  mixins: [CrudComponentMixin],
  computed: {
    component() {
      return this.$route.params.entities;
    }
  }
};
</script>
