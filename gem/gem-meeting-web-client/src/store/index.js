import Vue from 'vue';
import Vuex from 'vuex';
import meeting from './meeting';
import connection from './connection';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    meeting, connection,
  },
});
