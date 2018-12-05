<template>
  <div>
    <!-- Commenting popup -->
    <div
      v-show="showCommentPopup"
      ref="commentPopup"
      class="comment-popup">

      <small
        v-if="commentPopup.roles"
        class="heading has-text-centered">
        {{ commentPopup.user }}
        ({{ commentPopup.roles.join(', ') }})
        <br>
      </small>

      <b-message
        v-if="commentPopup.quote"
        class="message is-small">
        {{ commentPopup.quote.text }}
      </b-message>
      {{ commentPopup.content }}
    </div>

    <!-- Proposal content -->
    <div
      id="proposal-content"
      ref="proposalContent"
      :class="{'in-parts-reader': mode=='in-parts'}"
      @mouseup="selectionChange"
      v-html="proposal.content"/>

    <!-- "Show more" button -->
    <br>
    <a
      v-if="mode == 'in-parts'"
      :class="moreButtonClass()"
      class="button is-fullwidth"
      @click="more">
      {{ moreButtonTitle() }}
    </a>
  </div>
</template>

<script>
import CommunicationMixin from '@/components/CommunicationMixin';
import StageStateMixin from '@/components/meeting/stages/StageStateMixin';

function get(node, result, level) {
  const levelpad = String(level).padStart(3, '0');
  if (level !== '') { result[levelpad] = node; }
  Array.from(node.childNodes).filter(x => (x.classList ? !x.classList.contains('quote') : true)).forEach((n, idx) => {
    const idxpad = String(idx).padStart(3, '0');
    get(n, result, level ? `${levelpad}-${idxpad}` : `${idxpad}`);
  });
  return result;
}

export default {
  mixins: [StageStateMixin, CommunicationMixin],
  props: {
    mode: {
      type: String,
      default() { return 'all'; }
    },
    comments: {
      type: Array,
      default() { return []; }
    }
  },
  data() {
    return {
      reveal: 10,
      showCommentPopup: false,
      commentPopup: ''
    };
  },
  computed: {
    /**
     * Proposal for current stage
     */
    proposal() {
      return this.stageProposal;
    }
  },
  watch: {
    $stage() {
      /** Stage changes, so we need to update inline comments */
      this.injectComments();
    }
  },
  mounted() {
    this.injectComments();
  },
  methods: {
    /**
     * Reveal more content
     */
    more() {
      this.reveal += 150;
      this.$refs.proposalContent.style.maxHeight = `${this.reveal}px`;

      const percents = this.percents();
      if (percents) {
        this.send('reading_progress', { quantity: percents / 100 });
      }
    },

    /**
     * Get title of the button
     */
    moreButtonTitle() {
      const value = this.percents();
      if (value < 100) { return `Read more (${value}% done)`; }
      if (value >= 100) { return 'I read'; }
      return 'Read More';
    },

    moreButtonClass() {
      const value = this.percents();
      if (value >= 100) { return 'is-success'; }
      return 'is-light';
    },

    percents() {
      if (!this.$refs.proposalContent) { return undefined; }
      if (!this.$refs.proposalContent.scrollHeight) { return undefined; }

      const max = this.$refs.proposalContent.scrollHeight;
      const current = Math.min(this.reveal, max);
      const percents = Math.floor((current / max) * 100);

      return percents;
    },

    /**
     * Injects comment marks to the document.
     */
    injectComments() {
      // step 1:
      // remove all the comment marks previously added.
      // all injected nodes have .quote class
      const paras = document.getElementsByClassName('quote');
      while (paras[0]) {
        paras[0].parentNode.removeChild(paras[0]);
      }

      // step 2:
      // convert raw comments data to human readable form:
      // - convert user ids to names
      // - convert roles ids to names
      const { users, roles } = this.$store.state.meeting;
      const cssType = { '+': 'is-success', '-': 'is-danger', i: 'is-info' };

      const comments = this.comments.map(c => ({
        user: users[c.user_id].name,
        roles: users[c.user_id].roles.map(r => roles[r].name),
        mark: c.mark,
        content: c.content,
        type: cssType[c.mark],
        quote: c.quote
      })).filter(c => c.quote && c.quote.begin);

      // step 3:
      const nodeIds = get(this.$refs.proposalContent, {}, '');
      comments.forEach((c) => {
        // create comment mark node
        const commentNode = document.createElement('span');
        commentNode.innerHTML = c.user;
        commentNode.setAttribute('class', `quote tag ${c.type}`);

        // show comment popup on click
        commentNode.addEventListener('click', (event) => {
          this.showCommentPopup = true;
          this.commentPopup = c;
          this.$refs.commentPopup.style.left = `${event.pageX}px`;
          this.$refs.commentPopup.style.top = `${event.pageY}px`;
        });

        // hide comment on mouse leave
        commentNode.addEventListener('mouseleave', () => {
          this.showCommentPopup = false;
        });

        // insert comment node
        const quoteBeginNode = nodeIds[c.quote.begin];
        if (quoteBeginNode && quoteBeginNode.parentNode) {
          quoteBeginNode.parentNode.insertBefore(commentNode, quoteBeginNode);
        }
      });
    },

    /**
     * Selection has changed.
     */
    selectionChange(event) {
      // step 1:
      // assign unique ID for each node from proposal:
      // (it also skips nodes with .quote css class, because
      //  injecting qutation mark nodes will change IDs)
      // 001     - <p>test</p>
      // 002     - <p>
      // 002-001 -    <b>nested</b>
      //         - </p>
      // 003     - <h1>header</h1>
      const nodeIds = get(this.$refs.proposalContent, {}, '');

      // step 2:
      // get nodes of selection (start and end)
      const startSel = window.getSelection().baseNode;
      const endSel = window.getSelection().extentNode;

      // step 3:
      // get ID (from step 1) of selection start/end nodes
      const ss = Object.keys(nodeIds).find(key => nodeIds[key] === startSel);
      const se = Object.keys(nodeIds).find(key => nodeIds[key] === endSel);

      // get selection text
      const text = window.getSelection().toString();

      // emit event
      this.$bus.emit('proposalSelection', {
        text,
        event,
        begin: { node: ss },
        end: { node: se }
      });
    }
  }
};
</script>

<style scoped>
.in-parts-reader {
  overflow: hidden;
  text-overflow: ellipsis;
  max-height: 100px;
  transition: all .5s;
}
.comment-popup {
  position: absolute;
  min-width: 200px;
  min-height: 100px;
  background-color: white;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid hsl(0, 0%, 86%);
  max-width: 350px;
  box-shadow: 2px 2px 2px rgba(0,0,0,.5);
}
</style>

<style>
.quote {
  padding-left: 5px;
  padding-right: 5px;
  margin-right: 5px;
  user-select: none;
  cursor: zoom-in;
}
.quote.is-success::before {
  content: "👍";
}
.quote.is-danger::before {
  content: "👎";
}
.quote.is-info::before {
  content: "💬";
}
</style>
