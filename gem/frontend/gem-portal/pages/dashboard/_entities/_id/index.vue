<template>
  <div class="content">
    <div class="field is-grouped is-grouped-multiline">
      <p class="control">
        <nuxt-link :to="editUrl" class="button is-light">Edit</nuxt-link>
      </p>
      <p class="control">
        <nuxt-link :to="deleteUrl" class="button is-light">Delete</nuxt-link>
      </p>
    </div>

    <div :is="this.$route.params.entities" :entity="entity"/>
  </div>
</template>

<script>
import CrudComponentMixin from '@/components/CrudComponentMixin';
import CrudComponents from '@/lib/crud/components';

export default {
  layout: 'portal',
  mixins: [
    CrudComponentMixin({
      fields: ['_id', 'title', 'index', 'content']
    })
  ],
  components: CrudComponents.index
};
</script>
