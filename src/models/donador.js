const mongoose = require("mongoose");

const donadorSchema = mongoose.Schema({
  id_donador: {
    type: String,
    required: true,
    unique: true
  },
  paciente_id:{
    type: mongoose.Schema.Types.ObjectId,
    ref: "Paciente",
    required: true
  },
  hemoglobina: {
    type: Number,
    required: true
  },
});

module.exports = mongoose.model('Donador' ,donadorSchema);
