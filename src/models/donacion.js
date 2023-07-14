const mongoose = require("mongoose");

const donacionSchema = mongoose.Schema({
  id_donacion: {
    type: String,
    required: true,
    unique: true
  },
  donador_id: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "Donador",
    required: true
  },
  medico_id: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "Medico",
    required: true
  },
  tipo_sangre_id: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "TipoSangre",
    required: true
  },
  bolsa_sangre_id: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "BolsaSangre",
    required: true
  },
  fecha_donacion: {
    type: Date,
    required: true
  }
});

module.exports = mongoose.model('Donacion', donacionSchema);

