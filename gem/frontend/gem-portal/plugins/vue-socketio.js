import Vue from 'vue';
import VueSocket from 'vue-socket.io';
import sockets from '@/lib/socket';

export default context => {
  if (process.browser) {
    const url = process.env.API_HOST || 'localhost';
    Vue.use(VueSocket, 'http://' + url);
    Vue.options.sockets = sockets;
  }
};
