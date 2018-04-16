<template>
  <div class="content">
    <form v-on:submit.prevent='save'>
      <div class="field is-grouped is-grouped-multiline">
        <p class="control">
          <button type="submit" class="button is-light" :class="{'is-loading':busy}">Save changes</button>
        </p>
      </div>

      <b-field label="Index">
          <b-input v-model="entity.index" placeholder="Index" size="is-large"/>
      </b-field>

      <b-field label="Title">
        <b-input v-model="entity.title" placeholder="Title" size="is-large"/>
      </b-field>

      <b-field label="Content">
        <b-input v-model="entity.content" type="textarea" placeholder="Content"/>
      </b-field>
    </form>
  </div>
</template>

<script>
import CrudComponentMixin from '@/components/CrudComponentMixin';
import BusyMixin from '@/components/BusyMixin';

export default {
  layout: 'portal',
  mixins: [
    CrudComponentMixin({
      entities: 'proposals',
      fields: ['_id', 'title', 'index', 'content']
    }),
    BusyMixin
  ]
};
</script>
