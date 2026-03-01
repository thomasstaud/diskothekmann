import axios from "axios";

export async function get_video_id(track) {
    let query = `${track.name} ${track.artist}`;
    const response = await axios.get(`http://localhost:5000/search_video?query=${query}`, {});
    return response.data;
}