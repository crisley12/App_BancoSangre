const mongoose = require("mongoose");

const bolsaSangreSchema = mongoose.Schema({
  id_bolsa: {
    type: String,
    required: true,
    unique: true
  },
  codigo: {
    type: String,
    required: true
  },
  cantidad: {
    type: Number,
    required: true
  },
  tipo_sangre_id: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "TipoSangre",
    required: true
  }
});

module.exports = mongoose.model('Bolsa', bolsaSangreSchema);
