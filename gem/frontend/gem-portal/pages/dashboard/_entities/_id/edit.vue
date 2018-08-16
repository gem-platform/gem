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
import CrudEditComponents from '@/lib/crud/components/edit';
import mass from '@/lib/crud/mass';

export default {
  layout: 'dashboard',
  components: CrudEditComponents,
  data() {
    return {
      busy: false,
      isFormValid: true
    };
  },
  computed: {
    component() {
      return this.$route.params.entities;
    },

    entityId() {
      return this.$route.params.id;
    },

    entity() {
      const { entities } = this.$route.params;

      if (this.entityId === '@new') {
        return this.$store.getters[`dashboard/${entities}/newItem`];
      }

      const method = `dashboard/${entities}/keyed`;
      const getter = this.$store.getters[method];
      const entity = getter[this.entityId];

      if (this.entityId !== '@new' && entity === undefined) {
        throw Error('Entity does not found');
      }

      return entity;
    }
  },
  methods: {
    onInvalid(value) {
      this.isFormValid = !value;
    },
    async save() {
      try {
        this.busy = true;
        const { entities } = this.$route.params;
        await this.$store.dispatch(`dashboard/${entities}/save`, this.entity);
        this.$router.push(`/dashboard/${entities}`);
        this.$snackbar.open({ message: 'Record has been updated' });
      } catch (e) {
        const { response } = e;
        if (response && response.status === 422) {
          this.$snackbar.open({ message: 'Validation error', type: 'is-danger' });
        } else {
          this.$snackbar.open({ message: 'Unknown error', type: 'is-danger' });
        }
      } finally {
        this.busy = false;
      }
    },

    cancel() {
      this.$router.go(-1);
    }
  },
  async fetch(opt) {
    try {
      this.busy = true;

      if (opt.params.id === '@new') {
        const component = CrudEditComponents[opt.params.entities];
        if (component && component.fetch) {
          await component.fetch({ ...opt, mass, newEntity: true });
        }
      } else {
        const method = `dashboard/${opt.params.entities}/fetchOne`;
        const entity = await opt.store.dispatch(method, opt.params.id);
        const component = CrudEditComponents[opt.params.entities];
        if (component && component.fetch) {
          await component.fetch({
            ...opt, entity, mass, newEntity: false
          });
        }
      }
    } finally {
      this.busy = false;
    }
  }
};
</script>
