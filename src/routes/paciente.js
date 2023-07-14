const express = require("express");

const router = express.Router(); //enrutador

const pacienteSchema = require("../models/paciente");
// create paciente
router.post("/pacientes", (req, res) => {
  // res.send("create paciente");
  const paciente = pacienteSchema(req.body);
  paciente
    .save()
    .then((data) => res.json(data))
    .catch((error) => res.json({ message: error }));
});

//get obtener todos los usuarios
// router.get("/pacientes", (req, res) => {
//     pacienteSchema
//     .find()
//     .then((data) => res.json(data))
//     .catch((error) => res.json({ message: error}))
// });


// get encontrar un paciente especifico por su user_id para listar los datos del paciente 

router.get("/pacientes/:user_id", (req, res) => {
  const { user_id } = req.params;
  pacienteSchema
    .findOne({ user_id }) // Utilizar cedula como filtro en la consulta
    .then((data) => {
      if (data) {
        res.json(data); // Enviar el paciente encontrado como respuesta
      } else {
        res.json({ message: "Paciente no encontrado" });
      }
    })
    .catch((error) => res.json({ message: error }));
});

// get encontrar un paciente especifico por su cedula (Registro)

router.get("/pacientes/cedula/:cedula", (req, res) => {
  const { cedula } = req.params;
  pacienteSchema
    .findOne({ cedula }) // Utilizar cedula como filtro en la consulta
    .then((data) => {
      if (data) {
        res.json(data); // Enviar el paciente encontrado como respuesta
      } else {
        res.json({ message: "Paciente no encontrado" });
      }
    })
    .catch((error) => res.json({ message: error }));
});

// put actualizar usuario
router.put("/pacientes/:id", (req, res) => {
  const { id } = req.params;
  const {
    cedula,
    p_apellido,
    s_apellido,
    p_nombre,
    s_nombre,
    n_telefono,
    t_sangre,
    t_sexo,
    f_nacimiento,
  } = req.body;
  pacienteSchema
    .updateOne(
      { _id: id },
      {
        $set: {
          cedula,
          p_apellido,
          s_apellido,
          p_nombre,
          s_nombre,
          n_telefono,
          t_sangre,
          t_sexo,
          f_nacimiento,
        },
      }
    )
    .then((data) => res.json(data))
    .catch((error) => res.json({ message: error }));
});

// delete usuario
router.delete("/pacientes/:id", (req, res) => {
  const { id } = req.params;
  pacienteSchema
    .deleteOne({ _id: id })
    .then((data) => res.json(data))
    .catch((error) => res.json({ message: error }));
});

module.exports = router;
