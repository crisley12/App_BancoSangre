const mongoose = require("mongoose");

const citaSchema = mongoose.Schema({
  id_cita: {
    type: String,
    required: true,
    unique: true
  },
  paciente_id: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "Paciente",
    required: true
  },
  medico_id: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "Medico",
    required: true
  },
  fechaHora: {
    type: Date,
    required: true
  },
  descripción: {
    type: String
  }
});

module.exports = mongoose.model('Cita' ,citaSchema);