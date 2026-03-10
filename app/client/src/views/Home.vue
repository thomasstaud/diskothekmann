<template>
    <div class="m-5">
        <input v-model="playlistUrl" class="input w-1/4" type="text" placeholder="Playlist URL" />
        <button class="btn" @click="loadPlaylist()">Load</button>
    </div>
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
            playlistUrl: null,
        }
    },
    async mounted() {
        this.tracks = await api.get_tracks();
    },
    methods: {
      play() {
        this.track = this.tracks[Math.floor(Math.random() * this.tracks.length)]
        this.$store.commit('set_track', this.track)
      },
      loadPlaylist() {
        // remove leading url bits (up to the equals sign)
        // notably, this doesn't break things if there are no leading url bits
        let eqPos = this.playlistUrl.indexOf('=') + 1;
        let playlistId = this.playlistUrl.substring(eqPos);
        this.$store.commit('set_playlist', playlistId)
      }
    }
}
</script>
