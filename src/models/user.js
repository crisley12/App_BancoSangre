const mongoose = require("mongoose");
//esquema de usuario, si no lo cumple no funciona se hace por cada uno que tenga que hacer
const userSchema = mongoose.Schema({
    email: {
        type: String,
        required: true
    }, 
    password: {
        type: String,
        required: true
    },
    rol_id : {
        type: Number,
        default: null
    }
});

module.exports = mongoose.model('User' ,userSchema);