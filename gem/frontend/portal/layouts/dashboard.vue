<template>
  <div>
    <Navbar/>

    <div class="main-section">
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
import Navbar from '@/components/Navbar.vue';
import DashboardPanel from '@/components/DashboardPanel.vue';

export default {
  components: {
    Navbar,
    DashboardPanel
  }
};
</script>
