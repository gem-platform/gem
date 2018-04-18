<template>
  <aside class="menu">
    <p class="menu-label">
      General
    </p>
    <ul class="menu-list">
      <li><nuxt-link
        to="/dashboard"
        active-class="is-active"
        exact>Home</nuxt-link></li>
      <li>
        <nuxt-link
          to="/dashboard/proposals"
          active-class="is-active">Proposals</nuxt-link>
      </li>
      <li><a>Meetings</a></li>
      <li><a>Laws</a></li>
    </ul>

    <p class="menu-label">
      Administration
    </p>

    <ul class="menu-list">
      <li>
        <nuxt-link
          to="/dashboard/users"
          active-class="is-active">Users</nuxt-link>
      </li>
      <li><a>Roles</a></li>
      <li><a>Tokens</a></li>
    </ul>
  </aside>
</template>

<script>
export default {
  name: 'DashboardPanel'
};
</script>
