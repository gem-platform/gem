<template>
  <div>
    <div>
      <div class="field is-grouped is-grouped-multiline">
        <p class="control">
          <button
            :class="{'is-loading':busy}"
            type="submit"
            class="button is-light"
            @click="save">
            Save changes
          </button>
        </p>
      </div>

      <div
        :is="component"
        :entity="entity"/>
    </div>
  </div>
</template>

<script>
import CrudComponentMixin from '@/components/CrudComponentMixin';
import CrudComponents from '@/lib/crud/components';

export default {
  layout: 'dashboard',
  components: CrudComponents.edit,
  mixins: [CrudComponentMixin],
  computed: {
    component() {
      return this.$route.params.entities;
    },
    options() {
      const { entities } = this.$route.params;
      return CrudComponents.options[entities];
    }
  }
};
</script>
