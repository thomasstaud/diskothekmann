<template>
<div v-if="track != null" class="fixed card card-bordered p-5 bg-base-content text-base-100 shadow-xl w-2000 right-10 bottom-10">
    <YouTube 
        v-if="url != null"
        v-show="video"
        class="mb-5 rounded-lg"
        :src="url"
        @ready="onReady()"
        ref="youtube"/>

    <div class="flex justify-end">
        <button v-if="playing" @click="togglePause()" class="fa fa-pause btn btn-ghost text-xs"></button>
        <button v-if="!playing" @click="togglePause()" class="fa fa-play btn btn-ghost text-xs"></button>
        <button @click="skipAhead()" class="fa fa-forward btn btn-ghost text-xs"></button>

        <button @click="this.$store.commit('set_track', null)" class="fa fa-stop btn btn-ghost"></button>

        <div v-show="video" class="px-5">
            <span class="font-bold">{{ track.name }}</span> <br>
            <span>{{ track.artist }} - {{ track.year }}</span>
        </div>
        <button v-show="video" @click="video = false" class="fa fa-caret-down btn btn-ghost text-2xl"></button>
        <button v-show="!video" @click="video = true" class="fa fa-caret-up btn btn-ghost text-2xl"></button>
    </div>
</div>
</template>

<script>
import YouTube from 'vue3-youtube'
import * as api from "../api.js";

export default {
    data() {
        return {
            url: null,
            track: null,
            playlist: null,
            video: false,
            playing: null,
            loading: true
        }
    },
    methods: {
        async play_track() {
            this.playing = true;
            this.video = false;
            let id = await api.get_video_id(this.track);
            console.log(id);
            this.url = `https://www.youtube.com/watch?v=${id}`;
            console.log(this.url);
        },
        play_playlist() {
            this.playing = true;
        },
        onReady() {
            console.log("hans!");
            this.loading = false;
            this.playing = true;
            // this.$refs.youtube.playVideo();
            
            this.$refs.youtube.loadPlaylist(this.playlist);
            this.$refs.youtube.setShuffle(true);
        },
        togglePause() {
            if (this.loading) return;

            if (this.playing) {
                this.$refs.youtube.pauseVideo()
            } else {
                this.$refs.youtube.playVideo()
            }
            this.playing = !this.playing;
        },
        skipAhead() {
            let time = this.$refs.youtube.getCurrentTime()
            this.$refs.youtube.seekTo(time + 15);
        }
    },
    components: { YouTube },
    watch: {
       '$store.state.currentTrack': function() {
            this.track = this.$store.state.currentTrack
            if (!this.track) return;
            this.play_track()
        },
       '$store.state.currentPlaylist': function() {
            this.playlist = this.$store.state.currentPlaylist
            if (!this.playlist) return;
            this.play_playlist()
        },
    }
}
</script>