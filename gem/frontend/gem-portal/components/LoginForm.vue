<template>
  <div>
    <!-- GEM Logo -->
    <div class="logo">
      <img src="gem-logo-gray.svg">
    </div>

    <!-- Error message -->
    <transition name="fade">
      <b-message
        v-show="error"
        type="is-danger">
        {{ error }}
      </b-message>
    </transition>

    <!-- Control buttons -->
    <form @submit.prevent="submit">
      <!-- Login field -->
      <b-field
        :type="loginFieldType">
        <b-autocomplete
          v-model="login"
          :data="suggestions"
          placeholder="Name"
          size="is-large">
          <template slot="empty">No user found</template>
        </b-autocomplete>
      </b-field>

      <!-- Password field -->
      <b-field
        :type="passwordFieldType">
        <b-input
          ref="password"
          v-model="password"
          type="password"
          placeholder="Password"
          password-reveal/>
      </b-field>

      <!-- Login button -->
      <div class="field">
        <button
          :class="{'is-loading': busy}"
          type="submit"
          class="button is-fullwidth is-primary">
          Login
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import str from '@/lib/string';

export default {
  props: {
    logins: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      login: '',
      password: '',
      error: undefined,
      loginFieldType: '',
      passwordFieldType: ''
    };
  },
  computed: {
    busy() {
      return this.$store.state.auth.busy;
    },
    suggestions() {
      return this.logins.filter(l => str.contains(l, this.login));
    }
  },
  mounted() {
    this.login = localStorage.login || '';
  },
  methods: {
    async signIn() {
      try {
        await this.$auth.loginWith('local', {
          data: { login: this.login, password: this.password }
        });

        this.$emit('login', { success: true });
        this.error = undefined;
        localStorage.login = this.login;
      } catch (e) {
        this.error = 'Some error occured';
        const code = e.response.status;
        if (code === 401) {
          this.error = 'Wrong login/password';
          this.$emit('login', { success: false });
        }
      }
    },
    validate() {
      this.error = undefined;

      // no login provided
      if (!this.login) {
        this.loginFieldType = 'is-danger';
        this.error = 'Login and password required';
      } else {
        this.loginFieldType = 'is-success';
      }

      // wrong login
      if (!this.logins.includes(this.login)) {
        this.loginFieldType = 'is-danger';
        this.error = 'No specified login found';
      } else {
        this.loginFieldType = '';
      }

      // no password provided
      if (!this.password) {
        this.passwordFieldType = 'is-danger';
        this.error = 'Login and password required';
      } else {
        this.passwordFieldType = '';
      }

      const success = this.error === undefined;
      this.$emit('login', { success });
      return success;
    },
    submit() {
      const success = this.validate();
      if (success) {
        this.signIn();
      }
    }
  }
};
</script>

<style scoped>
.logo {
  padding: 20px;
  padding-top: 5px;
}
</style>
