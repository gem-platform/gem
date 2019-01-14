<template>
  <div>
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
          {{ user(comment.user).name }}
        </span>
        <!--<span
          v-for="(roleId, idx) in user(comment.user).roles"
          :key="idx">{{ role(roleId).name }}
        </span>-->
        <button
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

        <textarea
          v-if="isInEditMode(comment._id)"
          :value="comment.content"
          class="textarea inline-textarea"
          @input="onContentEdit(comment, $event.target.value)"
          @blur="setEditMode(comment._id, false)"/>
        <span v-else>{{ comment.content }}</span>
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
import NotificationMixin from '@/components/NotificationMixin';
import _ from 'lodash';


export default {
  mixins: [NotificationMixin],
  layout: 'dashboard',
  data() {
    return {
      selectedIds: [],
      editingIds: {}
    };
  },
  computed: {
    comments() {
      return this.$store.getters['dashboard/comments/list'];
    },

    /**
     * Return list of selected comments
     */
    selectedComments() {
      return _.filter(
        this.comments,
        x => _.includes(this.selectedIds, x._id)
      );
    }
  },
  methods: {
    user(id) {
      return this.$store.getters['dashboard/users/keyed'][id];
    },
    role(id) {
      return this.$store.getters['dashboard/roles/keyed'][id];
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
      if (this.selectedIds.length === 0) {
        this.notify('Nothing selected to merge');
        return;
      }

      // get list of authors
      const comments = _.chain(this.selectedComments);
      const authors = comments.map(x => x.user).uniq().value();
      const mergedContent = comments.map(c => c.content).value().join('\n \n ');
      const authorNames = _.chain(authors).map(id => this.user(id)).map(user => user.name).join(', ')
        .value();
      const isOneAuthor = authors.length === 1;
      const isSameMark = comments.map(x => x.mark).uniq().value().length === 1;
      const errors = [];

      if (!isOneAuthor) { errors.push(`These comments are of multiple authors: ${authorNames}.`); }
      if (!isSameMark) { errors.push('These comments have different marks.'); }

      if (errors.length > 0) {
        const errorsString = errors.join('\n');
        this.showMergeWarning(`${errorsString}\n Merge it anyway?`);
      }

      // create new comment based on selected
      this.$store.dispatch('dashboard/comments/save', {
        user: authors[0], // todo: how to merge comments of multiple authors?
        mark: this.selectedComments[0].mark, // todo: how to merge content with different marks?
        stage: this.selectedComments[0].stage, // todo: how to merge commments of different stages?
        proposal: proposalId,
        content: mergedContent
      });

      // remove selected one by one
      this.selectedIds.forEach((x) => {
        this.$store.dispatch('dashboard/comments/remove', { id: x });
      });

      this.clearSelection();
    },

    showMergeWarning(message) {
      this.$dialog.confirm({
        title: 'Merge comments',
        message,
        confirmText: 'Merge',
        type: 'is-danger',
        hasIcon: true,
        onConfirm: () => this.$toast.open('Account deleted!')
      });
    },

    isInEditMode(commentId) {
      return this.editingIds[commentId] === true;
    },

    setEditMode(commentId, value) {
      this.$set(this.editingIds, commentId, value);
    },

    onContentEdit(comment, value) {
      this.$store.dispatch('dashboard/comments/update', { _id: comment._id, content: value });
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

