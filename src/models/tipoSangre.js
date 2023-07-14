const mongoose = require("mongoose");

const tipoSangreSchema = mongoose.Schema({
  id_sangre: {
    type: String,
    required: true,
    unique: true
  },
  Sangre: {
    type: String,
    required: true
  },
});

module.exports = mongoose.model('TipoSangre' ,tipoSangreSchema);
