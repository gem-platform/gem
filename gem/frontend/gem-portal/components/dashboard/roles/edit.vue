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
        :group-select="true"
        select-label=""
        group-values="scopes"
        group-label="group"
        placeholder="Roles"
        label="name"
        track-by="_id"
        @input="onInput">
        <template
          slot="option"
          slot-scope="props">
          <div class="level">
            <span>{{ props.option.name || props.option.$groupLabel }}</span>
            <span class="has-text-grey role-description">{{ props.option.desc }}</span>
          </div>
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
      return [
        {
          group: 'Admin',
          scopes: [
            { _id: '*', name: 'Superuser', desc: 'Have full rights' }
          ]
        },
        {
          group: 'Dashboard',
          scopes: [
            { _id: 'dashboard', name: 'Access Dashboard', desc: 'Access Dashboard page' },
            { _id: 'dashboard.roles', name: 'Access Roles', desc: 'Access Roles page at dashboard' },
            { _id: 'dashboard.proposals', name: 'Access Proposals', desc: 'Access Proposals page at dashboard' },
            { _id: 'dashboard.users', name: 'Access Users', desc: 'Access Users page at dashboard' },
            { _id: 'dashboard.meetings', name: 'Access Meetings', desc: 'Access Meetings page at dashboard' },
            { _id: 'dashboard.laws', name: 'Access Laws', desc: 'Access Laws page at dashboard' }
          ]
        },
        {
          group: 'Meeting',
          scopes: [
            { _id: 'meeting', name: 'Access Meetings', desc: 'Access Meeting page' },
            { _id: 'meeting.vote', name: 'Vote' },
            { _id: 'meeting.comment', name: 'Comment' },
            { _id: 'meeting.discuss', name: 'Discuss' },
            { _id: 'meeting.join', name: 'Join Meeting' },
            { _id: 'meeting.manage', name: 'Manage Meeting' }
          ]
        }
      ];
    }
  },
  async created() {
    if (!this.entity.permissions) {
      return;
    }

    const flatroles = Array.prototype.concat.apply([], this.options.map(x => x.scopes));
    const roles = flatroles.filter(x => this.entity.permissions.includes(x._id));
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
