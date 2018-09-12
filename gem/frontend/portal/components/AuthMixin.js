export default {
  methods: {
    haveAccess(scope) {
      if (!this.$auth.user) {
        return false;
      }
      return this.$auth.user.scopes.includes('*') || this.$auth.user.scopes.includes(scope);
    }
  },
  computed: {
    user() {
      return this.$auth.user;
    },
    authenticated() {
      return this.$auth.user !== undefined;
    }
  }
};

