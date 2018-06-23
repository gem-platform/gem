import Vue from 'vue';
import VueSocket from 'vue-socket.io-extended';
import sockets from '@/lib/socket';
import io from 'socket.io-client';

export default (context) => {
  if (process.browser) {
    Vue.use(VueSocket, io('/'));
    Vue.options.sockets = sockets(context.store);
  }
};
