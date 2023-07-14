const mongoose = require("mongoose");
//esquema de paciente, si no lo cumple no funciona se hace por cada uno que tenga que hacer
const userSchema = mongoose.Schema({
    nombre: {
        type: String,
        required: true
    }, 
    rol: {
        type: Number,
        required: true
    },
});

module.exports = mongoose.model('Role' ,userSchema);