<template>
    <div class="home">
        <!-- <img src="@/assets/flat-min.jpg" alt="Flat" id="flat_photo"> -->
        <img src="@/assets/flat-min.jpg" alt="Flat" id="flat_photo">

        <h3>Calculate price</h3>

        <select name="city" id="city" v-model="city">
            <option value="prague">Prague</option>
            <option value="brno">Brno</option>
        </select>

        <select id="type" v-model="type">
            <option value="0">- Choose flat type -</option>
            <option v-for="flat_type in flat_types" :value="flat_type.value" :key="flat_type.value">
                {{ flat_type.text }}
            </option>
        </select>

        <input type="text" placeholder="Size in m2" id="size" v-model="displayedSize" @blur="isSizeInputActive=false"
               @focus="isSizeInputActive=true">

        <select id="locality" v-model="locality">
            <option value="0">- Choose locality -</option>
            <option v-for="region in regions[city]" :value="region.value" :key="region.value">
                {{ region.text }}
            </option>
        </select>

        <button class="submit-button" type="button" @click="getPrice()">Get price</button>

        <div class="result">
            <h3 v-if="prediction != 0">Approximate price: {{ prediction }}</h3>
        </div>
        <div v-if="error">
            <h3>ERROR: Can't reach the server</h3>
        </div>
    </div>
</template>

<script>
    // @ is an alias to /src
    const axios = require('axios')

    export default {
        name: 'home',
        components: {},
        data() {
            return {
                flat_types: [
                    {text: '1+kt', value: 1},
                    {text: '1+1', value: 2},
                    {text: '2+kt', value: 3},
                    {text: '2+1', value: 4},
                    {text: '3+kt', value: 5},
                    {text: '3+1', value: 6},
                    {text: '4+kt', value: 7},
                    {text: '4+1', value: 8},
                    {text: '5+kt', value: 9},
                    {text: '5+1', value: 10},
                    {text: 'Flatshare', value: 11},
                    {text: 'Unusual', value: 12}
                ],
                regions: {
                    "prague": [
                        {text: 'Praha', value: 0},
                        {text: 'Praha 1', value: 1},
                        {text: 'Praha 2', value: 2},
                        {text: 'Praha 3', value: 3},
                        {text: 'Praha 4', value: 4},
                        {text: 'Praha 5', value: 5},
                        {text: 'Praha 6', value: 6},
                        {text: 'Praha 7', value: 7},
                        {text: 'Praha 8', value: 8},
                        {text: 'Praha 9', value: 9},
                        {text: 'Praha 10', value: 10},
                        {text: 'Praha 11', value: 11}],
                    "brno": [
                        {text: 'Brno - Jundrov', value: 1},
                        {text: 'Brno - Medlánky', value: 2},
                        {text: 'Brno - Trnitá', value: 3},
                        {text: 'Brno - Maloměřice', value: 4},
                        {text: 'Brno - Žabovřesky', value: 5},
                        {text: 'Brno - Bohunice', value: 6},
                        {text: 'Brno - Staré Brno', value: 7},
                        {text: 'Brno - Černovice', value: 8},
                        {text: 'Brno - Černá Pole', value: 9},
                        {text: 'Brno - Kohoutovice', value: 10},
                        {text: 'Brno - Pisárky', value: 11},
                        {text: 'Brno - Líšeň', value: 12},
                        {text: 'Brno - Královo Pole', value: 13},
                        {text: 'Brno - Bystrc', value: 14},
                        {text: 'Brno - Komín', value: 15},
                        {text: 'Brno - Veveří', value: 16},
                        {text: 'Brno - Židenice', value: 17},
                        {text: 'Brno - Zábrdovice', value: 18},
                        {text: 'Brno - Komárov', value: 19},
                        {text: 'Brno - Obřany', value: 20},
                        {text: 'Brno - Horní Heršpice', value: 21},
                        {text: 'Brno - Nový Lískovec', value: 22},
                        {text: 'Brno - Ponava', value: 23},
                        {text: 'Brno - Štýřice', value: 24},
                        {text: 'Brno - Ivanovice', value: 25},
                        {text: 'Brno - Řečkovice', value: 26},
                        {text: 'Brno - Husovice', value: 27},
                        {text: 'Brno - Lesná', value: 28},
                        {text: 'Brno - část obce Veveří', value: 29},
                        {text: 'Brno - Brno-Komín', value: 30},
                        {text: 'Brno - Brno-střed', value: 31},
                        {text: 'Brno - Brno-město', value: 32},
                        {text: 'Brno', value: 0}]
                },
                city: "prague",
                type: 0,
                size: 0,
                locality: 0,
                isSizeInputActive: false,
                prediction: 0,
                error: false
            }
        },
        methods: {
            getPrice() {
                const api_link = '/predict'

                axios.post(api_link, {
                    city: this.city,
                    type: this.type,
                    size: this.size,
                    locality: this.locality
                }).then((response) => {
                    this.error = false
                    this.prediction = response.data
                    this.prediction = Math.round(this.prediction)
                }).catch(() => this.error = true)
            }
        },
        computed: {
            displayedSize: {
                get: function () {
                    if (this.isSizeInputActive) {
                        return (this.size == 0) ? "" : this.size.toString()
                    } else {
                        return (this.size == 0) ? "" : this.size + " m2"
                    }
                },
                set: function (newValue) {
                    this.size = newValue
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
    h3 {
        margin: 10px;
    }

    #size {
        text-align: center;
        width: 5vw;
    }

    #flat_photo {
        max-width: 300px;
        border-radius: 15px;
        margin: 10px;
    }

    select, input {
        margin: 0 5px;
    }

    input {
        vertical-align: middle;
    }

    .submit-button {
        padding: 3px 5px;
        -webkit-border-radius: 15px;
        -moz-border-radius: 15px;
        border-radius: 15px;
        border: 1px #d0d0d0 solid;
        background-color: #fff;
    }
</style>