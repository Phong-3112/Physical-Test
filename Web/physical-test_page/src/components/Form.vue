<template>
    <div class="form-stype-2">
            <div class="form-style-2-heading">Data Input</div>
            <form v-on:submit.prevent="submitForm">
                <label for="C">
                    <span>C 
                        <span class="required">*</span>
                    </span>
                </label>
                    <input type="number" class="input-field" name="C" v-model="form.C">
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
            <div>
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
            data: [],
            layout: {}
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

<style>
.form-style-2{
	max-width: 500px;
	padding: 20px 12px 10px 20px;
	font: 13px Arial, Helvetica, sans-serif;
}
.form-style-2-heading{
	font-weight: bold;
	font-style: italic;
	border-bottom: 2px solid #ddd;
	margin-bottom: 20px;
	font-size: 15px;
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