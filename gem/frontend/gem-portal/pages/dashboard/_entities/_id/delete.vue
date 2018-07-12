<template>
  <div class="content center">
    <div v-if="entity">
      <h1>Delete</h1>
      <p>Are you sure you want to delete?</p>
      <a
        :class="{'is-loading': busy}"
        class="button is-danger"
        @click="remove">
        Confirm
      </a>
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
  methods: {
    async remove() {
      try {
        this.busy = true;
        const id = this.entity._id;
        await this.$store.dispatch(this._storeMethod('remove'), { id });

        this.$router.push(this._url());
        this.$snackbar.open({ message: 'Record has been deleted' });
      } finally {
        this.busy = false;
      }
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
