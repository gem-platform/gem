<template>
  <nav class="navbar is-light">
    <div class="container">
      <div class="navbar-brand">
        <span
          class="navbar-item brand-text">
          <img src="/gem-logo-small.svg">&nbsp;GEM
        </span>
        <div
          class="navbar-burger burger"
          @click="toggleMenu">
          <span/>
          <span/>
          <span/>
        </div>
      </div>
      <div
        :class="{'is-active': menuOpen}"
        class="navbar-menu">
        <div class="navbar-start">
          <nuxt-link
            class="navbar-item"
            to="/"
            active-class="is-active"
            exact>
            Schedule
          </nuxt-link>

          <nuxt-link
            v-if="haveAccess('dashboard')"
            class="navbar-item"
            to="/dashboard"
            active-class="is-active">
            Dashboard
          </nuxt-link>

          <nuxt-link
            v-if="haveAccess('laws')"
            class="navbar-item"
            to="/laws"
            active-class="is-active">
            Laws
          </nuxt-link>

          <nuxt-link
            v-if="haveAccess('meeting') && meetingJoined"
            :to="meetingLink"
            class="navbar-item"
            active-class="is-active"
            disabled>
            Meeting
            <span
              v-if="meetingAttentionRequired"
              class="icon has-text-danger">
              <i class="fa fa-exclamation blink_me"/>
            </span>
          </nuxt-link>
        </div>

        <div class="navbar-end">
          <b-dropdown
            v-if="authenticated"
            hoverable
            position="is-bottom-left">
            <a
              slot="trigger"
              class="navbar-item">
              <span>{{ user.name }}</span>
            </a>

            <b-dropdown-item has-link>
              <nuxt-link
                class="navbar-item"
                to="/logout">
                Logout
              </nuxt-link>
            </b-dropdown-item>
          </b-dropdown>

          <nuxt-link
            v-else
            class="navbar-item"
            to="/login">
            Login
          </nuxt-link>
        </div>
      </div>
  </div></nav>
</template>

<script>
import AuthMixin from '@/components/AuthMixin';

export default {
  mixins: [AuthMixin],
  data() {
    return {
      menuOpen: false
    };
  },
  computed: {
    meetingAttentionRequired() {
      return this.$store.getters['meeting/attentionRequired'];
    },
    meetingJoined() {
      return this.$store.state.meeting.id;
    },
    meetingLink() {
      const mid = this.$store.state.meeting.id;
      return !mid ? '/meeting' : `/meeting/${mid}`;
    }
  },
  methods: {
    toggleMenu() {
      this.menuOpen = !this.menuOpen;
    }
  }
};
</script>

<style scoped>
nav.navbar {
  border-top: 4px solid #7957d5;
  margin-bottom: 1rem;
}
.blink_me {
  animation: blinker 1s linear infinite;
}

@keyframes blinker {
  50% {
    opacity: 0;
  }
}
</style>
