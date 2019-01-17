<template>
  <div>
    <div class="field">
      <b-dropdown>
        <a
          slot="trigger"
          class="button">
          <span class="icon">
            <i class="fa fa-user"/>
          </span>
          <span>Stages: {{ filteredWorkflowStageName }}</span>
        </a>

        <!-- Show comments from all the stages -->
        <b-dropdown-item has-link>
          <a
            class="navbar-item"
            @click.prevent="selectWorkflowStage(undefined)">All
          </a>
        </b-dropdown-item>

        <!-- Show comment from specified stage of workflow -->
        <b-dropdown-item
          v-for="ws in workflowStages"
          :key="ws._id"
          has-link>
          <a
            class="navbar-item"
            @click.prevent="selectWorkflowStage(ws._id)">
            {{ ws.name }}
          </a>
        </b-dropdown-item>
      </b-dropdown>
    </div>

    <!-- There is no comment for proposal -->
    <b-message
      v-if="comments.length == 0"
      type="is-info">
      There is no comments for this propoposal.
    </b-message>

    <article
      v-for="comment in comments"
      :key="comment._id"
      :class="commentType(comment.mark)"
      class="message">

      <div class="message-header">
        <b-checkbox
          :type="commentType(comment.mark)"
          v-model="selectedIds"
          :native-value="comment._id" />

        <span class="user-name">
          {{ getUser(comment.user).name }}
        </span>
        <!--<span
          v-for="(roleId, idx) in user(comment.user).roles"
          :key="idx">{{ role(roleId).name }}
        </span>-->
        <button
          v-if="isInEditMode(comment._id)"
          :class="commentType(comment.mark)"
          class="button is-small is-inverted"
          @click="setEditMode(comment._id, false)">
          Save
        </button>
        <button
          v-else
          :class="commentType(comment.mark)"
          class="button is-small is-inverted"
          @click="setEditMode(comment._id, true)">
          Edit
        </button>
      </div>

      <div class="message-body">
        <blockquote
          v-if="comment.quote"
          class="is-italic quote">
          {{ comment.quote.text }}
        </blockquote>
        <span
          v-if="!isInEditMode(comment._id)">
          {{ comment.content }}
        </span>

        <div v-if="isInEditMode(comment._id)">
          <b-field label="Mood">
            <b-select
              :value="comment.mark"
              placeholder="Select a mood"
              expanded
              @input="onMarkEdit(comment, $event)">
              <option value="+">Plus</option>
              <option value="-">Minus</option>
              <option value="i">Info</option>
            </b-select>
          </b-field>

          <b-field label="Content">
            <textarea
              :value="comment.content"
              class="textarea inline-textarea"
              @input="onContentEdit(comment, $event.target.value)" />
          </b-field>
        </div>
      </div>
    </article>

    <!-- Control buttons -->
    <div
      v-if="comments.length > 0"
      class="buttons">
      <button
        class="button"
        @click="clearSelection">Clear selection</button>
      <button
        class="button"
        @click="merge">Merge</button>
      <button
        class="button is-danger"
        @click="remove">Delete</button>
    </div>
  </div>
</template>

<script>
import AuthMixin from '@/components/AuthMixin';
import NotificationMixin from '@/components/NotificationMixin';
import _ from 'lodash';


export default {
  mixins: [AuthMixin, NotificationMixin],
  layout: 'dashboard',
  data() {
    return {
      selectedIds: [],
      editingIds: {},
      workflowStage: undefined
    };
  },
  computed: {
    comments() {
      return _
        .chain(this.$store.getters['dashboard/comments/list'])
        .filter(c => c.stage === this.workflowStage || this.workflowStage === undefined)
        .value();
    },

    /**
     * Return list of selected comments
     */
    selectedComments() {
      return _.filter(
        this.comments,
        x => _.includes(this.selectedIds, x._id)
      );
    },

    workflowStages() {
      return this.$store.getters['dashboard/workflowStages/list'];
    },

    filteredWorkflowStageName() {
      if (this.workflowStage === undefined) { return 'All'; }
      return this.getWorkflowStage(this.workflowStage).name;
    }
  },
  methods: {
    /**
     * Get user model by ID.
     */
    getUser(id) {
      return this.$store.getters['dashboard/users/keyed'][id];
    },

    /**
     * Get role model by ID.
     */
    getRole(id) {
      return this.$store.getters['dashboard/roles/keyed'][id];
    },

    getWorkflowStage(id) {
      return this.$store.getters['dashboard/workflowStages/keyed'][id];
    },

    commentType(mark) {
      if (mark === 'i') return 'is-info';
      if (mark === '+') return 'is-success';
      if (mark === '-') return 'is-danger';
      return '';
    },

    /**
     * Clear all selection.
     */
    clearSelection() {
      this.selectedIds = [];
    },

    /**
     * Remove selected comments.
     */
    remove() {
      const itemsCount = this.selectedIds.length;

      // no items to remove
      if (itemsCount <= 0) {
        this.notify('Nothing selected to remove');
        return;
      }

      // remove one by one
      this.selectedIds.forEach((x) => {
        this.$store.dispatch('dashboard/comments/remove', { id: x });
      });

      // notify user
      this.notify(`${itemsCount} item(s) removed`, 'is-success');
      this.clearSelection();
    },

    /**
     * Merge selected comments into first one.
     */
    merge() {
      const proposalId = this.$route.params.id;

      // nothing selected to merge
      if (this.selectedIds.length < 2) {
        this.notify('Select at least two comments to merge.');
        return;
      }

      // get list of authors
      const currentUserName = this.user.name;
      const comments = _.chain(this.selectedComments);
      const authors = comments.map(x => x.user).uniq().value();
      const firstCommentMark = this.selectedComments[0].mark;
      const firstCommentStage = this.getWorkflowStage(this.selectedComments[0].stage);
      const mergedContent = comments.map(c => c.content).value().join('\n\n');
      const authorNames = _.chain(authors).map(id => this.getUser(id)).map(user => user.name).join(', ')
        .value();
      const isOneAuthor = authors.length === 1;
      const isSameMark = comments.map(x => x.mark).uniq().value().length === 1;
      const isSameStage = comments.map(x => x.stage).uniq().value().length === 1;
      const errors = [];

      if (!isOneAuthor) { errors.push(`Are of multiple authors: ${authorNames}. Author will be set to ${currentUserName}.`); }
      if (!isSameMark) { errors.push(`Have different moods. Mood will be set to: ${firstCommentMark}`); }
      if (!isSameStage) { errors.push(`Have different stages. Stage will be set to: ${firstCommentStage.name}`); }

      const perfomMerge = () => {
        // create new comment based on selected
        this.$store.dispatch('dashboard/comments/save', {
          user: isOneAuthor ? authors[0] : this.user.id,
          mark: firstCommentMark,
          stage: firstCommentStage._id,
          proposal: proposalId,
          content: mergedContent
        });

        // remove selected one by one
        this.selectedIds.forEach((x) => {
          this.$store.dispatch('dashboard/comments/remove', { id: x });
        });

        this.clearSelection();
      };

      if (errors.length > 0) {
        const errorsString = errors.map(x => `<li>${x}</li>`).join('\n');
        this.showMergeWarning(`These comments: <ul class='errors'>${errorsString}</ul> Merge it anyway?`, perfomMerge);
      } else {
        perfomMerge();
      }
    },

    showMergeWarning(message, callback) {
      this.$dialog.confirm({
        title: 'Merge comments',
        message,
        confirmText: 'Merge',
        type: 'is-danger',
        hasIcon: true,
        onConfirm: () => callback()
      });
    },

    selectWorkflowStage(stage) {
      this.workflowStage = stage;
    },

    isInEditMode(commentId) {
      return this.editingIds[commentId] === true;
    },

    setEditMode(commentId, value) {
      this.$set(this.editingIds, commentId, value);

      // Really save object
      if (value === false) {
        const entity = this.$store.getters['dashboard/comments/keyed'][commentId];
        this.$store.dispatch('dashboard/comments/save', entity);
      }
    },

    onContentEdit(comment, value) {
      this.$store.dispatch('dashboard/comments/update', { _id: comment._id, content: value });
    },

    onMarkEdit(comment, value) {
      this.$store.dispatch('dashboard/comments/update', { _id: comment._id, mark: value });
    }
  },

  async fetch(context) {
    const pid = context.params.id;

    // Fetch comments for proposal
    const comments = await context.store.dispatch(
      'dashboard/comments/fetchPage',
      { where: { proposal: pid } }
    );
    const userIds = _.chain(comments._items).map(x => x.user).uniq().value();
    const workflowStageIds = _.chain(comments._items).map(x => x.stage).uniq().value();

    // Fetch users
    if (userIds.length > 0) {
      const users = await context.store.dispatch('dashboard/users/fetchList', { ids: userIds });
      const roleIds = _.chain(users._items).map(x => x.roles).flatten().uniq()
        .value();

      await context.store.dispatch('dashboard/roles/fetchList', { ids: roleIds });
    }

    // Fetch workflow stages
    if (workflowStageIds.length > 0) {
      await context.store.dispatch('dashboard/workflowStages/fetchList', { ids: workflowStageIds });
    }
  }
};
</script>

<style scoped>
.user-name {
  flex-basis: 100%;
}
.quote {
  padding-bottom: 0.5em;
}
</style>

