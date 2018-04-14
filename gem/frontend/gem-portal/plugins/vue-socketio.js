import Vue from 'vue';
import VueSocket from 'vue-socket.io';
import sockets from '@/lib/socket';

export default context => {
  if (process.browser) {
    Vue.use(VueSocket, '/');
    Vue.options.sockets = sockets(context.store);
  }
};
