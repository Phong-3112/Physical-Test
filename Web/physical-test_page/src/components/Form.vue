<template>
    <div class="total-view">
        <form class="form-style-2" v-on:submit.prevent="submitForm">
            <h2 class="form-style-2-heading">Data Input</h2>
            <label>
                <span>C</span>
                <input type="number" class="input-field" name="C" v-model="form.C" required>
            </label>
            <label>
                <span>theta</span>
                <input type="number" class="input-field" name="theta" v-model="form.theta" required>
            </label>
            <label>
                <span>Tmax</span>
                <input type="number" class="input-field" name="Tmax" v-model="form.Tmax" required>
            </label>
            <label>
                <span>Wmax</span>
                <input type="number" step=0.01 class="input-field" name="Wmax" v-model="form.Wmax" required>
            </label>
            <button class="btn btn-primary">Show Graph</button>
        </form>
        <div class="form-style-3">
            <h2 class="form-style-2-heading">Output Graph</h2>
            <Graph :data="data" :layout="layout" />
        </div>
    </div>
</template>


<script>
import axios from 'axios';
import Graph from './Graph.vue'

export default {
    name: 'PostFormAxios',
    components: {
        Graph
    },
    data(){
        return{
            form: {
                C: '20',
                theta: '40',
                Tmax: '40',
                Wmax: '0.5',
            },
            data: [
                {
                    x: [],
                    y: [],
                    z: [],
                    type: 'surface'
                }
            ],
            layout: {
                width: 800,
                height: 600,
                showscale: false
            }
        }
    },
    methods:{
        submitForm(){
            axios.post('http://127.0.0.1:5000/data', this.form)
                .then((res) => {
                    //Perform Success Action
                    //console.log(res.data)
                    this.data = []
                    var x_data = JSON.parse(res.data.x_data)
                    var y_data = JSON.parse(res.data.y_data)
                    var z_data = JSON.parse(res.data.z_data)
                    var graphdata = {x: x_data, y: y_data, z: z_data, type: 'surface'}
                    //console.log(graphdata)
                    this.data.push(graphdata)
                })
                .catch((error) => {
                    // error.response.status Check status code
                    console.log('error: ',error)
                }).finally(() => {
                    //Perform action in always
                });
        }
    }
}
</script>

<style scoped>
.total-view{
    display: flex;
}
.form-style-2{
	max-width: 500px;
	padding: 20px 12px 10px 20px;
	font: 13px Arial, Helvetica, sans-serif;
    justify-content: space-between;
}
.form-style-3{
	padding: 20px 12px 10px 20px;
	font: 13px Arial, Helvetica, sans-serif;
    justify-content: space-between;
}
.input-field{
    max-width: 500px;
}
.form-style-2-heading{
	font-weight: bold;
	font-style: italic;
	border-bottom: 2px solid #ddd;
	margin-bottom: 20px;
	font-size: 20px;
	padding-bottom: 3px;
}
.form-style-2 label{
	display: block;
	margin: 0px 0px 15px 0px;
}
.form-style-2 label > span{
	width: 100px;
	font-weight: bold;
	float: left;
	padding-top: 8px;
	padding-right: 5px;
}
.form-style-2 span.required{
	color:red;
}
.form-style-2 input.input-field{
	width: 48%;	
}
.form-style-2 input.input-field{
	box-sizing: border-box;
	-webkit-box-sizing: border-box;
	-moz-box-sizing: border-box;
	border: 1px solid #C2C2C2;
	box-shadow: 1px 1px 4px #EBEBEB;
	-moz-box-shadow: 1px 1px 4px #EBEBEB;
	-webkit-box-shadow: 1px 1px 4px #EBEBEB;
	border-radius: 3px;
	-webkit-border-radius: 3px;
	-moz-border-radius: 3px;
	padding: 7px;
	outline: none;
}
.form-style-2 .input-field:focus{
	border: 1px solid #0C0;
}
</style>