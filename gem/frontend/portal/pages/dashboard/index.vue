<template>
  <div>
    <b-message
      v-if="partially.yes"
      title="The data is partially displayed"
      type="is-warning">
      Only last {{ partially.count }} meetings are displayed
    </b-message>

    <!-- Editable switch -->
    <div class="field">
      <b-switch
        id="editable"
        v-model="editable">
        Editable
      </b-switch>
    </div>

    <!-- List of days -->
    <transition-group
      name="events-list"
      tag="div">
      <div
        v-for="(day, di) in view"
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
            v-for="(event, ei) in day.events"
            :id="'event-'+di+'-'+ei"
            :key="event._id"
            class="field is-grouped">

            <!-- Start time -->
            <b-input
              v-model="event.start"
              :readonly="!editable"
              placeholder="Start"
              class="short"
              data-role="start"
              @blur="onEventChanged(event)"/>

            <!-- End time -->
            <b-input
              v-model="event.end"
              :readonly="!editable"
              placeholder="End"
              class="short"
              data-role="end"
              @blur="onEventChanged(event)"/>

            <!-- Title and type field -->
            <b-input
              v-model="event.title"
              :readonly="!editable"
              class="title"
              placeholder="Name"
              data-role="title"
              expanded
              @input="onEventChanged(event);"/>

            <!-- Delete event button -->
            <button
              v-if="editable"
              class="button"
              data-role="delete"
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
    <div
      v-if="editable"
      class="field is-grouped dashboard-controls">
      <!-- Add new day button -->
      <p class="control">
        <button
          id="add-day"
          class="button is-light"
          @click="addDay">Add day</button>
      </p>

      <!-- Save changes button -->
      <p class="control">
        <button
          id="save"
          :disabled="!hasChanges"
          class="button is-light"
          @click="save">Save</button>
      </p>
    </div>

  </div>
</template>

<script>
import NotificationMixin from '@/components/NotificationMixin';
import * as moment from 'moment';
import _ from 'lodash';

export default {
  layout: 'dashboard',
  mixins: [NotificationMixin],
  data() {
    const events = this.$store.getters['dashboard/meetings/list'].map(m => ({
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
    /**
     * Return events keyed by id
     */
    eventsById() {
      return _.keyBy(this.events, '_id');
    },

    /**
     * Return events keyed by date
     */
    eventsByDate() {
      return _.groupBy(this.events, 'date');
    },

    /**
     * Are there any changes?
     */
    hasChanges() {
      return Object.keys(this.changes).length > 0;
    },

    /**
     * Is data rendered
     */
    partially() {
      const meta = this.$store.getters['dashboard/meetings/meta'];
      return { yes: meta.total > meta.perPage, count: meta.perPage };
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
      this.$set(this.changes, event._id, true);

      // there is no changes if new event deleted
      if (event._new && type === 'delete') {
        this.$delete(this.changes, event._id);
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
            this.$store.dispatch('dashboard/meetings/update', data);
            this.$store.dispatch('dashboard/meetings/save', data);
          } else {
            delete data._id;
            this.$store.dispatch('dashboard/meetings/save', data);
          }
        } else {
          this.$store.dispatch('dashboard/meetings/remove', { id });
        }
      });

      // Show notification if some changes found
      const changesCount = ids.length;
      if (changesCount > 0) {
        this.notify(`${changesCount} event(s) updated`);
      } else {
        this.notify('No changes found', 'is-danger');
      }

      // Return back to readonly state
      this.changes = [];
      this.editable = false;
    }
  },
  async fetch({ store }) {
    // Fetch all meetings
    await store.dispatch('dashboard/meetings/fetchPage', { max_results: 50 });
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
}
</style>
