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
        // the url should have this shape:
        // [youtube blabla]?v=[video id]&list=[playlist id]&[blabla]
        // we need to extract video and playlist id from that
        // for this, we use regex (because we are cool)
        const re = /.*\?v=(.*)&list=(.*)(?:&.*)?/
        const data = re.exec(this.playlistUrl);
        console.log(data[1], data[2]);
        this.$store.commit('set_track', data[1])
        this.$store.commit('set_playlist', data[2])
      }
    }
}
</script>
