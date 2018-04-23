/* Library to manipulate Date object */

export default {
  stripTime(d) {
    const nd = new Date(d);
    nd.setHours(0);
    nd.setMinutes(0);
    nd.setMilliseconds(0);
    return nd;
  },
  parseIsoDatetime(dtstr) {
    const dt = dtstr.split(/[: T-]/).map(parseFloat);
    return new Date(dt[0], dt[1] - 1, dt[2], dt[3] || 0, dt[4] || 0, dt[5] || 0, 0);
  },
  toIso(date) {
    function pad(number) {
      if (number < 10) {
        return `0${number}`;
      }
      return number;
    }

    // eslint-disable-next-line
    return date.getFullYear() +
      '-' + pad(date.getMonth() + 1) +
      '-' + pad(date.getDate()) +
      'T' + pad(date.getHours()) +
      ':' + pad(date.getMinutes()) +
      ':' + pad(date.getSeconds()) +
      '.' + (date.getMilliseconds() / 1000).toFixed(3).slice(2, 5) +
      'Z';
  }
};
