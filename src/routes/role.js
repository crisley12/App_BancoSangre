const express = require("express");

const router = express.Router(); //enrutador

const roleSchema = require("../models/role");
// create role
router.post("/roles", (req, res) => {
  // res.send("create role");
  const role = roleSchema(req.body);
  role
    .save()
    .then((data) => res.json(data))
    .catch((error) => res.json({ message: error }));
});

//get obtener todos los usuarios
router.get("/roles", (req, res) => {
  roleSchema
    .find()
    .then((data) => res.json(data))
    .catch((error) => res.json({ message: error }));
});

// get encontrar usuario especifico

router.get("/roles/:id", (req, res) => {
  const { id } = req.params;
  roleSchema
    .findById(id)
    .then((data) => res.json(data))
    .catch((error) => res.json({ message: error }));
});

// put actualizar usuario
router.put("/roles/:id", (req, res) => {
  const { id } = req.params;
  const { nombre, rol } = req.body;
  roleSchema
    .updateOne(
      { _id: id },
      {
        $set: {
          nombre,
          rol,
        },
      }
    )
    .then((data) => res.json(data))
    .catch((error) => res.json({ message: error }));
});

// delete usuario
router.delete("/roles/:id", (req, res) => {
  const { id } = req.params;
  roleSchema
    .deleteOne({ _id: id })
    .then((data) => res.json(data))
    .catch((error) => res.json({ message: error }));
});

module.exports = router;
