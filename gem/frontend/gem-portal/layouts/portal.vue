<template>
  <div>
    <Navbar/>
    <br>

    <div class="container">
      <div class="columns">
        <div class="column is-2">
          <DashboardPanel/>
        </div>
        <div class="column is-10">
          <nuxt/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '~/components/Navbar';
import DashboardPanel from '~/components/DashboardPanel';

export default {
  components: {
    Navbar,
    DashboardPanel
  }
};
</script>
