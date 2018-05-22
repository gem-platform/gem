<template>
  <div>
    <div class="field is-grouped is-grouped-multiline">
      <p class="control">
        <nuxt-link
          :to="newUrl"
          class="button">
          <span class="icon">
            <i class="fa fa-plus"/>
          </span>
          <span>Create new</span>
        </nuxt-link>
      </p>
    </div>

    <div
      :is="component"
      :entities="entities"
      :view-url="editUrl"/>
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
