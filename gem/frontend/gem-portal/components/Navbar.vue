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
            active-class="is-active">
            Meeting
            <span
              v-if="attention"
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
      menuOpen: false,
      attention: false,
      attentionToast: undefined
    };
  },
  computed: {
    meetingJoined() {
      return this.$store.state.meeting.id;
    },
    meetingLink() {
      const mid = this.$store.state.meeting.id;
      return !mid ? '/meeting' : `/meeting/${mid}`;
    },
    onMeetingPage() {
      return this.url.startsWith('/meeting');
    },
    url() {
      return this.$route.path;
    }
  },
  watch: {
    /**
     * On url changes
     */
    url() {
      // user returned back on meeting page after
      // attention requested
      if (this.attention && this.onMeetingPage) {
        this.attention = false;
        if (this.attentionToast) { this.attentionToast.close(); }
      }
    }
  },
  mounted() {
    this.$socket.on('stage', this.onStageData);
  },
  beforeDestroy() {
    this.$socket.off('stage', this.onStageData);
  },
  methods: {
    /**
     * Show
     */
    toggleMenu() {
      this.menuOpen = !this.menuOpen;
    },

    /**
     * On meeting stage data
     */
    onStageData() {
      const router = this.$router;
      const { meetingLink } = this;

      // user not at meeting page but something
      // happened at meeting, so request user to
      // return back to meeting
      if (!this.attention && !this.onMeetingPage) {
        this.attentionToast = this.$snackbar.open({
          message: 'Meeting attention required',
          type: 'is-danger',
          indefinite: true,
          actionText: 'Go',
          onAction() { router.push(meetingLink); }
        });
      }

      // set attention flag if user not at meeting page
      this.attention = !this.onMeetingPage;
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
