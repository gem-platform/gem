<template>
  <div>
    <!-- Name of the role -->
    <b-field label="Name">
      <b-input
        v-model="name"
        placeholder="Name"
        size="is-large"/>
    </b-field>

    <!-- Priority of the role -->
    <b-field label="Priority">
      <b-input
        v-model="priority"
        placeholder="Priority" />
    </b-field>

    <!-- List of permissions -->
    <label class="label">Permissions</label>
    <div
      v-for="(group, name) in permissionGroups"
      :key="name"
      class="notification">

      <!-- Permissions group -->
      <label class="label">{{ name }}</label>
      <div
        v-for="permission in group"
        :key="permission._id">
        <b-checkbox
          v-model="permissions"
          :native-value="permission._id"
          class="field">
          {{ permission.name }}
        </b-checkbox>
      </div>

    </div>
  </div>
</template>

<script>
import CrudEditComponentMixin from '@/components/CrudEditComponentMixin';
import security from '@/lib/security';
import _ from 'lodash';

export default {
  mixins: [
    CrudEditComponentMixin({
      properties: ['name', 'permissions', 'priority']
    })],
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  computed: {
    /**
     * Get grouped permissions
     */
    permissionGroups() {
      return _.groupBy(security.permissions, 'group');
    }
  }
};
</script>
