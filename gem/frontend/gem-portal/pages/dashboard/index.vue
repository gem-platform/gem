<template>
  <div>
    <!-- Editable switch -->
    <div class="field">
      <b-switch v-model="editable">
        Editable
      </b-switch>
    </div>

    <!-- List of days -->
    <transition-group
      name="events-list"
      tag="div">
      <div
        v-for="day in view"
        :key="day.date"
        class="box">

        <!-- Date field -->
        <div class="field is-grouped">
          <b-input
            :readonly="!editable"
            v-model="day.newDate"
            expanded
            placeholder="Date"
            size="is-large"
            @blur="onDateChanged(day.date, day.newDate, day.events)"/>
          <!-- Add new event to current day button -->
          <button
            v-if="editable"
            class="button is-large"
            @click="addEvent(day.date)">+</button>
        </div>

        <!-- List of events for specified day -->
        <transition-group
          name="events-list"
          tag="div">
          <div
            v-for="event in day.events"
            :key="event._id"
            :class="{'changed': isChanged(event._id)}"
            class="field is-grouped is-grouped-multiline">

            <!-- Start time -->
            <b-input
              v-model="event.start"
              :readonly="!editable"
              placeholder="Start"
              class="short"
              @blur="onEventChanged(event)"/>

            <!-- End time -->
            <b-input
              v-model="event.end"
              :readonly="!editable"
              placeholder="End"
              class="short"
              @blur="onEventChanged(event)"/>

            <!-- Title and type field -->
            <b-input
              v-model="event.title"
              :readonly="!editable"
              placeholder="Name"
              expanded
              @input="onEventChanged(event);"/>

            <!-- Delete event button -->
            <button
              v-if="editable"
              class="button"
              @click="removeEvent(event)">
              <span class="icon">
                <i class="fa fa-trash"/>
              </span>
            </button>
          </div>
        </transition-group>
      </div>
    </transition-group>

    <!-- Control buttons -->
    <div class="field is-grouped dashboard-controls">
      <!-- Add new day button -->
      <p class="control">
        <button
          class="button is-light"
          @click="addDay">Add day</button>
      </p>

      <!-- Save changes button -->
      <p class="control">
        <button
          class="button is-light"
          @click="save">Save</button>
      </p>
    </div>

  </div>
</template>

<script>
import * as moment from 'moment';
import _ from 'lodash';

export default {
  layout: 'dashboard',
  data() {
    const events = this.$store.getters['dashboard/meetings/all'].map(m => ({
      _id: m._id,
      title: m.title,
      date: moment.utc(m.start).format('YYYY/MM/DD'),
      start: moment.utc(m.start).format('HH:mm'),
      end: moment.utc(m.end).format('HH:mm'),
      type: m.type
    }));

    return {
      events,
      view: this.eventsView(events),
      editable: false,
      changes: {}
    };
  },
  computed: {
    eventsById() {
      return _.keyBy(this.events, '_id');
    },
    eventsByDate() {
      return _.groupBy(this.events, 'date');
    }
  },
  methods: {
    /**
     * Makes view representation of events.
     * { "date": "", events: [ list of events for specified date ] }
     */
    eventsView(events) {
      const eventDates = events.map(x => x.date);
      const uniqDates = _.chain(eventDates).uniq().sortBy(x => x).value();

      const res = uniqDates.map(date => ({
        date,
        newDate: date,
        events: _
          .chain(events)
          .filter(x => x.date === date)
          .sortBy('start')
          .value()
      }));

      return res;
    },

    /**
     * Is event changed?
     */
    isChanged(id) {
      return this.changes[id] === true;
    },

    /**
     * Date changed
     */
    onDateChanged(date, newDate, events) {
      // date not changed
      if (date === newDate) { return; }

      // set new date for events
      events.forEach((e) => {
        e.date = newDate;
        this.onEventChanged(e);
      });
    },

    /**
     * Event changed
     */
    onEventChanged(event, type) {
      // mark event as changed
      this.changes[event._id] = true;

      // there is no changes if new event deleted
      if (event._new && type === 'delete') {
        delete this.changes[event._id];
      }

      // update view
      this.view = this.eventsView(this.events);
    },

    /**
     * Add event to a day using specified dayIndex.
     * Also set start time equal to end time of last event.
     */
    addEvent(date) {
      const events = this.eventsByDate[date];
      const id = Math.random().toString(36).substr(2, 9);
      let start = '9:00';

      if (events) {
        const last = events[events.length - 1]; // get last event
        start = last ? last.end : ''; // get end time of last event
      }

      const event = {
        _new: true, _id: id, title: '', date, start
      };

      this.events.push(event);
      this.onEventChanged(event);
    },

    /**
     * Add new day using last date
     */
    addDay() {
      const last = _.maxBy(this.events, 'date');
      const date = last ? moment(last.date, 'YYYY/MM/DD') : moment();
      const next = date.add(1, 'days').format('YYYY/MM/DD');
      this.addEvent(next);
    },

    /**
     * Remove event from day using specified indexes
     */
    removeEvent(event) {
      const idx = _.findIndex(this.events, x => x._id === event._id);
      this.$delete(this.events, idx);
      this.onEventChanged(event, 'delete');
    },

    /**
     * Save changes
     */
    save() {
      const ids = Object.keys(this.changes);
      ids.forEach((id) => {
        const event = this.eventsById[id];

        if (event) {
          const { date, _new: isNew } = event;

          const data = Object.assign({}, _.omit(event, '_new', 'date', 'newDate'));
          data.start = moment.utc(`${date} ${event.start} +0000`, 'YYYY/MM/DD HH:mm Z').toDate();
          data.end = moment.utc(`${date} ${event.end} +0000`, 'YYYY/MM/DD HH:mm Z').toDate();

          if (!isNew) {
            this.$store.dispatch('dashboard/meetings/mutate', data);
          } else {
            delete data._id;
            this.$store.dispatch('dashboard/meetings/create', data);
          }
        } else {
          this.$store.dispatch('dashboard/meetings/remove', { id });
        }
      });
      this.changes = [];
    }
  },
  async fetch({ store }) {
    // Fetch all meetings
    await store.dispatch('dashboard/meetings/fetch');
  }
};
</script>

<style scoped>
.short {
  max-width: 75px;
  width: 75px;
}

.events-list-move {
  transition: transform .5s;
}
.events-list-enter-active, .events-list-leave-active {
  transition: all .5s;
}
.events-list-enter, .events-list-leave-to {
  opacity: 0;
  /*transform: translateX(30px);*/
}
.changed {
}
</style>
