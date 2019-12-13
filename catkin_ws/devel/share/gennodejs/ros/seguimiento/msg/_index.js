
"use strict";

let ArrayFloat = require('./ArrayFloat.js');
let puntosCaras = require('./puntosCaras.js');
let audioDetectado = require('./audioDetectado.js');
let direccionAudio = require('./direccionAudio.js');
let entradaKalman = require('./entradaKalman.js');
let siguelinea = require('./siguelinea.js');
let nivelAudio = require('./nivelAudio.js');
let salidaRedCompetitiva = require('./salidaRedCompetitiva.js');
let entradaRedCompetitiva = require('./entradaRedCompetitiva.js');
let salidaKalman = require('./salidaKalman.js');
let ganador = require('./ganador.js');

module.exports = {
  ArrayFloat: ArrayFloat,
  puntosCaras: puntosCaras,
  audioDetectado: audioDetectado,
  direccionAudio: direccionAudio,
  entradaKalman: entradaKalman,
  siguelinea: siguelinea,
  nivelAudio: nivelAudio,
  salidaRedCompetitiva: salidaRedCompetitiva,
  entradaRedCompetitiva: entradaRedCompetitiva,
  salidaKalman: salidaKalman,
  ganador: ganador,
};
