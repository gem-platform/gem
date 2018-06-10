<template>
  <div>
    <div class="dashboard-form">
      <div
        :is="component"
        :entity="entity"
        @invalid="onInvalid"/>
    </div>

    <div class="dashboard-controls">
      <div class="field is-grouped is-grouped-multiline">
        <p class="control">
          <button
            :disabled="!isFormValid"
            :class="{'is-loading':busy}"
            type="submit"
            class="button is-light"
            @click="save">
            <span class="icon">
              <i class="fa fa-save"/>
            </span>
            <span>Save</span>
          </button>
        </p>
        <p class="control">
          <button
            class="button is-light"
            @click="cancel">
            <span class="icon">
              <i class="fa fa-ban"/>
            </span>
            <span>Cancel</span>
          </button>
        </p>
      </div>
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
  data() {
    return {
      isFormValid: true
    };
  },
  computed: {
    component() {
      return this.$route.params.entities;
    },
    options() {
      const { entities } = this.$route.params;
      return CrudComponents.options[entities];
    }
  },
  methods: {
    onInvalid(value) {
      this.isFormValid = !value;
    }
  }
};
</script>
