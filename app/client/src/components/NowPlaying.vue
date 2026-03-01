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
        <button @click="this.$store.commit('set_track', null)" class="fa fa-stop btn btn-ghost"></button>

        <div class="px-5">
            <span class="font-bold">{{ track.name }}</span> <br>
            <span>{{ track.artist }}</span>
        </div>
        <button v-if="video" @click="video = false" class="fa fa-caret-down btn btn-ghost text-2xl"></button>
        <button v-if="!video" @click="video = true" class="fa fa-caret-up btn btn-ghost text-2xl"></button>
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
            video: false,
            playing: null,
            loading: true
        }
    },
    methods: {
        async play_track() {
            let id = await api.get_video_id(this.track);
            console.log(id);
            this.url = `https://www.youtube.com/watch?v=${id}`;
            console.log(this.url);
        },
        onReady() {
            this.loading = false;
            this.playing = true;
            this.$refs.youtube.playVideo()
        },
        togglePause() {
            if (this.loading) return;

            if (this.playing) {
                this.$refs.youtube.pauseVideo()
            } else {
                this.$refs.youtube.playVideo()
            }
            this.playing = !this.playing;
        }
    },
    components: { YouTube },
    watch: {
       '$store.state.playingTrack': function() {
            this.track = this.$store.state.playingTrack
            this.play_track()
        }
    }
}
</script>