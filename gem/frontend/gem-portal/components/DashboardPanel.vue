<template>
  <aside class="menu">
    <p class="menu-label">
      General
    </p>
    <ul class="menu-list">
      <li>
        <nuxt-link
          to="/dashboard"
          active-class="is-active"
          exact>Home</nuxt-link>
      </li>
      <li v-if="haveAccess('dashboard.proposals')">
        <nuxt-link
          to="/dashboard/proposals"
          active-class="is-active">Proposals</nuxt-link>
      </li>
      <li v-if="haveAccess('dashboard.meetings')">
        <nuxt-link
          to="/dashboard/meetings"
          active-class="is-active">Meetings</nuxt-link>
      </li>
      <li v-if="haveAccess('dashboard.laws')">
        <nuxt-link
          to="/dashboard/laws"
          active-class="is-active">Laws</nuxt-link>
      </li>
    </ul>

    <p
      v-if="showAdministrationSection"
      class="menu-label">
      Administration
    </p>

    <ul
      v-if="showAdministrationSection"
      class="menu-list">
      <li v-if="haveAccess('dashboard.users')">
        <nuxt-link
          to="/dashboard/users"
          active-class="is-active">Users</nuxt-link>
      </li>
      <li v-if="haveAccess('dashboard.roles')">
        <nuxt-link
          to="/dashboard/roles"
          active-class="is-active">Roles</nuxt-link>
      </li>
    </ul>
  </aside>
</template>

<script>
import AuthMixin from '@/components/AuthMixin';

export default {
  name: 'DashboardPanel',
  mixins: [AuthMixin],
  computed: {
    showAdministrationSection() {
      return this.haveAccess('dashboard.users') || this.haveAccess('dashboard.roles');
    }
  }
};
</script>
