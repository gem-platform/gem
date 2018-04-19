<template>
  <div class="box notification is-light">
    <div class="level">

      <div class="level-left">
        <div class="level-item">
          <div>
            <p class="heading">{{ subtitle }}</p>
            <p class="title">
              {{ title }}
            </p>
          </div>
        </div>
      </div>

      <div class="level-right">
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Timer</p>
            <p class="title">00:00</p>
          </div>
        </div>
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Till end</p>
            <p class="title">00:00</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MeetingScreenTopPanel',
  props: {
    title: {
      type: String,
      required: true
    },
    subtitle: {
      type: String,
      default: ''
    }
  }
};
</script>
