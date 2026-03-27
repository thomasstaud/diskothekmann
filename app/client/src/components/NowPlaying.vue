<template>
<div v-if="track != null || playlist != null" class="fixed card card-bordered p-5 bg-base-content text-base-100 shadow-xl w-2000 right-10 bottom-10">
    <YouTube 
        v-if="url != null"
        v-show="video"
        class="mb-5 rounded-lg"
        :src="url"
        :vars="vars"
        @ready="on_player_ready()"
        @stateChange="on_state_change"
        ref="youtube"/>

    <div class="flex justify-end">
        <button v-if="playing" @click="toggle_pause()" class="fa fa-pause btn btn-ghost text-xs"></button>
        <button v-if="!playing" @click="toggle_pause()" class="fa fa-play btn btn-ghost text-xs"></button>
        <button @click="skip_ahead()" class="fa fa-forward btn btn-ghost text-xs"></button>
        <button @click="next()" class="fa fa-arrow-right btn btn-ghost text-xs"></button>

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
            track_id: null,
            playlist: null,
            from_playlist: false,
            video: false,
            playing: null,
            loading: true
        }
    },
    methods: {
        async play_track() {
            this.playing = true;
            this.video = false;

            this.track_id = await api.get_video_id(this.track);
            console.log("loading song...");
            console.log(this.track_id);
            this.url = `https://www.youtube.com/watch?v=${this.track_id}`;
            console.log(this.url);

            this.from_playlist = false;
        },
        async play_playlist() {
            this.playing = true;
            this.video = false;

            this.vars = {
                listType: 'playlist',
                list: this.playlist,
            }
            console.log("loading playlist...");
            console.log(this.playlist);
            console.log("with song:");
            console.log(this.track_id);
            
            this.track = await api.get_track_from_id(this.track_id);
            console.log(this.track_id);
            this.url = `https://www.youtube.com/watch?v=${this.track_id}&list=${this.playlist}`;
            console.log(this.url);

            this.from_playlist = true;
            this.skipping = true; // weird, but this helps
        },
        on_player_ready() {
            this.loading = false;
            this.playing = true;

            if (this.from_playlist) {
                this.$refs.youtube.loadPlaylist(this.playlist);
                this.$refs.youtube.setShuffle(true);
            }
            this.$refs.youtube.playVideo();
        },
        async on_state_change(state) {
            console.log("state changed!");
            // state 1 means a song has started playing
            if (!this.skipping || state.data != 1) return;
            console.log("...meaningfully!");

            // extract new video id and load track info
            let new_url = this.$refs.youtube.getVideoUrl();
            const re = /.*\?v=(.*)/
            this.track_id = re.exec(new_url)[1];
            this.track = await api.get_track_from_id(this.track_id);
            this.skipping = false;
        },
        toggle_pause() {
            if (this.loading) return;

            if (this.playing) {
                this.$refs.youtube.pauseVideo()
            } else {
                this.$refs.youtube.playVideo()
            }
            this.playing = !this.playing;
        },
        skip_ahead() {
            let time = this.$refs.youtube.getCurrentTime()
            this.$refs.youtube.seekTo(time + 15);
        },
        next() {
            this.playing = true;
            this.video = false;
            this.skipping = true;
            console.log("skipping!");

            this.$refs.youtube.setShuffle(true);
            this.$refs.youtube.nextVideo();
        }
    },
    components: { YouTube },
    watch: {
       '$store.state.track': function() {
            this.track = this.$store.state.track;
            if (!this.track) return;
            this.play_track()
        },
       '$store.state.playlist': function() {
            this.track_id = this.$store.state.track_id;
            this.playlist = this.$store.state.playlist;
            if (!this.playlist) return;
            this.play_playlist()
        },
    }
}
</script>