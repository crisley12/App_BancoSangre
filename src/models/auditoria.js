const mongoose = require("mongoose");
//esquema de usuario, si no lo cumple no funciona se hace por cada uno que tenga que hacer
const auditoriaSchema = mongoose.Schema({
    accion: {
        type: Number,
        required: true
    }, 
    id_dato: {
        type : Number,
        required: true
    },
    tabla: {
        type: String,
        required: true
    },
    modificaciones: {
        type: Number,
        required: false
    },
    id_usuario : {
        type: String,
        required: true
    },
    created_at : {
        type: Date,
        required: true
    },
    updated_at : {
        type: Date,
        required: true
    }
});

module.exports = mongoose.model('Auditoria' ,auditoriaSchema);