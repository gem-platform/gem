import Vue from 'vue';
import io from 'socket.io-client';

export default () => {
  if (process.browser) {
    Vue.prototype.$socket = io('/');
  }
};
