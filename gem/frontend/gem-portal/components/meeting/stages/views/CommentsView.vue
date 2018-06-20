<template>
  <div>
    <!--
    <b-field label="Roles">
      <Roles :selected="commentsRoles"/>
    </b-field>
    -->

    <article
      v-for="comment in comments"
      :key="comment._id"
      class="media">
      <div class="media-content">
        <div class="content">
          <p>
            <strong>{{ comment.user }}</strong>&nbsp;
            <small>{{ comment.mark | mark }}</small>
            <br>
            {{ comment.content }}
          </p>
        </div>
      </div>
    </article>
  </div>
</template>

<script>
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';
import Roles from '@/components/Roles.vue';

export default {
  name: 'CommentsStageView',
  components: { Roles },
  filters: {
    mark(value) {
      if (value === '+') return 'Plus';
      if (value === '-') return 'Minus';
      if (value === 'i') return 'Info';
      return value;
    }
  },
  mixins: [StageStateMixin],
  computed: {
    comments() {
      return this.$stage.comments;
    },
    commentsRoles() {
      return [];
      // this.comments.map(x => x.user)
    }
  }
};
</script>
