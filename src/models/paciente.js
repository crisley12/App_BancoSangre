const mongoose = require("mongoose");
//esquema de paciente, si no lo cumple no funciona se hace por cada uno que tenga que hacer
const userSchema = mongoose.Schema({
    cedula: {
        type: String,
        required: true
    }, 
    p_apellido: {
        type: String,
        required: true
    },
    s_apellido: {
        type: String,
        required: true
    },
    p_nombre: {
        type: String,
        required: true
    },
    s_apellido: {
        type: String,
        required: true
    },
    p_nombre: {
        type: String,
        required: true
    },
    n_telefono: {
        type: String,
        required: true
    },
    t_sangre: {
      type: String,
      required: true
    },
    t_sexo: {
        type: String,
        required: true
    },
    f_nacimiento: {
        type: String,
        required: true
    },
    user_id: {
        type: String,
        required: true
    },
});

module.exports = mongoose.model('Paciente' ,userSchema);