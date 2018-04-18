<template>
  <div>
    <b-field label="Name">
      <b-input
        v-model="entity.name"
        placeholder="Name"
        size="is-large"/>
    </b-field>

    <b-field label="Permissions">
      <multiselect
        v-model="value"
        :options="options"
        :multiple="true"
        :close-on-select="false"
        :clear-on-select="true"
        :hide-selected="true"
        placeholder="Roles"
        label="name"
        track-by="_id"
        @input="onInput"/>
    </b-field>
  </div>
</template>

<script>
export default {
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      value: []
    };
  },
  computed: {
    options() {
      return [
        { _id: '*', name: 'Admin' },
        { _id: 'vote', name: 'Vote' },
        { _id: 'comment', name: 'Comment' },
        { _id: 'discuss', name: 'Discuss' },
        { _id: 'join', name: 'Join Session' },
        { _id: 'manage', name: 'Manage Session' }
      ];
    }
  },
  async created() {
    if (!this.entity.permissions) {
      return;
    }

    const roles = this.options.filter(x => this.entity.permissions.includes(x._id));
    this.value = roles;
  },
  methods: {
    onInput(value) {
      this.entity.permissions = value.map(x => x._id);
    }
  }
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
