const mongoose = require("mongoose");

const tipoSexoSchema = mongoose.Schema({
  id_sexo: {
    type: String,
    required: true,
    unique: true
  },
  Sexo: {
    type: String,
    required: true
  }
});

module.exports = mongoose.model('TipoSexo' ,tipoSexoSchema);
