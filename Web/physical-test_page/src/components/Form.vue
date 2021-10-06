<template>
    <div>
            <h2> Data Input </h2>
            <form v-on:submit.prevent="submitForm">
                <div class="form-group">
                    <label for="c">C</label>
                    <input type="number" class="form-control" id="c" placeholder="C" v-model="form.c">
                </div>
                <div class="form-group">
                    <label for="theta">theta</label>
                    <input type="number" class="form-control" id="theta" placeholder="theta" v-model="form.theta">
                </div>
                <div class="form-group">
                    <label for="Tmax">Tmax</label>
                    <input type="number" class="form-control" id="Tmax" placeholder="Tmax" v-model="form.Tmax">
                </div>
                <div class="form-group">
                    <label for="Wmax">Wmax</label>
                    <input type="number" step=0.01 class="form-control" id="Wmax" placeholder="Wmax" v-model="form.Wmax">
                </div>
                <div class="form-group">
                    <button class="btn btn-primary">Submit</button>
                </div>
            </form>
    </div>
</template>


<script>
import axios from 'axios';

export default {
    name: 'PostFormAxios',
    data(){
        return{
            form: {
                C: '20',
                theta: '40',
                Tmax: '40',
                Wmax: '0.5',
            }
        }
    },
    methods:{
        submitForm(){
            axios.post('http://127.0.0.1:5000/data', this.form)
                 .then((res) => {
                     //Perform Success Action
                     console.log(res.data.x_data)
                 })
                 .catch((error) => {
                     // error.response.status Check status code
                 }).finally(() => {
                     //Perform action in always
                 });
        }
    }
}
</script>