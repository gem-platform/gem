<template>
  <div>
    <div class="notification">
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
      name="proposals-list"
      tag="article">
      <article
        v-for="comment in comments"
        :key="comment._id"
        class="media">
        <div class="media-content">
          <div class="content">
            <p>
              <strong>{{ comment.user }}</strong>&nbsp;
              <span class="tags">
                <b-tag
                  v-for="(role, idx) in comment.roles"
                  :key="idx">{{ role }}
                </b-tag>

              </span>
              <br>
              {{ comment.content }}
            </p>
          </div>
        </div>
        <div class="media-right">
          <b-tag :type="comment.type">{{ comment.mark | mark }}</b-tag>
        </div>
      </article>
    </transition-group>
  </div>
</template>

<script>
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';
import Roles from '@/components/Roles.vue';
import Marks from '@/components/Marks.vue';
import _ from 'lodash';

export default {
  name: 'CommentsStageView',
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
  data() {
    return { filterRoles: [], filterMarks: ['+', '-', 'i'] };
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
          type: cssType[c.mark]
        }))
        .filter(c =>
          _.intersection(this.filterRoles, c.role_ids).length > 0
          || this.filterRoles.length === 0)
        .filter(m => _.includes(this.filterMarks, m.mark) || this.filterMarks.length === 0);
    }
  },
  created() {
    const roles = this.comments.map(x => x.role_ids);
    this.filterRoles = _.chain(roles).flatten().uniq().value();
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
.proposals-list-move {
  transition: transform .5s;
}
.proposals-list-enter-active, .proposals-list-leave-active {
  transition: all 1s;
}
.proposals-list-enter, .proposals-list-leave-to {
  opacity: 0;
}
</style>
