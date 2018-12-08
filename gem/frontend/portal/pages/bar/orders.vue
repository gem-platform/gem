<template>
  <div>
    <b-table
      :data="orders"
      :columns="orderColumns">
      <!-- Columns -->
      <template slot-scope="props">
        <!-- Name column -->
        <b-table-column label="Name">
          {{ props.row.name }}
        </b-table-column>

        <b-table-column label="Order">
          {{ props.row.items | list }}
        </b-table-column>

        <b-table-column label="Done">
          <button
            class="button is-small is-dark"
            @click="done(props.row.id)">
            Done
          </button>
        </b-table-column>
      </template>
    </b-table>
    <button @click="refresh">Refresh</button>
  </div>
</template>

<script>
import io from 'socket.io-client';

const bar = io('/', { path: '/bar/socket.io' });


export default {
  layout: 'portal',
  filters: {
    list(value) {
      return value.map(x => x.name).join(', ');
    }
  },
  data() {
    return {
      orders: []
    };
  },
  computed: {
    items() {
      return this.$store.getters['dashboard/barItems/list'];
    },
    orderColumns() {
      return [
        { field: 'name', label: 'Name' },
        { field: 'items', label: 'Order' },
        { label: 'Done' }
      ];
    }
  },
  mounted() {
    bar.on('add_order', (data) => {
      this.orders.push(data);
    });

    this.refresh();
  },
  methods: {
    refresh() {
      bar.emit('orders', (data) => {
        this.orders = data;
      });
    },
    done(id) {
      bar.emit('done', { id }, (res) => {
        if (res.success) {
          this.orders = this.orders.filter(x => x.id !== id);
        }
      });
    }
  },
  async fetch({ store }) {
    await store.dispatch('dashboard/barItems/fetchPage');
  }
};
</script>
