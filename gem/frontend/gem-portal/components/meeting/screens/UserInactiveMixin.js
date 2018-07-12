export default {
  computed: {
    _visibilityApi() {
      let hidden;
      let visibilityChange;

      if (typeof document.hidden !== 'undefined') { // Opera 12.10 and Firefox 18 and later support
        hidden = 'hidden';
        visibilityChange = 'visibilitychange';
      } else if (typeof document.msHidden !== 'undefined') {
        hidden = 'msHidden';
        visibilityChange = 'msvisibilitychange';
      } else if (typeof document.webkitHidden !== 'undefined') {
        hidden = 'webkitHidden';
        visibilityChange = 'webkitvisibilitychange';
      }

      return { hidden, visibilityChange };
    }
  },
  methods: {
    handleVisibilityChange() {
      const { hidden } = this._visibilityApi;
      this.$socket.emit('user_inactive', { value: document[hidden] });
    }
  },
  mounted() {
    const { hidden, visibilityChange } = this._visibilityApi;

    // Warn if the browser doesn't support addEventListener or the Page Visibility API
    if (!(typeof document.addEventListener === 'undefined' || hidden === undefined)) {
      document.addEventListener(visibilityChange, this.handleVisibilityChange, false);
    }

    this.$socket.emit('user_inactive', { value: false });
  },
  beforeDestroy() {
    const { visibilityChange } = this._visibilityApi;
    document.removeEventListener(visibilityChange, this.handleVisibilityChange);
  }
};

