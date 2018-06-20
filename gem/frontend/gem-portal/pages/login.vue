<template>
  <section
    :class="background"
    class="hero is-fullheight">
    <div class="hero-body">
      <div class="column is-4 is-offset-4">
        <Spinner v-show="!show"/>

        <transition
          name="popup">
          <div
            v-show="show"
            :class="{'shake': shake}"
            class="box">
            <LoginForm
              :logins="logins"
              @login="onLogin"/>
          </div>
        </transition>
      </div>
    </div>
  </section>
</template>

<script>
import Spinner from '@/components/Spinner.vue';
import LoginForm from '@/components/LoginForm.vue';

export default {
  name: 'Login',
  components: { Spinner, LoginForm },
  data() {
    return {
      show: false,
      shake: false
    };
  },
  computed: {
    logins() {
      // get names only form users
      return this.$store.getters['dashboard/users/all'].map(x => x.name);
    },
    background() {
      const { backgroundId } = this.$store.state.config;
      return `bg-${backgroundId}`;
    }
  },
  mounted() {
    this.show = true;
  },
  methods: {
    onLogin({ success }) {
      this.shake = !success;
      setTimeout(() => { this.shake = false; }, 1000);

      if (success) {
        this.$router.push('/');
      }
    }
  },
  async fetch({ store }) {
    // fetch all of the users to make autocomplete
    // at login field possible
    await store.dispatch('dashboard/users/fetch');
  }
};
</script>

<style scoped>
.shake {
  animation: shake 1s cubic-bezier(.36,.07,.19,.97) both;
}

@keyframes shake {
  10%, 90% {
    transform: translate3d(-1px, 0, 0);
  }

  20%, 80% {
    transform: translate3d(2px, 0, 0);
  }

  30%, 50%, 70% {
    transform: translate3d(-4px, 0, 0);
  }

  40%, 60% {
    transform: translate3d(4px, 0, 0);
  }
}

.hero.bg-1 {
  background: linear-gradient(
      135deg,
      rgba(229, 58, 121, 0.5) 30%,
      rgba(254, 175, 18, 0.5) 70%
    ),
    url('/login-bg/bg1.jpg') no-repeat center center fixed;
  background-size: cover;
}
.hero.bg-2 {
  background: linear-gradient(
      135deg,
      rgba(229, 58, 121, 0.5) 30%,
      rgba(254, 175, 18, 0.5) 70%
    ),
    url('/login-bg/bg2.jpg') no-repeat center center fixed;
  background-size: cover;
}
.hero.bg-3 {
  background: linear-gradient(
      135deg,
      rgba(229, 58, 121, 0.5) 30%,
      rgba(254, 175, 18, 0.5) 70%
    ),
    url('/login-bg/bg3.jpg') no-repeat center center fixed;
  background-size: cover;
}
.hero.bg-4 {
  background: linear-gradient(
      135deg,
      rgba(229, 58, 121, 0.5) 30%,
      rgba(254, 175, 18, 0.5) 70%
    ),
    url('/login-bg/bg4.jpg') no-repeat center center fixed;
  background-size: cover;
}
</style>
