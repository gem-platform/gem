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
            id="save"
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
            id="cancel"
            class="button is-light"
            @click="cancel">
            <span class="icon">
              <i class="fa fa-ban"/>
            </span>
            <span>Cancel</span>
          </button>
        </p>

        <p
          v-if="entityId != '@new'"
          class="control">
          <nuxt-link
            :to="linkToDelete(entityId)"
            class="button is-light">
            <span class="icon">
              <i class="fa fa-trash"/>
            </span>
            <span>Delete</span>
          </nuxt-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import CrudLinksComponentMixin from '@/components/CrudLinksComponentMixin';
import CrudEditComponents from '@/lib/crud/components/edit';
import mass from '@/lib/crud/mass';

export default {
  layout: 'dashboard',
  components: CrudEditComponents,
  mixins: [
    CrudLinksComponentMixin
  ],
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
        const snackbarNamestoShow = {
          proposals: 'proposal', laws: 'law', meetings: 'meeting', zones: 'zone', officials: 'official', roles: 'role', users: 'user', comments: 'comment', workflowStages: 'workflowstage', workflowtypes: 'workflowtype'
        };
        const snackBarName = snackbarNamestoShow[entities.toLowerCase()] || 'record';
        if (this.entityId === '@new') {
          this.$snackbar.open({ message: `New ${snackBarName} has been created` });
        } else {
          this.$snackbar.open({ message: `The ${snackBarName} has been updated` });
        }
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
    },

    ondelete() {
      const deleteLink = this.linkToDelete(22);
      this.$router.go(deleteLink);
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
