import Vue from 'vue';
import io from 'socket.io-client';

export default () => {
  if (process.browser) {
    Vue.prototype.$socket = io('/');

    // open_meeting is a global command, what doesn't belong
    // to any meeting
    Vue.prototype.$socket.on('open_meeting', (res) => {
      const newLocation = `/meeting/${res.meeting}`;
      const isLocationNotSame = window.location.pathname !== newLocation;
      const forceReload = res.force || false;

      if (res.success && (isLocationNotSame || forceReload)) {
        window.location = newLocation; // todo: do it more VUE-way
      }
    });
  }
};
