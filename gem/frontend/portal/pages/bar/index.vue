<template>
  <div>
    <div class="columns is-multiline">
      <div
        v-for="item in items"
        :key="item._id"
        class="column is-one-quarter">

        <div
          :class="{'is-success': order.includes(item._id)}"
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
              v-if="!order.includes(item._id)"
              href="#"
              class="card-footer-item"
              @click.prevent="add(item)">
              Add
            </a>
            <a
              v-if="order.includes(item._id)"
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
      order: [],
      completeOrder: false
    };
  },
  computed: {
    name() {
      return this.$auth.user.name;
    },
    items() {
      return this.$store.getters['dashboard/barItems/list'];
    }
  },
  methods: {
    add(item) {
      if (!this.order.includes(item._id)) {
        this.order.push({ id: item._id, name: item.name });
      }

      if (!this.completeOrder) {
        const { sendOrder } = this;
        this.completeOrder = true;

        this.$snackbar.open({
          message: 'Item added',
          actionText: 'Order',
          indefinite: true,
          onAction() {
            sendOrder();
          }
        });
      }
    },
    remove(item) {
      if (this.order.includes(item._id)) {
        this.order = this.order.filter(x => x.id !== item._id);
      }
    },
    sendOrder() {
      bar.emit('order', {
        name: this.name,
        items: this.order
      }, (res) => {
        if (res.success) {
          this.$snackbar.open({ message: 'Ordered' });
        }

        this.completeOrder = false;
        this.order = [];
      });
    }
  },
  async fetch({ store }) {
    await store.dispatch('dashboard/barItems/fetchPage');
  }
};
</script>

<style lang="scss" scoped>
.card.is-success {
  background-color: lightgreen;
}
.cover {object-fit: cover;}
</style>
