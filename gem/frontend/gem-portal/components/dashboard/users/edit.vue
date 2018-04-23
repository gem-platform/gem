<template>
  <div>
    <b-field label="Name">
      <b-input
        v-model="entity.name"
        placeholder="Name"
        size="is-large"/>
    </b-field>

    <b-field label="Password">
      <b-input
        v-model="entity.password"
        placeholder="Password"/>
    </b-field>

    <b-field label="Roles">
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
        @input="onInput">
        <template
          slot="tag"
          slot-scope="props">
          <span class="tag is-primary ctag">
            {{ props.option.name }}
            <button
              class="delete is-small"
              @click.prevent="props.remove(props.option)"/>
          </span>
        </template>
      </multiselect>
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
      return this.$store.getters['dashboard/roles/all'];
    }
  },
  async beforeCreate() {
    await this.$store.dispatch('dashboard/roles/fetch');

    if (!this.entity.roles) {
      return;
    }

    const roles = this.$store.getters['dashboard/roles/all'].filter(x =>
      this.entity.roles.includes(x._id));
    this.value = roles;
  },
  methods: {
    onInput(value) {
      this.entity.roles = value.map(x => x._id);
    }
  }
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style scoped>
.ctag {
  margin-right: 5px;
  margin-bottom: 5px;
}
</style>
