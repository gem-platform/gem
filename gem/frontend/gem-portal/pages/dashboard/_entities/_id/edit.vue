<template>
  <div class="content">
    <form @submit.prevent="save">
      <div class="field is-grouped is-grouped-multiline">
        <p class="control">
          <button
            :class="{'is-loading':busy}"
            type="submit"
            class="button is-light">
            Save changes
          </button>
        </p>
      </div>

      <div
        :is="this.$route.params.entities"
        :entity="entity"/>
    </form>
  </div>
</template>

<script>
import CrudComponentMixin from '@/components/CrudComponentMixin';
import CrudComponents from '@/lib/crud/components';
import BusyMixin from '@/components/BusyMixin';

export default {
  layout: 'portal',
  components: CrudComponents.edit,
  mixins: [
    CrudComponentMixin({
      entities: 'proposals',
      fields: ['_id', 'title', 'index', 'content']
    }),
    BusyMixin
  ]
};
</script>
