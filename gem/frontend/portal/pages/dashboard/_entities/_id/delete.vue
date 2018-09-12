<template>
  <div class="content center">
    <div v-if="entity">
      <h1>Delete</h1>
      <p>Are you sure you want to delete?</p>
      <div class="field is-grouped is-grouped-centered">
        <a
          :class="{'is-loading': busy}"
          class="button is-danger control"
          @click="remove">
          Confirm
        </a>
        <a
          class="button is-light control"
          @click="cancel">
          Cancel
        </a>
      </div>
    </div>
    <div v-else>
      Entity doesn't exist any more.
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      busy: false
    };
  },
  layout: 'dashboard',
  computed: {
    entity() {
      const { entities, id } = this.$route.params;

      const method = `dashboard/${entities}/keyed`;
      const getter = this.$store.getters[method];
      const entity = getter[id];

      return entity;
    }
  },
  methods: {
    async remove() {
      try {
        this.busy = true;
        const { entities, id } = this.$route.params;
        const method = `dashboard/${entities}/remove`;

        await this.$store.dispatch(method, { id });

        this.$router.push(`/dashboard/${entities}`);
        this.$snackbar.open({ message: 'Record has been deleted' });
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
      const method = `dashboard/${opt.params.entities}/fetchOne`;
      await opt.store.dispatch(method, opt.params.id);
    } finally {
      this.busy = false;
    }
  }
};
</script>

<style>
.center {
  display: flex;
  justify-content: center;
  height: 100%;
  align-items: center;
  text-align: center;
}
</style>
