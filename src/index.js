//codigo del servidor
const express = require("express");
const mongoose = require("mongoose");
require("dotenv").config();
const userRoutes = require("./routes/user");
const pacienteRoutes = require("./routes/paciente");
const roleRoutes = require("./routes/role");
//const tipoSangreRoutes = require("./routes/tipoSangre");
//const tipoSexoRoutes = require("./routes/tipoSexo");

const app = express();
const port = process.env.PORT || 9000;

//middleware
app.use(express.json());
app.use("/api", userRoutes);
app.use("/api", pacienteRoutes);
app.use("/api", roleRoutes);
//app.use("/api", tipoSangreRoutes);
//app.use("/api", tipoSexoRoutes);

// routes
app.get("/", (req, res) => {
  res.send("Bienvenido a mi api");
});

// Mongodb connection
mongoose
  .connect(process.env.MONGODB_URI)
  .then(() => console.log("Conectado mongo db atlas"))
  .catch((error) => console.error(error));

app.listen(port, () => console.log("Servidor escuchando por el puerto", port));
