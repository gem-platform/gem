<template>
  <div>
    <p
      v-if="header"
      class="heading has-text-centered">
      {{ header }}
    </p>

    <!-- Filter -->
    <div
      v-if="filter"
      class="notification">
      <b-field label="Roles">
        <Roles
          :selected="filterRoles"
          @change="onRolesFilterChanged"/>
      </b-field>
      <b-field label="Marks">
        <Marks
          @change="onMarksFilterChanged"/>
      </b-field>
    </div>

    <transition-group
      v-if="comments"
      name="comments-list"
      tag="article">
      <article
        v-for="comment in comments"
        :key="comment._id"
        class="media">

        <div class="media-content">
          <!-- Content of the comment -->
          <div class="content">
            <p>
              <!-- User's name -->
              <strong>{{ comment.user }}</strong>&nbsp;

              <!-- User's roles -->
              <span class="tags">
                <b-tag
                  v-for="(role, idx) in comment.roles"
                  :key="idx">{{ role }}
                </b-tag>
              </span>

              <!-- Content -->
              <br>
              <b-message
                v-if="comment.quote"
                size="is-small">
                {{ comment.quote.text }}
              </b-message>
              {{ comment.content }}
            </p>
          </div>
        </div>

        <!-- Mark -->
        <div class="media-right">
          <b-tag :type="comment.type">{{ comment.mark | mark }}</b-tag>
        </div>
      </article>
    </transition-group>

    <div
      v-if="comments.length <= 0"
      class="has-text-centered">
      There is no comments
    </div>
  </div>
</template>

<script>
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';
import Roles from '@/components/Roles.vue';
import Marks from '@/components/Marks.vue';
import _ from 'lodash';
import arr from '@/lib/array';

function anyRolePresent(roles1, roles2) {
  return _.intersection(roles1, roles2).length > 0;
}

function anyMarkPresent(filter, value) {
  return _.includes(filter, value);
}

export default {
  components: { Roles, Marks },
  filters: {
    mark(value) {
      if (value === '+') return 'Plus';
      if (value === '-') return 'Minus';
      if (value === 'i') return 'Info';
      return value;
    }
  },
  mixins: [StageStateMixin],
  props: {
    filter: {
      type: Boolean,
      default: false
    },
    header: {
      type: String,
      default() { return 'Comments'; }
    }
  },
  data() {
    const roles = arr.unkey(this.$store.state.meeting.roles, 'id');
    return {
      filterRoles: roles.map(x => x.id),
      filterMarks: ['+', '-', 'i']
    };
  },
  computed: {
    comments() {
      const { users, roles } = this.$store.state.meeting;
      const cssType = { '+': 'is-success', '-': 'is-danger', i: 'is-primary' };

      return this.$stage.comments
        .map(c => ({
          _id: c._id,
          user: users[c.user_id].name,
          roles: users[c.user_id].roles.map(r => roles[r].name),
          role_ids: users[c.user_id].roles,
          mark: c.mark,
          content: c.content,
          type: cssType[c.mark],
          quote: c.quote
        }))
        // Filter out comments of users whose roles were not in the filter
        .filter(c => anyRolePresent(this.filterRoles, c.role_ids))
        // Filter out comments with mark not in the filter
        .filter(m => anyMarkPresent(this.filterMarks, m.mark));
    }
  },
  methods: {
    onRolesFilterChanged(value) {
      this.filterRoles = value;
    },
    onMarksFilterChanged(value) {
      this.filterMarks = value;
    }
  }
};

</script>

<style scoped>
.tags {
  display: inline;
}
.comments-list-move {
  transition: transform .5s;
}
.comments-list-enter-active, .comments-list-leave-active {
  transition: all .5s;
}
.comments-list-enter, .comments-list-leave-to {
  opacity: 0;
}
</style>
