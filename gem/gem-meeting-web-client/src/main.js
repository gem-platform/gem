import 'buefy/lib/buefy.css';

import Vue from 'vue';
import Buefy from 'buefy';
import VueBus from 'vue-bus';
import VueSocket from 'vue-socket.io';
import App from './App.vue';
import store from './store';
import sockets from './socket';

Vue.use(Buefy);
Vue.use(VueBus);
Vue.use(VueSocket, 'http://localhost:8090', store);

Vue.config.productionTip = false;

new Vue({
  sockets,
  store,
  render: h => h(App)
}).$mount('#app');
