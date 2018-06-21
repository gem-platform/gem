<template>
  <div class="content notification column is-6 is-offset-3 is-warning">
    <h1>Join a meeting</h1>
    <p>
      You are not joined any meeting yet. <br>
      Please join a meeting using your schedule page.
    </p>
    <nuxt-link
      to="/"
      class="button is-primary is-fullwidth">
      Go to schedule page
    </nuxt-link>
  </div>
</template>

<script>
export default {
  layout: 'portal'
};
</script>

<style scoped>
.center {
  display: flex;
  justify-content: center;
  height: 100%;
  align-items: center;
  text-align: center;
}
</style>
