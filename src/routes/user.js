const express = require("express");

const router = express.Router(); //enrutador

const userSchema = require("../models/user");
// create user
router.post("/users", (req, res) => {
  // res.send("create user");
  const user = userSchema(req.body);
  user
    .save()
    .then((data) => res.json(data))
    .catch((error) => res.json({ message: error }));
});

//get obtener todos los usuarios
// router.get("/users", (req, res) => {
//   userSchema
//     .find()
//     .then((data) => res.json(data))
//     .catch((error) => res.json({ message: error }));
// });

// get encontrar usuario especifico

// router.get("/users/:id", (req, res) => {
//   const { id } = req.params;
//   userSchema
//     .findById(id)
//     .then((data) => res.json(data))
//     .catch((error) => res.json({ message: error }));
// });

router.get("/users", (req, res) => {
  const { email, password } = req.query;
  userSchema
    .findOne({ email, password }) // Buscar por correo electrónico y contraseña
    .then((data) => {
      if (data) {
        res.json(data); // Enviar el usuario encontrado como respuesta
      } else {
        res.json({ message: "Usuario no encontrado" });
      }
    })
    .catch((error) => res.json({ message: error }));
});

// put actualizar usuario
router.put("/users/:id", (req, res) => {
  const { id } = req.params;
  const { email, password, paciente_id, rol_id } = req.body;
  userSchema
    .updateOne({ _id: id }, { $set: { email, password, paciente_id, rol_id } })
    .then((data) => res.json(data))
    .catch((error) => res.json({ message: error }));
});

// delete usuario
router.delete("/users/:id", (req, res) => {
  const { id } = req.params;
  userSchema
    .deleteOne({ _id: id })
    .then((data) => res.json(data))
    .catch((error) => res.json({ message: error }));
});

module.exports = router;
