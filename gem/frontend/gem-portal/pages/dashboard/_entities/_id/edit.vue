<template>
  <div class="content">
    <form v-on:submit.prevent='save'>
      <div class="field is-grouped is-grouped-multiline">
        <p class="control">
          <button type="submit" class="button is-light" :class="{'is-loading':busy}">Save changes</button>
        </p>
      </div>

      <div :is="this.$route.params.entities" :entity="entity"/>
    </form>
  </div>
</template>

<script>
import CrudComponentMixin from '@/components/CrudComponentMixin';
import CrudComponents from '@/lib/crud/components';
import BusyMixin from '@/components/BusyMixin';

export default {
  layout: 'portal',
  mixins: [
    CrudComponentMixin({
      entities: 'proposals',
      fields: ['_id', 'title', 'index', 'content']
    }),
    BusyMixin
  ],
  components: CrudComponents.edit
};
</script>
