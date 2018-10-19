<template>
  <aside class="menu">
    <p class="menu-label">
      General
    </p>
    <ul class="menu-list">
      <li>
        <nuxt-link
          to="/dashboard/search"
          active-class="is-active"
          exact>Search</nuxt-link>
      </li>
      <li>
        <nuxt-link
          to="/dashboard"
          active-class="is-active"
          exact>Schedule</nuxt-link>
      </li>
      <li v-if="haveAccess('dashboard.proposals')">
        <nuxt-link
          to="/dashboard/proposals"
          active-class="is-active">Proposals</nuxt-link>
      </li>
      <li v-if="haveAccess('dashboard.comments')">
        <nuxt-link
          to="/dashboard/comments"
          active-class="is-active">Comments</nuxt-link>
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
      class="menu-label">
      Workflow
    </p>
    <ul
      class="menu-list">
      <li v-if="haveAccess('dashboard.workflow')">
        <nuxt-link
          to="/dashboard/workflowTypes"
          active-class="is-active">Workflows</nuxt-link>
      </li>
      <li v-if="haveAccess('dashboard.workflow')">
        <nuxt-link
          to="/dashboard/workflowStages"
          active-class="is-active">Stages</nuxt-link>
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

    <p
      v-if="showAdministrationSection"
      class="menu-label">
      Zonal Assignments
    </p>

    <ul
      v-if="showAdministrationSection"
      class="menu-list">
      <li v-if="haveAccess('za.officials')">
        <nuxt-link
          to="/dashboard/officials"
          active-class="is-active">Officials</nuxt-link>
      </li>
      <li v-if="haveAccess('za.zones')">
        <nuxt-link
          to="/dashboard/zones"
          active-class="is-active">Zones</nuxt-link>
      </li>
    </ul>

    <p
      v-if="showAdministrationSection"
      class="menu-label">
      Reports
    </p>

    <ul
      v-if="showAdministrationSection"
      class="menu-list">
      <li v-if="haveAccess('za')">
        <nuxt-link
          to="/dashboard/reports/za"
          active-class="is-active">Zonal Assignments</nuxt-link>
      </li>
    </ul>

    <p
      v-if="showAdministrationSection"
      class="menu-label">
      Bar
    </p>

    <ul
      v-if="showAdministrationSection"
      class="menu-list">
      <li v-if="haveAccess('bar.manage')">
        <nuxt-link
          to="/dashboard/barItems"
          active-class="is-active">Bar</nuxt-link>
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
