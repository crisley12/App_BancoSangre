const mongoose = require("mongoose");

const medicoSchema = mongoose.Schema({
  nombre: {
    type: String,
    required: true
  },
  apellido: {
    type: String,
    required: true
  },
  telefono: {
    type: String,
    required: true
  },
  ubicacion: {
    type: String,
    required: true
  },
  tipoSangre: {
    type: String,
    required: true
  },
  especialidad: {
    type: String,
    required: true
  },
  user_id: {
    type: String,
    required: true
  },
});

module.exports = mongoose.model('Medico' ,medicoSchema);
