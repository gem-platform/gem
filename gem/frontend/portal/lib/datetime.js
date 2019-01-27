/* Library to manipulate Date object */
import moment from 'moment';

export const diff = (start, end) => {
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
};

export const getDateTime = (date, time) =>
  moment(date)
    .startOf('day')
    .add(time.getHours(), 'hours')
    .add(time.getMinutes(), 'minutes')
    .utcOffset(-0, true)
    .toISOString();

export const isStartDateBefore = (dateFields) => {
  const start = moment(getDateTime(dateFields.startDate, dateFields.startTime));
  const end = moment(getDateTime(dateFields.endDate, dateFields.endTime));

  return !start.isAfter(end, 'day');
};

export const isDifferentDayOrStartTimeBefore = (dateFields) => {
  const start = moment(getDateTime(dateFields.startDate, dateFields.startTime));
  const end = moment(getDateTime(dateFields.endDate, dateFields.endTime));

  return !start.isSame(end, 'day') || start.isBefore(end);
};
