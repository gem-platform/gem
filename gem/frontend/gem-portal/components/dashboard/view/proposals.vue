<template>
  <div>
    <h1>{{ entity.title }}</h1>
    <div v-html="entity.content"/>

    <hr>

    <article
      v-for="comment in comments"
      :key="comment._id"
      class="media">

      <div class="media-content">
        <!-- Content of the comment -->
        <div class="content">
          <!-- User's name -->
          <strong>{{ comment.user }}</strong>&nbsp;

          <!-- User's roles -->
          <span class="tags">
            <b-tag
              v-for="(role, idx) in comment.roles"
              :key="idx">{{ role }}
            </b-tag>

            <b-tag>
              <nuxt-link :to="comment.urlEdit">Edit</nuxt-link>
            </b-tag>
            <b-tag>
              <nuxt-link :to="comment.urlDelete">Delete</nuxt-link>
            </b-tag>
          </span>


          <!-- Content -->
          <br>
          {{ comment.content }}
        </div>
      </div>

      <!-- Mark -->
      <div class="media-right">
        <b-tag :type="comment.type">{{ comment.mark | mark }}</b-tag>
      </div>
    </article>
  </div>
</template>

<script>
import _ from 'lodash';

export default {
  filters: {
    mark(value) {
      if (value === '+') return 'Plus';
      if (value === '-') return 'Minus';
      if (value === 'i') return 'Info';
      return value;
    }
  },
  props: {
    entity: {
      type: Object,
      required: true
    }
  },
  computed: {
    comments() {
      const comments = this.$store.getters['dashboard/comments/list'];
      const users = this.$store.getters['dashboard/users/keyed'];
      const roles = this.$store.getters['dashboard/roles/keyed'];

      return comments
        .filter(x => x.proposal === this.$route.params.id)
        .map(x => ({
          _id: x._id,
          content: x.content,
          user: users[x.user].name,
          roles: users[x.user].roles.map(r => roles[r].name),
          mark: x.mark,
          urlEdit: `/dashboard/comments/${x._id}/edit`,
          urlDelete: `/dashboard/comments/${x._id}/delete`
        }));
    }
  },
  async fetch(opt) {
    //
    const pid = opt.params.id;

    // Fetch comments for proposal
    const comments = await opt.store.dispatch(
      'dashboard/comments/fetchPage',
      { where: { proposal: pid } }
    );
    const userIds = _.chain(comments._items).map(x => x.user).uniq().value();

    // Fetch users
    if (userIds.length > 0) {
      const users = await opt.store.dispatch('dashboard/users/fetchList', { ids: userIds });
      const roleIds = _.chain(users._items).map(x => x.roles).flatten().uniq()
        .value();

      await opt.store.dispatch('dashboard/roles/fetchList', { ids: roleIds });
    }
  }
};
</script>

<style scoped>
.tags {
  display: inline;
}
</style>
