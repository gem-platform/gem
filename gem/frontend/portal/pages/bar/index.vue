<template>
  <div>
    <!-- Complete order -->
    <div class="columns">
      <div class="column">
        <button
          :disabled="orderIds.length == 0"
          class="button is-primary is-fullwidth"
          @click="completeOrder">
          Complete order
        </button>
      </div>
    </div>

    <div class="columns is-multiline">
      <div
        v-for="item in items"
        :key="item._id"
        class="column is-one-quarter">

        <div
          :class="{'is-success': orderIds.includes(item._id)}"
          class="card">
          <div class="card-image">
            <figure class="image is-4by3 cover">
              <img
                :src="'/media/'+item.image"
                class="cover"
                alt="Placeholder image">
            </figure>
          </div>
          <div class="card-content">
            <div class="media">
              <div class="media-content">
                <p class="title is-4">{{ item.name }}</p>
              </div>
            </div>

            <div class="content">
              {{ item.description }}
            </div>
          </div>

          <footer class="card-footer">
            <a
              v-if="!orderIds.includes(item._id)"
              href="#"
              class="card-footer-item"
              @click.prevent="add(item)">
              Add
            </a>
            <a
              v-if="orderIds.includes(item._id)"
              href="#"
              class="card-footer-item"
              @click.prevent="remove(item)">
              Remove
            </a>
          </footer>

        </div>
      </div>
    </div>

  </div>
</template>

<script>
import io from 'socket.io-client';

const bar = io('/', { path: '/bar/socket.io' });

export default {
  layout: 'portal',
  data() {
    return {
      order: []
    };
  },
  computed: {
    name() {
      return this.$auth.user.name;
    },
    items() {
      return this.$store.getters['dashboard/barItems/list'];
    },
    orderIds() {
      return this.order.map(x => x.id);
    }
  },
  methods: {
    add(item) {
      if (!this.orderIds.includes(item._id)) {
        this.order.push({ id: item._id, name: item.name });
      }
    },
    remove(item) {
      if (this.orderIds.includes(item._id)) {
        this.order = this.order.filter(x => x.id !== item._id);
      }
    },

    /**
     * Complete order. Send order to the server.
     */
    completeOrder() {
      bar.emit('order', {
        name: this.name,
        items: this.order
      }, (res) => {
        if (res.success) {
          this.$snackbar.open({ message: 'Ordered' });
        } else {
          this.$snackbar.open({ message: 'We are unable to process your order, sorry' });
        }

        this.order = [];
      });
    }
  },

  /**
   * Fetch all the bar items from server.
   */
  async fetch({ store }) {
    await store.dispatch('dashboard/barItems/fetchPage');
  }
};
</script>

<style lang="scss" scoped>
.card.is-success {
  background-color:lightyellow;
}
.cover {object-fit: cover;}
</style>
