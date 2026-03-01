<template>
  <div class="centered">
      <button class="fa fa-play btn btn-ghost" @click="play()"></button>
  </div>
</template>

<script>
import * as api from "../api.js";

export default {
    data() {
        return {
            tracks: null,
            track: null,
        }
    },
    async mounted() {
        this.tracks = await api.get_tracks();
    },
    methods: {
      play() {
        this.track = this.tracks[Math.floor(Math.random() * this.tracks.length)]
        this.$store.commit('set_track', this.track)
      }
    }
}
</script>
