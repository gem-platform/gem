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
    
    <h1>{{ entity.title }} ({{entity.index}})</h1>
    {{ entity.content }}
  </div>
</template>

<script>
import CrudComponentMixin from '@/components/CrudComponentMixin';

export default {
  layout: 'portal',
  mixins: [
    CrudComponentMixin({
      entities: 'proposals',
      fields: ['_id', 'title', 'index', 'content']
    })
  ]
};
</script>
