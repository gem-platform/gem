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
  },
  diff(start, end) {
    let negative = false;
    let distance = end - start;

    if (distance < 0) {
      distance = start - end;
      negative = true;
    }


    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    return {
      days: Math.max(0, days),
      hours: Math.max(0, hours),
      minutes: Math.max(0, minutes),
      seconds: Math.max(0, seconds),
      distance,
      negative
    };
  }
};
