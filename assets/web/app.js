// Constantes oficiales del proyecto
let ESTRUCTURA_PERSONAL = {
  "Rodrigo Bustamante": {
    zonas: ["Chiloé"],
    tecnicos: ["Roger Vargas", "Bernardo Guenteo", "Freddy Blanco", "Orlando Andres Garate", "Alejandro Mansilla"]
  },
  "Manuel Yovera": {
    zonas: ["Pto. Montt", "Hornopirén", "Seno Reloncaví", "Estuario Reloncaví", "Calbuco", "Valdivia", "Chaitén", "Ayacara"],
    tecnicos: ["Armando Perez", "Cristian Norambuena", "Yerson Seron"]
  },
  "Camilo Oyarzún": {
    zonas: ["Pto. Aguirre", "Pto. Chacabuco", "Pto. Aysén", "Pto. Cisnes"],
    tecnicos: ["Mariluz Tocol", "Leonardo Valenzuela", "Luis Oyarzun", "Heriberto Lira"]
  },
  "Francisco Vásquez": {
    zonas: ["Melinka", "Pto. Natales", "Pta. Arenas (PUQ)"],
    tecnicos: ["Carlos Rodriguez", "Carlos Salinas", "Eduin Campos", "Hayran Poveda", "Franco Quintallana", "Glenn Montiel", "Pablo Peréz"]
  }
};

const ENCARGADOS = {
  "Rodrigo Bustamante": ESTRUCTURA_PERSONAL["Rodrigo Bustamante"].tecnicos,
  "Manuel Yovera": ESTRUCTURA_PERSONAL["Manuel Yovera"].tecnicos,
  "Camilo Oyarzún": ESTRUCTURA_PERSONAL["Camilo Oyarzún"].tecnicos,
  "Francisco Vásquez": ESTRUCTURA_PERSONAL["Francisco Vásquez"].tecnicos
};

const EMPRESAS = [
  "Camanchaca", "AquaChile", "Mowi", "Cermaq", "Multiexport",
  "Abick", "Aquagen", "Salmones de Chile", "Blumar", "Ventisqueros",
  "Salmones Saysen", "Marine Farm", "Yadran", "Invermar", "Cooke",
  "Nova Austral", "Salmones Caleta Bay", "St-Andrews", "Salmones Magallanes",
  "Australis", "Aquasan", "Blu River", "Friosur", "Los Fiordos",
  "Salmones Austral", "Otro..."
];

const MAPA_ABREVIATURAS_EMPRESAS = {
  "st": { abbrev: "St", empresa: "St-Andrews" },
  "mw": { abbrev: "MW", empresa: "Mowi" },
  "sm": { abbrev: "SM", empresa: "Salmones Magallanes" },
  "au": { abbrev: "Au", empresa: "Australis" },
  "ca": { abbrev: "Ca", empresa: "Camanchaca" },
  "ce": { abbrev: "Ce", empresa: "Cermaq" },
  "mef": { abbrev: "Mef", empresa: "Multiexport" },
  "ab": { abbrev: "Ab", empresa: "Abick" },
  "ac": { abbrev: "AC", empresa: "AquaChile" },
  "as": { abbrev: "AS", empresa: "Aquasan" },
  "sc": { abbrev: "SC", empresa: "Salmones de Chile" },
  "bl": { abbrev: "Bl", empresa: "Blumar" },
  "ve": { abbrev: "VE", empresa: "Ventisqueros" },
  "br": { abbrev: "Br", empresa: "Blu River" },
  "sa": { abbrev: "SA", empresa: "Salmones Saysen" },
  "mf": { abbrev: "MF", empresa: "Marine Farm" },
  "fs": { abbrev: "FS", empresa: "Friosur" },
  "ya": { abbrev: "Ya", empresa: "Yadran" },
  "in": { abbrev: "In", empresa: "Invermar" },
  "ck": { abbrev: "Ck", empresa: "Cooke" },
  "na": { abbrev: "NA", empresa: "Nova Austral" },
  "lf": { abbrev: "LF", empresa: "Los Fiordos" },
  "sal": { abbrev: "SAL", empresa: "Salmones Austral" },
  "cb": { abbrev: "Cb", empresa: "Salmones Caleta Bay" }
};

function parseLocationInfo(loc) {
  if (!loc) return { empresa: null, nombre_centro: "", location: "" };
  const locClean = loc.trim().toLowerCase().split(".")[0];
  if (!locClean) return { empresa: null, nombre_centro: "", location: "" };

  const parts = locClean.split("-");
  const prefix = parts[0];

  let rest = "";
  if (parts.length > 1) {
    rest = parts.slice(1).join("-");
  } else {
    rest = locClean;
  }

  // Separar prefijos conocidos pegados como acopio/piscicultura/planta/etc.
  const prefijosConocidos = ["acopio", "piscicultura", "planta", "ensenada", "isla", "canal", "bahia", "seno", "punta", "puerto", "boca", "paso", "estero", "rio", "caleta"];
  for (const p of prefijosConocidos) {
    if (rest.startsWith(p) && rest.length > p.length) {
      rest = p + " " + rest.slice(p.length);
      break;
    }
  }

  // Separar sufijos comunes pegados como sur/norte/este/oeste/alto/bajo
  ["sur", "norte", "este", "oeste", "alto", "bajo"].forEach(w => {
    if (rest.endsWith(w) && rest.length > w.length) {
      rest = rest.slice(0, -w.length) + " " + w;
    }
  });

  // Insert space before numbers (e.g. tranqui1 -> tranqui 1)
  const restFormatted = rest.replace(/([a-zA-Z]+)(\d+)/g, "$1 $2");
  
  // Format in Title Case (Capitalize each word, no company prefix code)
  const nombre_centro = restFormatted
    .split(/[\s-_]+/)
    .filter(w => w.length > 0)
    .map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase())
    .join(" ");

  let empresa = null;
  if (MAPA_ABREVIATURAS_EMPRESAS[prefix]) {
    empresa = MAPA_ABREVIATURAS_EMPRESAS[prefix].empresa;
  }

  return { empresa: empresa, nombre_centro: nombre_centro, location: locClean };
}
const TIPOS_EQUIPOS = [
  "Jennic simple", "Jennic doble", "Notebook", "Cámara", "Antena", "Estación Meteorológica", "Otro"
];

const TIPOS_SENSORES = [
  "Sensor Oxígeno - T°c", "Sensor Conductividad", "Sensor Oxígeno - Conductividad - T°c",
  "Sensor Sulfuro", "Sensor Redox", "Sensor pH", "Sensor Profundidad",
  "Sensor Nivel de Agua", "Sensor Salinidad", "Sensor Temperatura",
  "Sensor Corriente", "Sensor Turbidez", "Sensor Clorofila", "Sensor ADCP", "Otro"
];

const TIPOS_ELEMENTOS = TIPOS_EQUIPOS;

const RESPONSABLES_ACTIVACION = [
  "Hector Portillo",
  "Gabriel Moya",
  "Leonardo Araneda",
  "Felipe Godoy",
  "Edwin Gonzalez",
  "Ivan Soto",
  "Otro..."
];

// Estado global del certificado (Valores Oficiales Predeterminados)
let certificadoState = {
  datos_generales: {
    encargado_area: "Rodrigo Bustamante",
    empresa: "Camanchaca",
    location: "",
    nombre_centro: "",
    fecha_instalacion: new Date().toLocaleDateString('es-CL'),
    tecnico_visita: "Bernardo Guenteo",
    numero_ficha: "",
    coordenadas: "",
    barrio: "",
    puerto_patron: "",
    correo_centro: ""
  },
  infraestructura: {
    categoria: "Notebook",
    marca: "Lenovo",
    modelo: "Lenovo V14 G3 IAP",
    sistema_operativo: "Ubuntu 24.04 LTS",
    mac_ethernet: "",
    ip_vpn: ""
  },
  acceso_remoto: {
    protocolo: "OpenVPN",
    tun0: "10.9.18.37",
    hostserver: "dataweb.innovex.cl",
    puerto_server: "8888"
  },
  estacion_camara: {
    camara_instalada: "Si",
    modelo_camara: "Domo",
    conexion_camara: "Switch PoE",
    ip_fija_camara: "192.168.8.40",
    ubicacion_camara: "Pontón",
    estacion_instalada: "Si",
    modelo_estacion: "Davis",
    region_davis: "US",
    ubicacion_estacion: "Pontón",
    switch_poe: "Si",
    modelo_switch: "DS-3E0105P-E(B)",
    ubicacion_switch: "Pontón"
  },
  monitoreo_abiotico: {
    instalado: "Si",
    tipo_antena: "Outdoor",
    version: "v2.0.2",
    mac: "00:15:8D:00:09:24:53:F7",
    panid: "2020"
  },
  ubicacion_repuestos: "Bodega Pontón Principal",
  equipos_repuesto: [
    { tipo: "Equipo Jennic", mac: "00:15:8D:00:09:82:2A:A5", identificacion: "00:15:8D:00:09:82:2A:A5" },
    { tipo: "Sensor Integrado", metraje: "15", serie: "12345Y", identificacion: "12345Y" }
  ],
  ubicaciones: [
    {
      nombre: "Pontón Principal",
      coordenadas: "-42.749224 -73.580710",
      elementos: [
        { tipo: "Oxi-Sal", metraje: "5", serie: "12845" },
        { tipo: "Oxi-Sal", metraje: "10", serie: "12846" }
      ]
    }
  ],
  activacion: {
    ip_final: "10.170.47.28",
    interfaz: "wlp0s20f3",
    responsable_activacion: "Hector Portillo",
    estado_final: "Operativo"
  },
  evidencias: [],
  configuracion_alarmas: [],
  motes: [],
  observaciones: ""
};

// Inicialización cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", () => {
  setupTabs();
  poblarDropdownsConstantes();
  cargarEstructuraPersonalDesdeAPI();
  bindFormInputs();
  crearNuevoCertificadoSinPopup();
  cargarListaCertificadosHeader(false);
  setupDragAndDrop();

  // Dark / Light Mode Toggle con Persistencia
  const themeBtn = document.getElementById("btnToggleTheme");
  if (themeBtn) {
    try {
      const savedTheme = localStorage.getItem("portal_theme");
      if (savedTheme === "dark") {
        document.body.classList.add("dark-theme");
        document.body.classList.remove("light-theme");
        themeBtn.textContent = "☀️ Modo Claro";
      }
    } catch (e) {}

    themeBtn.addEventListener("click", () => {
      document.body.classList.toggle("dark-theme");
      const isDark = document.body.classList.contains("dark-theme");
      if (isDark) {
        document.body.classList.remove("light-theme");
      } else {
        document.body.classList.add("light-theme");
      }
      themeBtn.textContent = isDark ? "☀️ Modo Claro" : "🌓 Modo Oscuro";
      try {
        localStorage.setItem("portal_theme", isDark ? "dark" : "light");
      } catch (e) {}
    });
  }

  // Header Actions (Sin Popups)
  document.getElementById("btnHeaderNuevo")?.addEventListener("click", () => {
    crearNuevoCertificadoSinPopup();
  });

  document.getElementById("btnHeaderCargar")?.addEventListener("click", () => {
    const loc = document.getElementById("headerCertSelect")?.value;
    if (loc) cargarCertificadoPorLocation(loc);
    else mostrarToast("Seleccione un certificado de la lista del encabezado", "error");
  });

  const btnEliminar = document.getElementById("btnHeaderEliminar");
  if (btnEliminar) {
    btnEliminar.addEventListener("click", () => {
      const loc = document.getElementById("headerCertSelect")?.value || (certificadoState.datos_generales ? certificadoState.datos_generales.location : "");
      if (!loc) {
        mostrarToast("Seleccione un certificado de la lista del encabezado para eliminar", "warning");
        return;
      }
      if (confirm(`¿Está seguro que desea ELIMINAR permanentemente el certificado del centro '${loc}'? Esta acción borra el registro JSON, el PDF y sus imágenes asociadas.`)) {
        eliminarCertificadoPorLocation(loc);
      }
    });
  }

  document.getElementById("btnProcesarAutofill")?.addEventListener("click", procesarAutofill);
  document.getElementById("btnEjecutarSSHAutofill")?.addEventListener("click", ejecutarSSHAutofill);
  document.getElementById("btnCopiarComandoAutofill")?.addEventListener("click", copiarComandoPortapapeles);
  document.getElementById("btnGuardar")?.addEventListener("click", guardarAvance);
  setupNavButtons();


  // Revisor & Verificación de Ingreso
  const btnEjecutarRevisor = document.getElementById("btnEjecutarRevisor");
  if (btnEjecutarRevisor) {
    btnEjecutarRevisor.addEventListener("click", ejecutarRevisorEquipos);
  }
  const btnCopiarPlantillaRevisor = document.getElementById("btnCopiarPlantillaRevisor");
  if (btnCopiarPlantillaRevisor) {
    btnCopiarPlantillaRevisor.addEventListener("click", copiarPlantillaRevisor);
  }
  const btnAutoRellenarDesdeRevisor = document.getElementById("btnAutoRellenarDesdeRevisor");
  if (btnAutoRellenarDesdeRevisor) {
    btnAutoRellenarDesdeRevisor.addEventListener("click", autoRellenarDesdeRevisor);
  }

  const inputsRevisor = [
    "rev_centro", "rev_host", "rev_usuario", "rev_contrasena", "rev_tipo_conexion",
    "rev_sistema_operativo", "rev_kernel", "rev_clave_pc", "rev_dataweb",
    "rev_pcinnovex", "rev_cacheton", "rev_python3", "rev_weather_davis", "rev_visibility_cam",
    "rev_version_equipos", "rev_senal", "rev_voltajes",
    "rev_saturacion", "rev_salinidad", "rev_temperatura",
    "rev_camara", "rev_estacion", "rev_repuestos",
    "rev_repuesto_equipo", "rev_repuesto_sensor", "rev_repuesto_kit",
    "rev_telefono", "rev_correo", "rev_observaciones"
  ];
  inputsRevisor.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener("input", () => construirPlantillaRevisorDesdeFormulario());
      el.addEventListener("change", () => construirPlantillaRevisorDesdeFormulario());
    }
  });

  const revContrasenaEl = document.getElementById("rev_contrasena");
  if (revContrasenaEl) {
    revContrasenaEl.addEventListener("input", (e) => {
      const elClave = document.getElementById("rev_clave_pc");
      if (elClave && (!elClave.value || elClave.dataset.synced !== "custom")) {
        elClave.value = e.target.value;
      }
      construirPlantillaRevisorDesdeFormulario();
    });
  }
  const revHostEl = document.getElementById("rev_host");
  if (revHostEl) {
    revHostEl.addEventListener("input", (e) => {
      const val = e.target.value.trim();
      const elCentro = document.getElementById("rev_centro");
      if (elCentro && val) {
        const parsed = parseLocationInfo(val.split(".")[0]);
        if (parsed.nombre_centro && (!elCentro.value || elCentro.dataset.synced !== "custom")) {
          elCentro.value = parsed.nombre_centro;
        }
      }
      construirPlantillaRevisorDesdeFormulario();
    });
  }
  const revCentroEl = document.getElementById("rev_centro");
  if (revCentroEl) {
    revCentroEl.addEventListener("input", () => {
      revCentroEl.dataset.synced = "custom";
    });
  }

  // Información para ingreso de técnico
  const btnEjecutarIngresoTecnico = document.getElementById("btnEjecutarIngresoTecnico");
  if (btnEjecutarIngresoTecnico) {
    btnEjecutarIngresoTecnico.addEventListener("click", ejecutarIngresoTecnico);
  }
  const btnGenerarPlantillaIngreso = document.getElementById("btnGenerarPlantillaIngreso");
  if (btnGenerarPlantillaIngreso) {
    btnGenerarPlantillaIngreso.addEventListener("click", () => generarPlantillaIngreso({ notificar: true }));
  }
  const btnCopiarPlantillaIngreso = document.getElementById("btnCopiarPlantillaIngreso");
  if (btnCopiarPlantillaIngreso) {
    btnCopiarPlantillaIngreso.addEventListener("click", copiarPlantillaIngreso);
  }

  const inputsIngreso = [
    "ingreso_host", "ingreso_usuario", "ingreso_contrasena", "ingreso_clave_pc", "ingreso_acceso_remoto",
    "ingreso_repuesto_equipo", "ingreso_repuesto_sensor", "ingreso_repuesto_kit",
    "ingreso_antena_status", "ingreso_equipos_conectados", "ingreso_voltaje_pilas",
    "ingreso_observaciones", "ingreso_observaciones_generales"
  ];
  inputsIngreso.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener("input", programarActualizacionIngreso);
      el.addEventListener("change", programarActualizacionIngreso);
    }
  });

  const ingContrasenaEl = document.getElementById("ingreso_contrasena");
  if (ingContrasenaEl) {
    ingContrasenaEl.addEventListener("input", (e) => {
      const elClave = document.getElementById("ingreso_clave_pc");
      if (elClave && (!elClave.value || elClave.dataset.synced !== "custom")) {
        elClave.value = e.target.value;
      }
      programarActualizacionIngreso();
    });
  }
  const ingClavePcEl = document.getElementById("ingreso_clave_pc");
  if (ingClavePcEl) {
    ingClavePcEl.addEventListener("input", () => {
      ingClavePcEl.dataset.synced = "custom";
    });
  }

  inicializarObservacionesGeneralesDefault();

  // Configurar Selector Principal de Módulos de Soporte
  setupModuleSwitcher();

  const btnSubtabPlantilla = document.getElementById("btnSubtabPlantilla");
  const btnSubtabDocumentoLive = document.getElementById("btnSubtabDocumentoLive");
  if (btnSubtabPlantilla && btnSubtabDocumentoLive) {
    btnSubtabPlantilla.addEventListener("click", () => {
      const p = document.getElementById("viewPlantillaTexto");
      const d = document.getElementById("viewDocumentoLive");
      if (p) p.style.display = "block";
      if (d) d.style.display = "none";
      btnSubtabPlantilla.classList.add("active");
      btnSubtabDocumentoLive.classList.remove("active");
    });
    btnSubtabDocumentoLive.addEventListener("click", () => {
      const p = document.getElementById("viewPlantillaTexto");
      const d = document.getElementById("viewDocumentoLive");
      if (p) p.style.display = "none";
      if (d) d.style.display = "block";
      btnSubtabDocumentoLive.classList.add("active");
      btnSubtabPlantilla.classList.remove("active");
      actualizarFrameDocumentoLive();
    });
  }

  const btnSubtabIngresoLive = document.getElementById("btnSubtabIngresoLive");
  const btnSubtabIngresoTexto = document.getElementById("btnSubtabIngresoTexto");
  if (btnSubtabIngresoLive && btnSubtabIngresoTexto) {
    btnSubtabIngresoLive.addEventListener("click", () => {
      const l = document.getElementById("viewIngresoLive");
      const t = document.getElementById("viewIngresoTexto");
      if (l) l.style.display = "block";
      if (t) t.style.display = "none";
      btnSubtabIngresoLive.classList.add("active");
      btnSubtabIngresoTexto.classList.remove("active");
      actualizarFrameDocumentoIngresoLive();
    });
    btnSubtabIngresoTexto.addEventListener("click", () => {
      const l = document.getElementById("viewIngresoLive");
      const t = document.getElementById("viewIngresoTexto");
      if (l) l.style.display = "none";
      if (t) t.style.display = "block";
      btnSubtabIngresoTexto.classList.add("active");
      btnSubtabIngresoLive.classList.remove("active");
    });
  }

  // Toggles de Vista Previa Derecha
  document.getElementById("btnToggleVistaHTML")?.addEventListener("click", () => {
    modoVistaPreviaModulos = "html";
    const liveC = document.getElementById("liveHtmlContainer");
    if (liveC) liveC.style.display = "block";
    document.getElementById("btnToggleVistaHTML")?.classList.add("active");
    document.getElementById("btnToggleVistaPDF")?.classList.remove("active");
    document.getElementById("btnToggleVistaTexto")?.classList.remove("active");
    actualizarVistaPreviaDerechaPorModulo();
  });

  document.getElementById("btnToggleVistaPDF")?.addEventListener("click", () => {
    modoVistaPreviaModulos = "html";
    document.getElementById("btnToggleVistaTexto")?.classList.remove("active");
    compilarYMostrarPDF();
  });

  document.getElementById("btnToggleVistaTexto")?.addEventListener("click", () => {
    mostrarTextoPlanoEnPanelDerecho();
  });

  document.getElementById("btnCopiarDesdePreview")?.addEventListener("click", async () => {
    let txt = "";
    if (moduloActivoActual === "revisor") {
      txt = document.getElementById("txtPlantillaRevisor")?.value || construirPlantillaRevisorTextoClientSide();
    } else if (moduloActivoActual === "ingreso_tecnico") {
      txt = document.getElementById("txtPlantillaIngresoTecnico")?.value || construirPlantillaIngresoTextoClientSide();
    } else {
      txt = document.getElementById("preTextoPlanoDerecho")?.textContent || "";
    }
    const copiado = await copiarTextoAlPortapapeles(txt);
    const btn = document.getElementById("btnCopiarDesdePreview");
    if (btn && copiado) {
      const orig = btn.innerHTML;
      btn.innerHTML = "✓ Copiado";
      setTimeout(() => { btn.innerHTML = orig; }, 1800);
    }
    mostrarToast(copiado ? "Texto copiado al portapapeles" : "No se pudo copiar el texto", copiado ? "success" : "error");
  });

  // Pre-generar datos iniciales de Revisor e Ingreso Técnico
  setTimeout(() => {
    generarPlantillaRevisor();
    generarPlantillaIngreso();
  }, 100);

  // Formulario Integrado Repuestos
  document.getElementById("btnToggleFormRepuesto")?.addEventListener("click", () => {
    const f = document.getElementById("formNuevoRepuesto");
    if (f) f.style.display = f.style.display === "none" ? "block" : "none";
  });
  document.getElementById("btnCancelarRepuesto")?.addEventListener("click", () => {
    const f = document.getElementById("formNuevoRepuesto");
    if (f) f.style.display = "none";
  });
  document.getElementById("btnGuardarRepuesto")?.addEventListener("click", guardarNuevoRepuestoInline);

  document.getElementById("rep_tipo_select")?.addEventListener("change", (e) => {
    const esJennic = e.target.value === "Equipo Jennic";
    const gMac = document.getElementById("group_rep_mac");
    const gSerie = document.getElementById("group_rep_serie");
    const gMet = document.getElementById("group_rep_metraje");
    if (gMac) gMac.style.display = esJennic ? "flex" : "none";
    if (gSerie) gSerie.style.display = esJennic ? "none" : "flex";
    if (gMet) gMet.style.display = esJennic ? "none" : "flex";
  });

  // Formulario Ubicación
  document.getElementById("btnToggleFormUbicacion")?.addEventListener("click", () => {
    const f = document.getElementById("formNuevaUbicacion");
    if (f) f.style.display = f.style.display === "none" ? "block" : "none";
  });
  document.getElementById("btnCancelarUbicacion")?.addEventListener("click", () => {
    const f = document.getElementById("formNuevaUbicacion");
    if (f) f.style.display = "none";
  });
  document.getElementById("btnGuardarUbicacion")?.addEventListener("click", guardarNuevaUbicacionInline);

  document.getElementById("btnAgregarFilaAlarma")?.addEventListener("click", agregarFilaAlarmaVacia);
  document.getElementById("btnProcesarPegadoAlarmas")?.addEventListener("click", procesarPegadoTextoAlarmas);

  document.getElementById("ub_repuestos_general")?.addEventListener("input", (e) => {
    certificadoState.ubicacion_repuestos = e.target.value;
    renderLiveHtmlSheet();
  });

  // Inicializar componentes del Portal Unificado
  iniciarPortalUnificado();
});

// Crear nuevo certificado sin popup emergente
function crearNuevoCertificadoSinPopup() {
  certificadoState = {
    datos_generales: {
      location: "",
      nombre_centro: "",
      empresa: "Camanchaca",
      encargado_area: "Rodrigo Bustamante",
      tecnico_visita: "Bernardo Guenteo",
      fecha_instalacion: new Date().toLocaleDateString('es-CL'),
      numero_ficha: "",
      coordenadas: "",
      barrio: "",
      puerto_patron: "",
      correo_centro: ""
    },
    infraestructura: {
      categoria: "Notebook",
      marca: "Lenovo",
      modelo: "Lenovo V14 G3 IAP",
      sistema_operativo: "Ubuntu 24.04 LTS",
      mac_ethernet: "",
      ip_vpn: ""
    },
    acceso_remoto: {
      protocolo: "OpenVPN",
      tun0: "",
      hostserver: "dataweb.innovex.cl",
      puerto_server: "8888"
    },
    estacion_camara: {
      camara_instalada: "Si",
      modelo_camara: "Domo",
      conexion_camara: "Switch PoE",
      ip_fija_camara: "192.168.8.40",
      ubicacion_camara: "Pontón",
      estacion_instalada: "Si",
      modelo_estacion: "Davis",
      region_davis: "US",
      ubicacion_estacion: "Pontón",
      switch_poe: "Si",
      modelo_switch: "DS-3E0105P-E(B)",
      ubicacion_switch: "Pontón"
    },
    monitoreo_abiotico: {
      instalado: "Si",
      tipo_antena: "Outdoor",
      version: "v2.0.2",
      mac: "",
      panid: "2020"
    },
    ubicacion_repuestos: "",
    equipos_repuesto: [],
    ubicaciones: [],
    activacion: {
      ip_final: "",
      interfaz: "wlp0s20f3",
      responsable_activacion: "Hector Portillo",
      estado_final: "Operativo"
    },
    evidencias: [],
    configuracion_alarmas: [],
    motes: [],
    observaciones: ""
  };

  poblarFormularioDesdeState();
  
  const tabBtn = document.querySelector(".tab-btn[data-tab='generales']");
  if (tabBtn) tabBtn.click();
  
  const locInput = document.getElementById("gen_location");
  if (locInput) locInput.focus();

  mostrarToast("Nuevo certificado limpio iniciado. Complete Location ID y Nombre del Centro.", "info");
}

// Toast Notifications
function mostrarToast(mensaje, tipo = "info") {
  const container = document.getElementById("toastContainer");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = `toast ${tipo}`;
  toast.innerHTML = `<span>${mensaje}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 3500);
}

// Poblar Dropdowns y resolver campos "Otro..."
function poblarDropdownsConstantes() {
  // Empresas
  const empSel = document.getElementById("gen_empresa_select");
  const empCustom = document.getElementById("gen_empresa_custom");
  if (empSel) {
    empSel.innerHTML = "";
    EMPRESAS.forEach(emp => {
      const opt = document.createElement("option");
      opt.value = emp;
      opt.textContent = emp;
      empSel.appendChild(opt);
    });

    empSel.addEventListener("change", (e) => {
      if (e.target.value === "Otro...") {
        if (empCustom) empCustom.style.display = "block";
        if (empCustom) certificadoState.datos_generales.empresa = empCustom.value;
      } else {
        if (empCustom) empCustom.style.display = "none";
        certificadoState.datos_generales.empresa = e.target.value;
      }
      renderLiveHtmlSheet();
    });
  }

  if (empCustom) {
    empCustom.addEventListener("input", (e) => {
      certificadoState.datos_generales.empresa = e.target.value;
      renderLiveHtmlSheet();
    });
  }

  // Encargados
  const encSel = document.getElementById("gen_encargado_select");
  if (encSel) {
    encSel.innerHTML = "";
    Object.keys(ESTRUCTURA_PERSONAL).forEach(enc => {
      const opt = document.createElement("option");
      opt.value = enc;
      opt.textContent = enc;
      encSel.appendChild(opt);
    });

    encSel.addEventListener("change", (e) => {
      certificadoState.datos_generales.encargado_area = e.target.value;
      actualizarDropdownAreas(e.target.value);
      actualizarDropdownTecnicos(e.target.value);
      renderLiveHtmlSheet();
    });
  }

  // Áreas / Zonas Geográficas
  const areaSel = document.getElementById("gen_area_select");
  const areaCustom = document.getElementById("gen_area_custom");
  if (areaSel) {
    areaSel.addEventListener("change", (e) => {
      if (e.target.value === "Otra zona...") {
        if (areaCustom) {
          areaCustom.style.display = "block";
          certificadoState.datos_generales.area = areaCustom.value;
        }
      } else {
        if (areaCustom) areaCustom.style.display = "none";
        certificadoState.datos_generales.area = e.target.value;
      }
      renderLiveHtmlSheet();
    });
  }

  if (areaCustom) {
    areaCustom.addEventListener("input", (e) => {
      certificadoState.datos_generales.area = e.target.value;
      renderLiveHtmlSheet();
    });
  }

  // Técnicos
  actualizarDropdownAreas("Rodrigo Bustamante");
  actualizarDropdownTecnicos("Rodrigo Bustamante");
  const tecSel = document.getElementById("gen_tecnico_select");
  const tecCustom = document.getElementById("gen_tecnico_custom");
  if (tecSel) {
    tecSel.addEventListener("change", (e) => {
      if (e.target.value === "Otro...") {
        if (tecCustom) tecCustom.style.display = "block";
        if (tecCustom) certificadoState.datos_generales.tecnico_visita = tecCustom.value;
      } else {
        if (tecCustom) tecCustom.style.display = "none";
        certificadoState.datos_generales.tecnico_visita = e.target.value;
      }
      renderLiveHtmlSheet();
    });
  }

  if (tecCustom) {
    tecCustom.addEventListener("input", (e) => {
      certificadoState.datos_generales.tecnico_visita = e.target.value;
      renderLiveHtmlSheet();
    });
  }

  // Responsables Activación
  const respSel = document.getElementById("act_responsable_select");
  const respCustom = document.getElementById("act_responsable_custom");
  if (respSel) {
    respSel.innerHTML = "";
    RESPONSABLES_ACTIVACION.forEach(r => {
      const opt = document.createElement("option");
      opt.value = r;
      opt.textContent = r;
      respSel.appendChild(opt);
    });

    respSel.addEventListener("change", (e) => {
      if (e.target.value === "Otro...") {
        if (respCustom) respCustom.style.display = "block";
        if (respCustom) certificadoState.activacion.responsable_activacion = respCustom.value;
      } else {
        if (respCustom) respCustom.style.display = "none";
        certificadoState.activacion.responsable_activacion = e.target.value;
      }
      renderLiveHtmlSheet();
    });
  }

  if (respCustom) {
    respCustom.addEventListener("input", (e) => {
      certificadoState.activacion.responsable_activacion = e.target.value;
      renderLiveHtmlSheet();
    });
  }
}

async function cargarEstructuraPersonalDesdeAPI() {
  try {
    const res = await fetch("/api/personal/estructura");
    if (res.ok) {
      const data = await res.json();
      if (data.mapa_completo && Object.keys(data.mapa_completo).length > 0) {
        ESTRUCTURA_PERSONAL = data.mapa_completo;
        const encSel = document.getElementById("gen_encargado_select");
        if (encSel) {
          const prevVal = encSel.value || certificadoState.datos_generales.encargado_area;
          encSel.innerHTML = "";
          Object.keys(ESTRUCTURA_PERSONAL).forEach(enc => {
            const opt = document.createElement("option");
            opt.value = enc;
            opt.textContent = enc;
            encSel.appendChild(opt);
          });
          if (prevVal && ESTRUCTURA_PERSONAL[prevVal]) {
            encSel.value = prevVal;
          }
          actualizarDropdownAreas(encSel.value, certificadoState.datos_generales.area);
          actualizarDropdownTecnicos(encSel.value, certificadoState.datos_generales.tecnico_visita);
        }
      }
    }
  } catch (err) {
    console.log("Estructura personal usando fallback local");
  }
}

function actualizarDropdownAreas(encargado, valorSeleccionado = null) {
  const areaSel = document.getElementById("gen_area_select");
  const areaCustom = document.getElementById("gen_area_custom");
  if (!areaSel) return;

  areaSel.innerHTML = "";

  const infoEnc = ESTRUCTURA_PERSONAL[encargado] || { zonas: [], tecnicos: [] };
  const zonasPropias = infoEnc.zonas || [];

  // 1. Zonas asignadas al encargado seleccionado
  if (zonasPropias.length > 0) {
    const grpPrincipal = document.createElement("optgroup");
    grpPrincipal.label = `Zonas Asignadas (${encargado})`;
    zonasPropias.forEach(z => {
      const opt = document.createElement("option");
      opt.value = z;
      opt.textContent = z;
      grpPrincipal.appendChild(opt);
    });
    areaSel.appendChild(grpPrincipal);
  }

  // 2. Otras zonas de la red (para suplencias entre encargados)
  const otrasZonas = [];
  Object.entries(ESTRUCTURA_PERSONAL).forEach(([otroEnc, data]) => {
    if (otroEnc !== encargado && data.zonas) {
      data.zonas.forEach(z => {
        if (!zonasPropias.includes(z) && !otrasZonas.includes(z)) {
          otrasZonas.push(z);
        }
      });
    }
  });

  if (otrasZonas.length > 0) {
    const grpOtras = document.createElement("optgroup");
    grpOtras.label = "Otras Zonas (Suplencias)";
    otrasZonas.sort().forEach(z => {
      const opt = document.createElement("option");
      opt.value = z;
      opt.textContent = z;
      grpOtras.appendChild(opt);
    });
    areaSel.appendChild(grpOtras);
  }

  // 3. Opción 'Otra zona...'
  const optOtra = document.createElement("option");
  optOtra.value = "Otra zona...";
  optOtra.textContent = "Otra zona...";
  areaSel.appendChild(optOtra);

  // Seleccionar valor adecuado
  if (valorSeleccionado) {
    const match = Array.from(areaSel.options).find(o => o.value.toLowerCase() === String(valorSeleccionado).trim().toLowerCase());
    if (match) {
      areaSel.value = match.value;
      if (areaCustom) areaCustom.style.display = "none";
      certificadoState.datos_generales.area = match.value;
    } else {
      areaSel.value = "Otra zona...";
      if (areaCustom) {
        areaCustom.style.display = "block";
        areaCustom.value = valorSeleccionado;
      }
      certificadoState.datos_generales.area = valorSeleccionado;
    }
  } else {
    if (zonasPropias.length > 0) {
      areaSel.value = zonasPropias[0];
      if (areaCustom) areaCustom.style.display = "none";
      certificadoState.datos_generales.area = zonasPropias[0];
    } else {
      areaSel.value = "Otra zona...";
      if (areaCustom) areaCustom.style.display = "block";
    }
  }
}

function actualizarDropdownTecnicos(encargado, valorSeleccionado = null) {
  const tecSel = document.getElementById("gen_tecnico_select");
  const tecCustom = document.getElementById("gen_tecnico_custom");
  if (!tecSel) return;

  tecSel.innerHTML = "";

  const infoEnc = ESTRUCTURA_PERSONAL[encargado] || { zonas: [], tecnicos: [] };
  const tecnicosPropios = infoEnc.tecnicos || [];

  // 1. Técnicos asignados al encargado
  if (tecnicosPropios.length > 0) {
    const grpPrincipal = document.createElement("optgroup");
    grpPrincipal.label = `Técnicos a Cargo (${encargado})`;
    tecnicosPropios.forEach(t => {
      const opt = document.createElement("option");
      opt.value = t;
      opt.textContent = t;
      grpPrincipal.appendChild(opt);
    });
    tecSel.appendChild(grpPrincipal);
  }

  // 2. Otros técnicos
  const otrosTecs = [];
  Object.entries(ESTRUCTURA_PERSONAL).forEach(([otroEnc, data]) => {
    if (otroEnc !== encargado && data.tecnicos) {
      data.tecnicos.forEach(t => {
        if (!tecnicosPropios.includes(t) && !otrosTecs.includes(t)) {
          otrosTecs.push(t);
        }
      });
    }
  });

  if (otrosTecs.length > 0) {
    const grpOtras = document.createElement("optgroup");
    grpOtras.label = "Otros Técnicos";
    otrosTecs.sort().forEach(t => {
      const opt = document.createElement("option");
      opt.value = t;
      opt.textContent = t;
      grpOtras.appendChild(opt);
    });
    tecSel.appendChild(grpOtras);
  }

  // 3. Opción 'Otro...'
  const optOtro = document.createElement("option");
  optOtro.value = "Otro...";
  optOtro.textContent = "Otro...";
  tecSel.appendChild(optOtro);

  // Seleccionar valor adecuado
  if (valorSeleccionado) {
    const match = Array.from(tecSel.options).find(o => o.value.toLowerCase() === String(valorSeleccionado).trim().toLowerCase());
    if (match) {
      tecSel.value = match.value;
      if (tecCustom) tecCustom.style.display = "none";
      certificadoState.datos_generales.tecnico_visita = match.value;
    } else {
      tecSel.value = "Otro...";
      if (tecCustom) {
        tecCustom.style.display = "block";
        tecCustom.value = valorSeleccionado;
      }
      certificadoState.datos_generales.tecnico_visita = valorSeleccionado;
    }
  } else {
    if (tecnicosPropios.length > 0) {
      tecSel.value = tecnicosPropios[0];
      if (tecCustom) tecCustom.style.display = "none";
      certificadoState.datos_generales.tecnico_visita = tecnicosPropios[0];
    } else {
      tecSel.value = "Otro...";
      if (tecCustom) tecCustom.style.display = "block";
    }
  }
}

let moduloActivoActual = "certificado"; // "certificado", "revisor", "ingreso_tecnico"
let modoVistaPreviaModulos = "html"; // "html", "texto"

function activarSeccionTab(targetTab) {
  document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
  const targetId = `tab-${targetTab}`;
  const targetEl = document.getElementById(targetId);
  if (targetEl) {
    targetEl.classList.add("active");
  }

  // Sincronizar estado activo de los botones tab
  document.querySelectorAll(".tab-btn").forEach(t => {
    if (t.dataset.tab === targetTab) t.classList.add("active");
    else t.classList.remove("active");
  });

  // Re-renderizar listas al navegar para garantizar visualización inmediata
  if (moduloActivoActual === "certificado") {
    try { renderMotesList(); } catch(e) {}
    try { renderUbicacionesList(); } catch(e) {}
    try { renderRepuestosList(); } catch(e) {}
    try { renderRepuestosMotesDropdown(); } catch(e) {}
  }

  if (targetTab === "ingreso_tecnico") {
    prellenarDatosHostIngresoTecnico();
  }
  actualizarVistaPreviaDerechaPorModulo();
}

window.cambiarModuloActivo = function(mod) {
  const moduleBtns = document.querySelectorAll(".module-btn");
  moduleBtns.forEach(b => {
    if (b.dataset.module === mod) {
      b.classList.add("active");
      b.style.background = "#0284c7";
      b.style.color = "#ffffff";
      b.style.borderColor = "#0284c7";
    } else {
      b.classList.remove("active");
      b.style.background = "var(--card-bg)";
      b.style.color = "var(--text-color)";
      b.style.borderColor = "var(--border-color)";
    }
  });

  moduloActivoActual = mod;

  const navTabs = document.querySelector(".nav-tabs");
  const certControls = document.getElementById("certContextControls");
  const certGroup = document.getElementById("certSelectorGroup");
  const btnGuardar = document.getElementById("btnGuardar");
  const btnToggleVistaPDF = document.getElementById("btnToggleVistaPDF");
  const btnToggleVistaTexto = document.getElementById("btnToggleVistaTexto");
  const btnToggleVistaHTML = document.getElementById("btnToggleVistaHTML");
  const btnCopiarDesdePreview = document.getElementById("btnCopiarDesdePreview");

  // Resetear toggles de vista previa al cambiar de módulo
  if (btnToggleVistaHTML) btnToggleVistaHTML.classList.add("active");
  if (btnToggleVistaPDF) btnToggleVistaPDF.classList.remove("active");
  if (btnToggleVistaTexto) btnToggleVistaTexto.classList.remove("active");
  const liveC = document.getElementById("liveHtmlContainer");
  if (liveC) liveC.style.display = "block";

  if (mod === "certificado") {
    if (navTabs) navTabs.style.display = "flex";
    if (certControls) certControls.style.display = "flex";
    if (certGroup) certGroup.style.display = "flex";
    if (btnGuardar) btnGuardar.style.display = "inline-block";
    if (btnToggleVistaPDF) btnToggleVistaPDF.style.display = "inline-block";
    if (btnToggleVistaTexto) btnToggleVistaTexto.style.display = "none";
    if (btnCopiarDesdePreview) btnCopiarDesdePreview.style.display = "none";

    activarSeccionTab("autofill");
  } else if (mod === "revisor") {
    if (navTabs) navTabs.style.display = "none";
    if (certControls) certControls.style.display = "none";
    if (certGroup) certGroup.style.display = "none";
    if (btnGuardar) btnGuardar.style.display = "none";
    if (btnToggleVistaPDF) btnToggleVistaPDF.style.display = "none";
    if (btnToggleVistaTexto) btnToggleVistaTexto.style.display = "inline-block";
    if (btnCopiarDesdePreview) btnCopiarDesdePreview.style.display = "inline-flex";

    activarSeccionTab("revisor");
  } else if (mod === "ingreso_tecnico") {
    if (navTabs) navTabs.style.display = "none";
    if (certControls) certControls.style.display = "none";
    if (certGroup) certGroup.style.display = "none";
    if (btnGuardar) btnGuardar.style.display = "none";
    if (btnToggleVistaPDF) btnToggleVistaPDF.style.display = "none";
    if (btnToggleVistaTexto) btnToggleVistaTexto.style.display = "inline-block";
    if (btnCopiarDesdePreview) btnCopiarDesdePreview.style.display = "inline-flex";

    activarSeccionTab("ingreso_tecnico");
  }
};

function setupModuleSwitcher() {
  const moduleBtns = document.querySelectorAll(".module-btn");
  moduleBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      window.cambiarModuloActivo(btn.dataset.module);
    });
  });
}

function setupTabs() {
  const tabs = document.querySelectorAll(".tab-btn");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));

      tab.classList.add("active");
      const targetTab = tab.dataset.tab;
      const targetId = `tab-${targetTab}`;
      const targetEl = document.getElementById(targetId);
      if (targetEl) targetEl.classList.add("active");

      actualizarVistaPreviaDerechaPorModulo();

      if (targetTab === "ingreso_tecnico") {
        prellenarDatosHostIngresoTecnico();
      }
    });
  });
}

function actualizarVistaPreviaDerechaPorModulo() {
  const btnToggleTexto = document.getElementById("btnToggleVistaTexto");
  if (btnToggleTexto && btnToggleTexto.classList.contains("active")) {
    mostrarTextoPlanoEnPanelDerecho();
    return;
  }

  if (moduloActivoActual === "revisor") {
    mostrarVistaPreviaRevisorDerecha();
  } else if (moduloActivoActual === "ingreso_tecnico") {
    mostrarVistaPreviaIngresoDerecha();
  } else {
    restaurarVistaPreviaCertificadoDerecha();
  }
}

function restaurarVistaPreviaCertificadoDerecha() {
  // Asegurar que el contenedor HTML Live esté visible
  const liveContainer = document.getElementById("liveHtmlContainer");
  if (liveContainer) liveContainer.style.display = "block";

  // Asegurar el toggle activo correcto
  const btnHTML = document.getElementById("btnToggleVistaHTML");
  const btnPDF = document.getElementById("btnToggleVistaPDF");
  const btnTexto = document.getElementById("btnToggleVistaTexto");
  if (btnHTML) btnHTML.classList.add("active");
  if (btnPDF) btnPDF.classList.remove("active");
  if (btnTexto) btnTexto.classList.remove("active");

  // Renderizar el informe del certificado
  renderLiveHtmlSheet();
}

function bindFormInputs() {
  const mappings = [
    { id: "gen_location", sec: "datos_generales", key: "location" },
    { id: "gen_nombre_centro", sec: "datos_generales", key: "nombre_centro" },
    { id: "gen_numero_ficha", sec: "datos_generales", key: "numero_ficha" },
    { id: "gen_fecha_instalacion", sec: "datos_generales", key: "fecha_instalacion" },
    { id: "gen_coordenadas", sec: "datos_generales", key: "coordenadas" },
    { id: "gen_barrio", sec: "datos_generales", key: "barrio" },
    { id: "gen_puerto_patron", sec: "datos_generales", key: "puerto_patron" },
    { id: "gen_correo_centro", sec: "datos_generales", key: "correo_centro" },
    { id: "gen_telefono_centro", sec: "datos_generales", key: "telefono_centro" },

    { id: "infra_area", sec: "infraestructura", key: "area" },
    { id: "infra_categoria", sec: "infraestructura", key: "categoria" },
    { id: "infra_marca", sec: "infraestructura", key: "marca" },
    { id: "infra_modelo", sec: "infraestructura", key: "modelo" },
    { id: "infra_so_select", sec: "infraestructura", key: "sistema_operativo" },
    { id: "infra_kernel", sec: "infraestructura", key: "kernel" },
    { id: "infra_mac_ethernet", sec: "infraestructura", key: "mac_ethernet" },
    { id: "infra_mac_wifi", sec: "infraestructura", key: "mac_wifi" },
    { id: "infra_pc_id", sec: "infraestructura", key: "pc_id" },
    { id: "infra_pc_password", sec: "infraestructura", key: "pc_password" },
    { id: "infra_tipo_ip", sec: "infraestructura", key: "tipo_ip" },
    { id: "infra_ip_fija", sec: "infraestructura", key: "ip_fija" },
    { id: "infra_ip_vpn", sec: "infraestructura", key: "ip_vpn" },

    { id: "acc_protocolo_select", sec: "acceso_remoto", key: "protocolo" },
    { id: "acc_tun0", sec: "acceso_remoto", key: "tun0" },
    { id: "acc_hostserver", sec: "acceso_remoto", key: "hostserver" },
    { id: "acc_puerto_server", sec: "acceso_remoto", key: "puerto_server" },

    { id: "cam_instalada", sec: "estacion_camara", key: "camara_instalada" },
    { id: "cam_modelo_camara", sec: "estacion_camara", key: "modelo_camara" },
    { id: "cam_mac_camara", sec: "estacion_camara", key: "mac_camara" },
    { id: "cam_conexion_camara", sec: "estacion_camara", key: "conexion_camara" },
    { id: "cam_ip_fija_camara", sec: "estacion_camara", key: "ip_fija_camara" },
    { id: "cam_ubicacion_camara", sec: "estacion_camara", key: "ubicacion_camara" },

    { id: "cam_estacion_instalada", sec: "estacion_camara", key: "estacion_instalada" },
    { id: "cam_modelo_estacion", sec: "estacion_camara", key: "modelo_estacion" },
    { id: "cam_id_estacion", sec: "estacion_camara", key: "id_estacion_meteorologica" },
    { id: "cam_altura_estacion", sec: "estacion_camara", key: "altura_estacion" },
    { id: "cam_region_davis", sec: "estacion_camara", key: "region_davis" },
    { id: "cam_ubicacion_estacion", sec: "estacion_camara", key: "ubicacion_estacion" },

    { id: "cam_switch_poe", sec: "estacion_camara", key: "switch_poe" },
    { id: "cam_modelo_switch", sec: "estacion_camara", key: "modelo_switch" },
    { id: "cam_ubicacion_switch", sec: "estacion_camara", key: "ubicacion_switch" },

    { id: "ab_instalado", sec: "monitoreo_abiotico", key: "instalado" },
    { id: "ab_tipo_antena", sec: "monitoreo_abiotico", key: "tipo_antena" },
    { id: "ab_ubicacion_antena", sec: "monitoreo_abiotico", key: "ubicacion_antena" },
    { id: "ab_version", sec: "monitoreo_abiotico", key: "version" },
    { id: "ab_mac", sec: "monitoreo_abiotico", key: "mac" },
    { id: "ab_panid", sec: "monitoreo_abiotico", key: "panid" },
    { id: "ab_cantidad_equipos_asociados", sec: "monitoreo_abiotico", key: "cantidad_equipos_asociados" },

    { id: "act_ip_final", sec: "activacion", key: "ip_final" },
    { id: "act_interfaz", sec: "activacion", key: "interfaz" },
    { id: "act_estado_final", sec: "activacion", key: "estado_final" },

    { id: "chk_pc_operativo", sec: "activacion_checklist", key: "pc_operativo" },
    { id: "chk_red_validada", sec: "activacion_checklist", key: "red_validada" },
    { id: "chk_antena_operativa", sec: "activacion_checklist", key: "antena_operativa" },
    { id: "chk_jennic_comunicando", sec: "activacion_checklist", key: "jennic_comunicando" },
    { id: "chk_sensores_datos", sec: "activacion_checklist", key: "sensores_datos" },
    { id: "chk_archivos_dat", sec: "activacion_checklist", key: "archivos_dat" },
    { id: "chk_transmision_estacion", sec: "activacion_checklist", key: "transmision_estacion" },
    { id: "chk_transmision_camara", sec: "activacion_checklist", key: "transmision_camara" },
    { id: "chk_datos_dataweb", sec: "activacion_checklist", key: "datos_dataweb" },
    { id: "chk_alarmas_estandar", sec: "activacion_checklist", key: "alarmas_estandar" }
  ];

  mappings.forEach(m => {
    const el = document.getElementById(m.id);
    if (el) {
      const handler = (e) => {
        const val = e.target.value;
        if (m.sec === "activacion_checklist") {
          if (!certificadoState.activacion) certificadoState.activacion = {};
          if (!certificadoState.activacion.checklist) certificadoState.activacion.checklist = {};
          certificadoState.activacion.checklist[m.key] = val;
        } else {
          if (!certificadoState[m.sec]) certificadoState[m.sec] = {};
          certificadoState[m.sec][m.key] = val;
        }

        if (m.id === "infra_tipo_ip") {
          actualizarVisibilidadConectividadIP();
        }

        // Auto-formateo especial para Location: Inferir Empresa y Nombre del Centro (Title Case sin código)
        if (m.id === "gen_location") {
          const parsed = parseLocationInfo(val);
          if (parsed.nombre_centro) {
            certificadoState.datos_generales.nombre_centro = parsed.nombre_centro;
            const elNom = document.getElementById("gen_nombre_centro");
            if (elNom) elNom.value = parsed.nombre_centro;
          }
          if (parsed.empresa) {
            certificadoState.datos_generales.empresa = parsed.empresa;
            const elEmp = document.getElementById("gen_empresa_select");
            if (elEmp) {
              elEmp.value = parsed.empresa;
              const cust = document.getElementById("gen_empresa_custom");
              if (cust) cust.style.display = "none";
            }
          }
        }

        renderLiveHtmlSheet();
      };
      el.addEventListener("input", handler);
      el.addEventListener("change", handler);
      el.addEventListener("blur", handler);
    }
  });

  const idsVisibilidad = ["cam_estacion_instalada", "cam_modelo_estacion", "cam_instalada", "cam_conexion_camara", "infra_tipo_ip", "ab_instalado"];
  idsVisibilidad.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener("change", () => {
        actualizarVisibilidadCamaraEstacion();
        actualizarVisibilidadConectividadIP();
        // Toggle abiotic fields container
        if (id === "ab_instalado") {
          const containerAb = document.getElementById("abiotico_fields_container");
          if (containerAb) {
            containerAb.style.display = el.value === "No" ? "none" : "block";
          }
        }
        renderLiveHtmlSheet();
      });
    }
  });

  const obsEl = document.getElementById("obs_texto");
  if (obsEl) {
    const obsHandler = (e) => {
      certificadoState.observaciones = e.target.value;
      renderLiveHtmlSheet();
    };
    obsEl.addEventListener("input", obsHandler);
    obsEl.addEventListener("change", obsHandler);
  }
}

function actualizarVisibilidadCamaraEstacion() {
  const estInst = document.getElementById("cam_estacion_instalada")?.value;
  const modeloEst = document.getElementById("cam_modelo_estacion")?.value;
  const grpModeloEst = document.getElementById("group_modelo_estacion");
  const grpIdEst = document.getElementById("group_id_estacion");
  const grpAlturaEst = document.getElementById("group_altura_estacion");
  const grpRegionDavis = document.getElementById("group_region_davis");
  const grpUbicEst = document.getElementById("group_ubicacion_estacion");

  if (estInst === "Si") {
    if (grpModeloEst) grpModeloEst.style.display = "flex";
    if (grpIdEst) grpIdEst.style.display = "flex";
    if (grpAlturaEst) grpAlturaEst.style.display = "flex";
    if (grpUbicEst) grpUbicEst.style.display = "flex";
    if (modeloEst === "Davis") {
      if (grpRegionDavis) grpRegionDavis.style.display = "flex";
    } else {
      if (grpRegionDavis) grpRegionDavis.style.display = "none";
    }
  } else {
    if (grpModeloEst) grpModeloEst.style.display = "none";
    if (grpIdEst) grpIdEst.style.display = "none";
    if (grpAlturaEst) grpAlturaEst.style.display = "none";
    if (grpRegionDavis) grpRegionDavis.style.display = "none";
    if (grpUbicEst) grpUbicEst.style.display = "none";
  }

  const camInst = document.getElementById("cam_instalada")?.value;
  const conexionCam = document.getElementById("cam_conexion_camara")?.value;
  const grpModCam = document.getElementById("group_modelo_camara");
  const grpMacCam = document.getElementById("group_mac_camara");
  const grpConCam = document.getElementById("group_conexion_camara");
  const grpIpCam = document.getElementById("group_ip_camara");
  const grpUbicCam = document.getElementById("group_ubicacion_camara");
  const secSwitchPoe = document.getElementById("section_switch_poe");

  if (camInst === "Si") {
    if (grpModCam) grpModCam.style.display = "flex";
    if (grpMacCam) grpMacCam.style.display = "flex";
    if (grpConCam) grpConCam.style.display = "flex";
    if (grpIpCam) grpIpCam.style.display = "flex";
    if (grpUbicCam) grpUbicCam.style.display = "flex";

    if (conexionCam === "Switch PoE") {
      if (secSwitchPoe) secSwitchPoe.style.display = "block";
      if (!certificadoState.estacion_camara) certificadoState.estacion_camara = {};
      certificadoState.estacion_camara.switch_poe = "Si";
    } else {
      if (secSwitchPoe) secSwitchPoe.style.display = "none";
      if (!certificadoState.estacion_camara) certificadoState.estacion_camara = {};
      certificadoState.estacion_camara.switch_poe = "No";
    }
  } else {
    if (grpModCam) grpModCam.style.display = "none";
    if (grpMacCam) grpMacCam.style.display = "none";
    if (grpConCam) grpConCam.style.display = "none";
    if (grpIpCam) grpIpCam.style.display = "none";
    if (grpUbicCam) grpUbicCam.style.display = "none";
    if (secSwitchPoe) secSwitchPoe.style.display = "none";
    if (!certificadoState.estacion_camara) certificadoState.estacion_camara = {};
    certificadoState.estacion_camara.switch_poe = "No";
  }
}

function actualizarVisibilidadConectividadIP() {
  const tipoIp = document.getElementById("infra_tipo_ip") ? document.getElementById("infra_tipo_ip").value : "IP VPN tun0";
  const grpFija = document.getElementById("group_infra_ip_fija");
  const grpVpn = document.getElementById("group_infra_ip_vpn");

  if (grpFija) grpFija.style.display = (tipoIp === "IP Fija" || tipoIp === "Ambas") ? "block" : "none";
  if (grpVpn) grpVpn.style.display = (tipoIp === "IP VPN tun0" || tipoIp === "Ambas") ? "block" : "none";
}

function poblarFormularioDesdeState() {
  const setVal = (id, val) => {
    const el = document.getElementById(id);
    if (el && val !== undefined) el.value = val;
  };

  const dg = certificadoState.datos_generales || {};
  
  if (dg.location) {
    const parsed = parseLocationInfo(dg.location);
    if (parsed.nombre_centro && (!dg.nombre_centro || dg.nombre_centro === dg.location)) {
      dg.nombre_centro = parsed.nombre_centro;
    }
    if (parsed.empresa && !dg.empresa) {
      dg.empresa = parsed.empresa;
    }
  }

  setVal("gen_location", dg.location);
  setVal("gen_nombre_centro", dg.nombre_centro);
  setVal("gen_empresa_select", dg.empresa);
  if (dg.encargado_area) {
    setVal("gen_encargado_select", dg.encargado_area);
    actualizarDropdownAreas(dg.encargado_area, dg.area);
    actualizarDropdownTecnicos(dg.encargado_area, dg.tecnico_visita);
  } else {
    actualizarDropdownAreas("Rodrigo Bustamante", dg.area);
    actualizarDropdownTecnicos("Rodrigo Bustamante", dg.tecnico_visita);
  }
  setVal("gen_numero_ficha", dg.numero_ficha);
  setVal("gen_fecha_instalacion", dg.fecha_instalacion);
  setVal("gen_coordenadas", dg.coordenadas);
  setVal("gen_barrio", dg.barrio);
  setVal("gen_puerto_patron", dg.puerto_patron);
  setVal("gen_correo_centro", dg.correo_centro);
  setVal("gen_telefono_centro", dg.telefono_centro || dg.numero_centro || "");

  const inf = certificadoState.infraestructura || {};
  setVal("infra_area", inf.area || "");
  setVal("infra_categoria", inf.categoria);
  setVal("infra_marca", inf.marca);
  setVal("infra_modelo", inf.modelo);
  setVal("infra_so_select", inf.sistema_operativo);
  setVal("infra_kernel", inf.kernel || "");
  setVal("infra_mac_ethernet", inf.mac_ethernet);
  setVal("infra_mac_wifi", inf.mac_wifi || "");
  setVal("infra_pc_id", inf.pc_id);
  setVal("infra_pc_password", inf.pc_password);
  setVal("infra_tipo_ip", inf.tipo_ip || "IP VPN tun0");
  setVal("infra_ip_fija", inf.ip_fija);
  setVal("infra_ip_vpn", inf.ip_vpn);
  actualizarVisibilidadConectividadIP();

  const acc = certificadoState.acceso_remoto || {};
  setVal("acc_protocolo_select", acc.protocolo);
  setVal("acc_tun0", acc.tun0);
  setVal("acc_hostserver", acc.hostserver);
  setVal("acc_puerto_server", acc.puerto_server);

  const cam = certificadoState.estacion_camara || {};
  setVal("cam_instalada", cam.camara_instalada || "No");
  setVal("cam_modelo_camara", cam.modelo_camara || "Domo");
  setVal("cam_mac_camara", cam.mac_camara || "");
  setVal("cam_conexion_camara", cam.conexion_camara || "Switch PoE");
  setVal("cam_ip_fija_camara", cam.ip_fija_camara || "");
  setVal("cam_ubicacion_camara", cam.ubicacion_camara || "Pontón");

  setVal("cam_estacion_instalada", cam.estacion_instalada || "No");
  setVal("cam_modelo_estacion", cam.modelo_estacion || "Davis");
  setVal("cam_id_estacion", cam.id_estacion_meteorologica || "");
  setVal("cam_altura_estacion", cam.altura_estacion || "");
  setVal("cam_region_davis", cam.region_davis || "US");
  setVal("cam_ubicacion_estacion", cam.ubicacion_estacion || "Pontón");

  setVal("cam_modelo_switch", cam.modelo_switch || "DS-3E0105P-E(B)");
  setVal("cam_ubicacion_switch", cam.ubicacion_switch || "Pontón");

  actualizarVisibilidadCamaraEstacion();

  const ab = certificadoState.monitoreo_abiotico || {};
  const abInst = ab.instalado || ((ab.version || ab.mac || (certificadoState.motes && certificadoState.motes.length > 0)) ? "Si" : "Si");
  setVal("ab_instalado", abInst);
  const containerAb = document.getElementById("abiotico_fields_container");
  if (containerAb) {
    containerAb.style.display = abInst === "No" ? "none" : "block";
  }
  setVal("ab_tipo_antena", ab.tipo_antena || "Outdoor");
  setVal("ab_ubicacion_antena", ab.ubicacion_antena || "Púlpito / Techo");
  setVal("ab_version", ab.version || "");
  setVal("ab_mac", ab.mac || "");
  setVal("ab_panid", ab.panid || "");
  setVal("ab_cantidad_equipos_asociados", ab.cantidad_equipos_asociados || (certificadoState.motes ? String(certificadoState.motes.length) : ""));

  const act = certificadoState.activacion || {};
  setVal("act_ip_final", act.ip_final);
  setVal("act_interfaz", act.interfaz);
  setVal("act_responsable_select", act.responsable_activacion || "Hector Portillo");
  setVal("act_estado_final", act.estado_final);

  const chk = act.checklist || {};
  setVal("chk_pc_operativo", chk.pc_operativo || "OK");
  setVal("chk_red_validada", chk.red_validada || "OK");
  setVal("chk_antena_operativa", chk.antena_operativa || "OK");
  setVal("chk_jennic_comunicando", chk.jennic_comunicando || "OK");
  setVal("chk_sensores_datos", chk.sensores_datos || "OK");
  setVal("chk_archivos_dat", chk.archivos_dat || "OK");
  setVal("chk_transmision_estacion", chk.transmision_estacion || "OK");
  setVal("chk_transmision_camara", chk.transmision_camara || "OK");
  setVal("chk_datos_dataweb", chk.datos_dataweb || "OK");
  setVal("chk_alarmas_estandar", chk.alarmas_estandar || "OK");

  setVal("ub_repuestos_general", certificadoState.ubicacion_repuestos || "");
  setVal("obs_texto", certificadoState.observaciones || "");

  try { renderMotesList(); } catch(e) {}
  try { renderRepuestosMotesDropdown(); } catch(e) {}
  try { renderUbicacionesList(); } catch(e) {}
  try { renderRepuestosList(); } catch(e) {}
  try { renderEvidenciasGrid(); } catch(e) {}
  try { renderAlarmasTabla(); } catch(e) {}
  try { renderLiveHtmlSheet(); } catch(e) {}
  try { actualizarVistaPreviaDerechaPorModulo(); } catch(e) {}
}

function setupDragAndDrop() {
  const dropEv = document.getElementById("dropzoneEvidencias");
  const fileEv = document.getElementById("fileEvidencias");

  if (dropEv && fileEv) {
    dropEv.addEventListener("click", () => fileEv.click());
    dropEv.addEventListener("dragover", (e) => { e.preventDefault(); dropEv.classList.add("dragover"); });
    dropEv.addEventListener("dragleave", () => dropEv.classList.remove("dragover"));
    dropEv.addEventListener("drop", (e) => {
      e.preventDefault();
      dropEv.classList.remove("dragover");
      if (e.dataTransfer.files.length) procesarArchivosEvidencias(e.dataTransfer.files);
    });
    fileEv.addEventListener("change", (e) => {
      if (e.target.files.length) procesarArchivosEvidencias(e.target.files);
    });
  }

  const dropAl = document.getElementById("dropzoneAlarmas");
  const fileAl = document.getElementById("fileAlarmas");

  if (dropAl && fileAl) {
    dropAl.addEventListener("click", () => fileAl.click());
    dropAl.addEventListener("dragover", (e) => { e.preventDefault(); dropAl.classList.add("dragover"); });
    dropAl.addEventListener("dragleave", () => dropAl.classList.remove("dragover"));
    dropAl.addEventListener("drop", (e) => {
      e.preventDefault();
      dropAl.classList.remove("dragover");
      if (e.dataTransfer.files.length) procesarArchivoAlarmas(e.dataTransfer.files[0]);
    });
    fileAl.addEventListener("change", (e) => {
      if (e.target.files.length) procesarArchivoAlarmas(e.target.files[0]);
    });
  }
}

async function procesarArchivosEvidencias(files) {
  const location = certificadoState.datos_generales.location || "ce-tranqui1";

  for (let file of files) {
    const reader = new FileReader();
    reader.onload = async (e) => {
      const base64 = e.target.result;
      try {
        const res = await fetch("/api/upload_evidencia", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ nombre: file.name, base64: base64, location: location })
        });
        const data = await res.json();

        if (data.status === "ok") {
          if (!certificadoState.evidencias) certificadoState.evidencias = [];
          certificadoState.evidencias.push({ nombre: file.name, ruta: data.ruta, preview: base64 });
          renderEvidenciasGrid();
          renderLiveHtmlSheet();
          mostrarToast(`📷 Evidencia ${file.name} subida`, "success");
        }
      } catch (err) {
        mostrarToast("Error al subir evidencia: " + err.message, "error");
      }
    };
    reader.readAsDataURL(file);
  }
}

async function procesarArchivoAlarmas(file) {
  const location = certificadoState.datos_generales.location || "ce-tranqui1";
  const reader = new FileReader();

  reader.onload = async (e) => {
    const base64 = e.target.result;
    try {
      const res = await fetch("/api/upload_alarmas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre: file.name, base64: base64, location: location })
      });
      const data = await res.json();

      if (data.status === "ok") {
        certificadoState.configuracion_alarmas = data.alarmas || [];
        renderAlarmasTabla();
        renderLiveHtmlSheet();
        mostrarToast(`📊 ${data.alarmas.length} alarmas importadas`, "success");
      }
    } catch (err) {
      mostrarToast("Error al procesar alarmas", "error");
    }
  };
  reader.readAsDataURL(file);
}

async function procesarPegadoTextoAlarmas() {
  const txt = document.getElementById("txtPegarAlarmas").value;
  if (!txt.trim()) {
    mostrarToast("Por favor pegue la tabla de alarmas en el recuadro", "warning");
    return;
  }

  try {
    const res = await fetch("/api/parse_alarmas_texto", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ texto: txt })
    });
    const data = await res.json();

    if (data.status === "ok" && data.alarmas && data.alarmas.length > 0) {
      if (!certificadoState.configuracion_alarmas) certificadoState.configuracion_alarmas = [];
      certificadoState.configuracion_alarmas.push(...data.alarmas);
      renderAlarmasTabla();
      renderLiveHtmlSheet();
      document.getElementById("txtPegarAlarmas").value = "";
      mostrarToast(`${data.alarmas.length} alarmas agregadas desde texto`, "success");
    } else {
      mostrarToast("No se detectaron filas válidas de alarmas en el texto pegado", "warning");
    }
  } catch (err) {
    mostrarToast("Error al procesar alarmas desde texto: " + err.message, "error");
  }
}

function renderEvidenciasGrid() {
  const container = document.getElementById("gridEvidencias");
  if (!container) return;

  container.innerHTML = "";
  const evs = certificadoState.evidencias || [];

  if (evs.length === 0) {
    container.innerHTML = `<div class="subtitle">Sin fotografías de evidencia subidas.</div>`;
    return;
  }

  evs.forEach((ev, idx) => {
    const card = document.createElement("div");
    card.className = "evidencia-card";
    card.style.position = "relative";
    const src = ev.preview || `/api/pdf_preview/2026/${certificadoState.datos_generales.location || 'ce-tranqui1'}/evidencias/${ev.nombre}`;
    const titulo = ev.titulo || ev.nombre || `Foto N° ${idx + 1}`;

    const btnSubir = idx > 0 ? `<button class="btn btn-small btn-secondary" onclick="subirEvidencia(${idx})" title="Mover Arriba">⬆️</button>` : '';
    const btnBajar = idx < evs.length - 1 ? `<button class="btn btn-small btn-secondary" onclick="bajarEvidencia(${idx})" title="Mover Abajo">⬇️</button>` : '';

    card.innerHTML = `
      <img src="${src}" alt="${titulo}" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px 6px 0 0;">
      <div class="footer" style="padding: 8px; display: flex; flex-direction: column; gap: 6px; background: var(--card-bg);">
        <input type="text" value="${titulo}" onchange="actualizarNombreEvidencia(${idx}, this.value)" placeholder="Nombre o descripción foto..." style="font-size: 11px; padding: 4px 6px; border: 1px solid var(--border-color); border-radius: 4px; width: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-size: 11px; font-weight: 600; color: var(--text-muted);">Foto N° ${idx + 1}</span>
          <div style="display: flex; gap: 4px;">
            ${btnSubir}
            ${btnBajar}
            <button class="btn btn-small btn-secondary" onclick="eliminarEvidencia(${idx})" title="Eliminar foto">❌</button>
          </div>
        </div>
      </div>
    `;
    container.appendChild(card);
  });
}

function subirEvidencia(idx) {
  if (idx <= 0) return;
  const temp = certificadoState.evidencias[idx];
  certificadoState.evidencias[idx] = certificadoState.evidencias[idx - 1];
  certificadoState.evidencias[idx - 1] = temp;
  renderEvidenciasGrid();
  renderLiveHtmlSheet();
}

function bajarEvidencia(idx) {
  const evs = certificadoState.evidencias || [];
  if (idx >= evs.length - 1) return;
  const temp = certificadoState.evidencias[idx];
  certificadoState.evidencias[idx] = certificadoState.evidencias[idx + 1];
  certificadoState.evidencias[idx + 1] = temp;
  renderEvidenciasGrid();
  renderLiveHtmlSheet();
}

function actualizarNombreEvidencia(idx, nuevoNombre) {
  if (certificadoState.evidencias && certificadoState.evidencias[idx]) {
    certificadoState.evidencias[idx].titulo = nuevoNombre;
    certificadoState.evidencias[idx].nombre_mostrar = nuevoNombre;
    renderLiveHtmlSheet();
  }
}

function eliminarEvidencia(idx) {
  certificadoState.evidencias.splice(idx, 1);
  renderEvidenciasGrid();
  renderLiveHtmlSheet();
}

function normalizarAlarmaJS(al) {
  let status = al.status || 'Activo';
  let equipo = (al.equipo || '-').trim();
  let sensor = (al.sensor || '-').trim();
  let correo = al.correo || '-';
  let conf_min = al.conf_min || '-';
  let conf_max = al.conf_max || '-';
  let medicion = al.medicion || '-';
  let envio = al.envio || '60';

  const esSensorEnEquipo = (
    /^\(\d+\)/.test(equipo) ||
    equipo.toLowerCase().includes("sensor") ||
    equipo.includes(" - ") ||
    equipo.toLowerCase().includes("pontón") ||
    equipo.toLowerCase().includes("ponton") ||
    equipo.toLowerCase().includes("jaula")
  );

  if (esSensorEnEquipo) {
    const matchEq = equipo.match(/(Equipo\s*\d+)/i);
    const eqExtraido = matchEq ? matchEq[1] : "-";

    if (sensor === "-" || !sensor || sensor.toLowerCase() === "sin sensor") {
      sensor = equipo;
    }
    equipo = eqExtraido !== "-" ? eqExtraido : "Equipo 1";
  }

  if (/^\(\d+\)/.test(equipo) || equipo.includes(" - ")) {
    const matchEq = equipo.match(/(Equipo\s*\d+)/i);
    equipo = matchEq ? matchEq[1] : "Equipo 1";
  }

  let sensorClean = sensor.replace(/^\(\d+\)\s*/, '');
  if (sensorClean.includes(" - ")) {
    sensorClean = sensorClean.split(" - ")[0].trim();
  }

  if (!medicion || medicion === "-" || /^\(\d+\)/.test(medicion) || medicion.includes(" - ")) {
    const sLow = (sensor + " " + equipo + " " + sensorClean).toLowerCase();
    if (sLow.includes("oxygen") || sLow.includes("oxigeno") || sLow.includes("oxígeno") || sLow.includes("oxi")) {
      medicion = "Oxígeno";
    } else if (sLow.includes("salinity") || sLow.includes("salinidad")) {
      medicion = "Salinidad";
    } else if (sLow.includes("temperature") || sLow.includes("temperatura")) {
      medicion = "Temperatura";
    } else if (sLow.includes("orp")) {
      medicion = "ORP";
    } else if (sLow.includes("ph")) {
      medicion = "pH";
    } else if (sLow.includes("conductivid") || sLow.includes("conductivity")) {
      medicion = "Conductividad";
    } else {
      medicion = "Oxígeno";
    }
  }

  return {
    status: status,
    equipo: equipo,
    sensor: sensorClean || '-',
    correo: correo,
    conf_min: conf_min,
    conf_max: conf_max,
    medicion: medicion,
    envio: envio
  };
}

function renderAlarmasTabla() {
  const tbody = document.getElementById("tbodyAlarmas");
  if (!tbody) return;

  tbody.innerHTML = "";
  const alarmas = certificadoState.configuracion_alarmas || [];

  if (alarmas.length === 0) {
    tbody.innerHTML = `<tr><td colspan="9" style="text-align:center; color:var(--text-muted);">Sin alarmas configuradas. Cargue un Excel o agregue una fila.</td></tr>`;
    return;
  }

  alarmas.forEach((alRaw, idx) => {
    const al = normalizarAlarmaJS(alRaw);
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><input type="text" value="${al.status}" onchange="actualizarAlarma(${idx}, 'status', this.value)"></td>
      <td><input type="text" value="${al.equipo}" onchange="actualizarAlarma(${idx}, 'equipo', this.value)"></td>
      <td><input type="text" value="${al.sensor}" onchange="actualizarAlarma(${idx}, 'sensor', this.value)"></td>
      <td><input type="text" value="${al.correo}" onchange="actualizarAlarma(${idx}, 'correo', this.value)"></td>
      <td><input type="text" value="${al.conf_min}" onchange="actualizarAlarma(${idx}, 'conf_min', this.value)"></td>
      <td><input type="text" value="${al.conf_max}" onchange="actualizarAlarma(${idx}, 'conf_max', this.value)"></td>
      <td><input type="text" value="${al.medicion}" onchange="actualizarAlarma(${idx}, 'medicion', this.value)"></td>
      <td><input type="text" value="${al.envio}" onchange="actualizarAlarma(${idx}, 'envio', this.value)"></td>
      <td><button class="btn btn-small btn-secondary" onclick="eliminarAlarma(${idx})" title="Eliminar alarma">❌</button></td>
    `;
    tbody.appendChild(tr);
  });
}

function actualizarAlarma(idx, key, val) {
  if (!certificadoState.configuracion_alarmas) certificadoState.configuracion_alarmas = [];
  certificadoState.configuracion_alarmas[idx][key] = val;
  renderLiveHtmlSheet();
}

function agregarFilaAlarmaVacia() {
  if (!certificadoState.configuracion_alarmas) certificadoState.configuracion_alarmas = [];
  certificadoState.configuracion_alarmas.push({
    status: "Activada", equipo: "Equipo 1", sensor: "Sensor 5 mts Pontón", correo: "centro@camanchaca.cl",
    conf_min: "4,5", conf_max: "16,0", medicion: "Oxígeno", envio: "60"
  });
  renderAlarmasTabla();
  renderLiveHtmlSheet();
}

function eliminarAlarma(idx) {
  if (certificadoState.configuracion_alarmas) {
    certificadoState.configuracion_alarmas.splice(idx, 1);
    renderAlarmasTabla();
    renderLiveHtmlSheet();
  }
}

// RENDERIZADO INSTANTÁNEO A4 LIVE HTML 100% IDÉNTICO A REPORTLAB PDF
function renderLiveHtmlSheet() {
  try {
    if (moduloActivoActual !== "certificado") {
      return;
    }
    const sheet = document.getElementById("liveHtmlSheet") || document.getElementById("reportlabSheet");
    if (!sheet) return;

    const dg = (certificadoState && certificadoState.datos_generales) || {};
    const inf = (certificadoState && certificadoState.infraestructura) || {};
    const acc = (certificadoState && certificadoState.acceso_remoto) || {};
    const cam = (certificadoState && certificadoState.estacion_camara) || {};
    const ab = (certificadoState && certificadoState.monitoreo_abiotico) || {};
    const act = (certificadoState && certificadoState.activacion) || {};
    const ubs = (certificadoState && certificadoState.ubicaciones) || [];
    const reps = (certificadoState && certificadoState.equipos_repuesto) || [];
    const als = (certificadoState && certificadoState.configuracion_alarmas) || [];
    const evs = (certificadoState && certificadoState.evidencias) || [];

    const fichaNo = dg.numero_ficha ? (dg.numero_ficha.startsWith("DS-") ? dg.numero_ficha : `DS-${dg.numero_ficha}`) : `DS-${(dg.location || "001").toUpperCase()}`;

    let htmlUbicacionesTables = "";
    if (!ubs || ubs.length === 0) {
      htmlUbicacionesTables = `<div style="font-size:10px; color:#666666; margin-bottom:8px;">Sin ubicaciones registradas.</div>`;
    } else {
      ubs.forEach(u => {
        if (!u) return;
        let rows = "";
        const elemList = u.elementos || u.equipos || [];
        if (!elemList || elemList.length === 0) {
          rows = `<tr><td colspan="4" style="text-align:center; color:#999999;">Sin equipos en esta ubicación.</td></tr>`;
        } else {
          elemList.forEach((el, idx) => {
            if (!el) return;
            const nombreEq = el.nombre || el.name || "";
            const tipoEq = el.tipo || "-";
            const labelEq = nombreEq ? `${nombreEq} (${tipoEq})` : tipoEq;
            const ident = el.mac ? `MAC: ${el.mac}` : (el.serie ? `S/N: ${el.serie}` : '-');

            let sensoresStr = "";
            if (el.sensores && el.sensores.length > 0) {
              const sensoresOrd = [...el.sensores].sort((a, b) => parseFloat(a.metros || 0) - parseFloat(b.metros || 0));
              sensoresStr = sensoresOrd.map(s => `• ${s.tipo_sensor || 'Sensor'} (${s.metros ? s.metros + 'm' : '-'})${s.sn ? ' [S/N: ' + s.sn + ']' : ''}`).join("<br>");
            } else if (el.metraje) {
              sensoresStr = `${el.metraje} metros`;
            } else {
              sensoresStr = "-";
            }

            rows += `<tr>
              <td style="text-align:center;">${idx + 1}</td>
              <td><strong>${labelEq}</strong></td>
              <td><code>${ident}</code></td>
              <td>${sensoresStr}</td>
            </tr>`;
          });
        }

        const coordsText = u.coordenadas ? ` <span style="font-weight:normal; color:#666666;">(GPS: ${u.coordenadas})</span>` : '';
        htmlUbicacionesTables += `
          <div style="font-size:10px; font-weight:bold; color:#333333; margin-top:6px; margin-bottom:3px;">
            Ubicación: ${u.nombre || 'Ubicación'}${coordsText}
          </div>
          <table class="reportlab-list-table">
            <thead>
              <tr>
                <th style="width:30px;">N°</th>
                <th>Equipo / Elemento</th>
                <th>MAC</th>
                <th>Sensores Asociados (Tipo — Metros)</th>
              </tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        `;
      });
    }

    let htmlRepuestosRows = "";
    if (reps && reps.length) {
      reps.forEach(r => {
        if (!r) return;
        const ident = r.mac ? `MAC: ${r.mac}` : (r.serie ? `S/N: ${r.serie}` : '-');
        htmlRepuestosRows += `<tr><td>${r.tipo || '-'}</td><td>${r.metraje ? r.metraje + 'm' : '-'}</td><td>${ident}</td></tr>`;
      });
    }

    let htmlAlarmasRows = "";
    if (als && als.length) {
      als.forEach(al => {
        if (!al) return;
        const norm = normalizarAlarmaJS(al);
        htmlAlarmasRows += `<tr>
          <td>${norm.status}</td>
          <td>${norm.equipo}</td>
          <td>${norm.sensor}</td>
          <td>${norm.correo}</td>
          <td>${norm.conf_min}</td>
          <td>${norm.conf_max}</td>
          <td>${norm.medicion}</td>
          <td>${norm.envio}</td>
        </tr>`;
      });
    }

    const chkData = act.checklist || {};
    const checklistItems = [
      { key: "pc_operativo", desc: "Computador instalado y operativo" },
      { key: "red_validada", desc: "Configuración de red validada" },
      { key: "antena_operativa", desc: "Antena receptora operativa" },
      { key: "jennic_comunicando", desc: "Todos los equipos Jennic comunicando" },
      { key: "sensores_datos", desc: "Sensores detectados y entregando datos" },
      { key: "archivos_dat", desc: "Archivos .dat generándose y guardándose" },
      { key: "transmision_estacion", desc: "Transmisión datos Estación Meteorológica" },
      { key: "transmision_camara", desc: "Transmisión datos Fotográficos" },
      { key: "datos_dataweb", desc: "Datos visibles y actualizando en DataWeb" },
      { key: "alarmas_estandar", desc: "Alarmas configuradas según estándar" }
    ];

    let htmlChecklistRows = "";
    checklistItems.forEach(ci => {
      const val = (chkData[ci.key] || "OK").toUpperCase();
      const isOk = val === "OK" || val === "SI" || val === "CONFORME";
      const isNA = val === "N/A" || val === "NO APLICA";
      const okMark = isOk ? "[ ✔ ]" : "[   ]";
      const naMark = isNA ? "[ ✔ ]" : "[   ]";
      const obs = isOk ? "Conforme" : (isNA ? "N/A" : "Pendiente");

      htmlChecklistRows += `<tr>
        <td>${ci.desc}</td>
        <td style="text-align:center;">${okMark}</td>
        <td style="text-align:center;">${naMark}</td>
        <td>${obs}</td>
      </tr>`;
    });

    const abioticoSeccionHtml = (ab.instalado !== 'No') ? `
      <tr><td class="attr">¿Monitoreo Abiótico?</td><td class="val">${ab.instalado || 'Si'}</td></tr>
      <tr><td class="attr">Tipo y Ubicación de Antena</td><td class="val">${ab.tipo_antena || 'Outdoor'} (${ab.ubicacion_antena || 'Púlpito / Techo'})</td></tr>
      <tr><td class="attr">Versión Firmware / MAC</td><td class="val">${ab.version || '-'} | MAC: ${ab.mac || '-'}</td></tr>
      <tr><td class="attr">Pan ID</td><td class="val">${ab.panid || '-'}</td></tr>
      ${ab.cantidad_equipos_asociados ? `<tr><td class="attr">Equipos Jennic Asociados</td><td class="val">${ab.cantidad_equipos_asociados}</td></tr>` : ''}
    ` : '';

    sheet.innerHTML = `
      <!-- Encabezado Oficial ReportLab 3 Cajas -->
      <div class="reportlab-header-box">
        <div class="reportlab-header-left">
          <img src="/static/assets/innovex-logo.png" alt="Innovex">
        </div>
        <div class="reportlab-header-center">
          VALIDACIÓN DE INSTALACIÓN
        </div>
        <div class="reportlab-header-right">
          <div class="row"><div class="lbl">N° Ficha</div><div class="val">${fichaNo}</div></div>
          <div class="row"><div class="lbl">Periodo</div><div class="val">2026</div></div>
          <div class="row"><div class="lbl">Páginas</div><div class="val">1 de 1</div></div>
        </div>
      </div>

      <!-- 1. Datos Generales -->
      <div class="reportlab-sec-title">1. Información general del centro</div>
      <table class="reportlab-attr-table">
        <tr><td class="attr">Location ID (Centro)</td><td class="val">${dg.location || '<em style="color:#ef4444;">[Sin asignar]</em>'}</td></tr>
        <tr><td class="attr">Nombre del Centro</td><td class="val">${dg.nombre_centro || '<em style="color:#ef4444;">[Sin asignar]</em>'}</td></tr>
        <tr><td class="attr">Empresa Cliente</td><td class="val">${dg.empresa || '-'}</td></tr>
        <tr><td class="attr">Encargado de Área</td><td class="val">${dg.encargado_area || '-'}</td></tr>
        ${dg.area ? `<tr><td class="attr">Área (Zona Geográfica)</td><td class="val">${dg.area}</td></tr>` : ''}
        <tr><td class="attr">Técnico de Visita</td><td class="val">${dg.tecnico_visita || '-'}</td></tr>
        <tr><td class="attr">Fecha de Instalación</td><td class="val">${dg.fecha_instalacion || '-'}</td></tr>
        <tr><td class="attr">Teléfono del Centro</td><td class="val">${dg.telefono_centro || dg.numero_centro || '-'}</td></tr>
        <tr><td class="attr">Correo del Centro</td><td class="val">${dg.correo_centro || '-'}</td></tr>
        <tr><td class="attr">Barrio / Zona</td><td class="val">${dg.barrio || '-'}</td></tr>
        <tr><td class="attr">Puerto Patrón</td><td class="val">${dg.puerto_patron || '-'}</td></tr>
        <tr><td class="attr">Coordenadas GPS</td><td class="val">${dg.coordenadas || '-'}</td></tr>
      </table>

      <!-- 2. Infraestructura & Conectividad -->
      <div class="reportlab-sec-title">2. Infraestructura del PC de Monitoreo & Conectividad</div>
      <table class="reportlab-attr-table">
        ${inf.area ? `<tr><td class="attr">Área</td><td class="val">${inf.area}</td></tr>` : ''}
        <tr><td class="attr">Categoría Equipo</td><td class="val">${inf.categoria || '-'}</td></tr>
        <tr><td class="attr">Marca / Modelo</td><td class="val">${inf.marca || ''} ${inf.modelo || ''}</td></tr>
        <tr><td class="attr">Sistema Operativo</td><td class="val">${inf.sistema_operativo || '-'}</td></tr>
        ${inf.kernel ? `<tr><td class="attr">Kernel</td><td class="val">${inf.kernel}</td></tr>` : ''}
        <tr><td class="attr">MAC Ethernet</td><td class="val">${inf.mac_ethernet || '-'}</td></tr>
        ${inf.mac_wifi ? `<tr><td class="attr">MAC Wi-Fi</td><td class="val">${inf.mac_wifi}</td></tr>` : ''}
        <tr><td class="attr">ID Equipo / PC</td><td class="val">${inf.pc_id || '-'}</td></tr>
        <tr><td class="attr">Contraseña PC</td><td class="val">${inf.pc_password || '-'}</td></tr>
        <tr><td class="attr">Tipo de Conexión IP</td><td class="val">${inf.tipo_ip || 'IP VPN tun0'}</td></tr>
        ${(inf.tipo_ip === 'IP Fija' || inf.tipo_ip === 'Ambas') ? `<tr><td class="attr">IP Fija PC</td><td class="val">${inf.ip_fija || '-'}</td></tr>` : ''}
        ${(inf.tipo_ip === 'IP VPN tun0' || inf.tipo_ip === 'Ambas' || !inf.tipo_ip) ? `<tr><td class="attr">IP VPN tun0</td><td class="val">${inf.ip_vpn || acc.tun0 || '-'}</td></tr>` : ''}
        <tr><td class="attr">Protocolo VPN</td><td class="val">${acc.protocolo || '-'}</td></tr>
        <tr><td class="attr">Servidor Host / Puerto</td><td class="val">${acc.hostserver || 'dataweb.innovex.cl'}:${acc.puerto_server || '8888'}</td></tr>
      </table>

      <!-- 3. Antena, Cámara & Estación Meteorológica -->
      <div class="reportlab-sec-title">3. Antena, Estación Meteorológica & Cámara</div>
      <table class="reportlab-attr-table">
        ${abioticoSeccionHtml}
        <tr>
          <td class="attr">Estación Meteorológica</td>
          <td class="val">${cam.estacion_instalada === 'Si' ? `${cam.modelo_estacion || 'Davis'} ${cam.id_estacion_meteorologica ? `[ID: ${cam.id_estacion_meteorologica}]` : ''} ${cam.altura_estacion ? `[Altura: ${cam.altura_estacion}m]` : ''} ${cam.modelo_estacion === 'Davis' && cam.region_davis ? `(Región ${cam.region_davis})` : ''} - Ubicación: ${cam.ubicacion_estacion || 'Pontón'}` : 'No'}</td>
        </tr>
        <tr>
          <td class="attr">Cámara de Alimentación</td>
          <td class="val">${cam.camara_instalada === 'Si' ? `${cam.modelo_camara || 'Domo'} ${cam.mac_camara ? `[MAC: ${cam.mac_camara}]` : ''} (${cam.conexion_camara || 'Switch PoE'}) - IP: ${cam.ip_fija_camara || '-'} - Ubicación: ${cam.ubicacion_camara || 'Pontón'}` : 'No'}</td>
        </tr>
        <tr>
          <td class="attr">Switch PoE</td>
          <td class="val">${cam.switch_poe === 'Si' && cam.conexion_camara === 'Switch PoE' ? `${cam.modelo_switch || 'DS-3E0105P-E(B)'} - Ubicación: ${cam.ubicacion_switch || 'Pontón'}` : 'No'}</td>
        </tr>
      </table>

      ${ab.instalado !== 'No' ? `
        <!-- 4. Ubicaciones e Instalación -->
        <div class="reportlab-sec-title">4. Detalle de equipos instalados por ubicación</div>
        ${htmlUbicacionesTables}

        <!-- 5. Repuestos -->
        <div class="reportlab-sec-title">5. Equipos de repuesto (Almacenamiento: ${certificadoState.ubicacion_repuestos || 'Bodega Pontón'})</div>
        ${(reps && reps.length) ? `
          <table class="reportlab-list-table">
            <thead><tr><th>Tipo de Equipo</th><th>Metros</th><th>MAC</th></tr></thead>
            <tbody>${htmlRepuestosRows}</tbody>
          </table>
        ` : '<div style="font-size:10px; color:#666666; margin-bottom:8px;">Sin repuestos registrados.</div>'}
      ` : ''}

      <!-- Activación -->
      <div class="reportlab-sec-title">${ab.instalado !== 'No' ? '6' : '4'}. Validación de activación del servicio</div>
      <table class="reportlab-attr-table">
        <tr><td class="attr">IP Asignada / Interfaz</td><td class="val">${act.ip_final || '-'} (${act.interfaz || '-'})</td></tr>
        <tr><td class="attr">Responsable Activación</td><td class="val">${act.responsable_activacion || '-'}</td></tr>
        <tr><td class="attr">Estado Final</td><td class="val"><strong>${act.estado_final || 'Operativo'}</strong></td></tr>
      </table>
      <div style="font-weight:bold; font-size:10px; margin-top:6px; margin-bottom:3px; color:#222222;">Checklist de Validación de Operatividad:</div>
      <table class="reportlab-list-table">
        <thead><tr><th>Validación</th><th style="text-align:center;">OK</th><th style="text-align:center;">N/A</th><th>Observación</th></tr></thead>
        <tbody>${htmlChecklistRows}</tbody>
      </table>

      <!-- Alarmas -->
      ${(als && als.length) ? `
        <div class="reportlab-sec-title">${ab.instalado !== 'No' ? '7' : '5'}. Configuración de alarmas</div>
        <table class="reportlab-list-table">
          <thead><tr><th>Status</th><th>Equipo</th><th>Sensor</th><th>Usuario</th><th>Mín</th><th>Máx</th><th>Medición</th><th>Envío</th></tr></thead>
          <tbody>${htmlAlarmasRows}</tbody>
        </table>
      ` : ''}

      <!-- Observaciones -->
      <div class="reportlab-sec-title">${ab.instalado !== 'No' ? (als && als.length ? '8' : '7') : (als && als.length ? '6' : '5')}. Observaciones y notas libres</div>
      <div class="reportlab-obs-box">
        ${certificadoState.observaciones || '<span style="color:#aaaaaa;">[ Espacio reservado para notas de campo y firma del cliente ]</span>'}
      </div>

      <!-- Registro Fotográfico -->
      ${(evs && evs.length) ? `
        <div class="reportlab-sec-title">${ab.instalado !== 'No' ? (als && als.length ? '9' : '8') : (als && als.length ? '7' : '6')}. Registro fotográfico</div>
        <div style="font-size:10px; color:#555555; margin-bottom:8px;">Adjuntas ${evs.length} fotografía(s) de evidencia técnica.</div>
      ` : ''}
    `;
  } catch (err) {
    console.error("Error en renderLiveHtmlSheet:", err);
  }
}

let sensoresDraft = {};

function agregarSensorDraft(ubIdx) {
  const tipoSensor = document.getElementById(`elem_sensor_tipo_${ubIdx}`).value;
  const metros = document.getElementById(`elem_sensor_metros_${ubIdx}`).value.trim();
  const snInput = document.getElementById(`elem_sensor_sn_${ubIdx}`);
  const sn = snInput ? snInput.value.trim() : "";
  if (!sensoresDraft[ubIdx]) sensoresDraft[ubIdx] = [];
  sensoresDraft[ubIdx].push({ tipo_sensor: tipoSensor, metros: metros, sn: sn });
  if (snInput) snInput.value = "";
  const mInput = document.getElementById(`elem_sensor_metros_${ubIdx}`);
  if (mInput) mInput.value = "";
  renderSensoresDraft(ubIdx);
}

function eliminarSensorDraft(ubIdx, sIdx) {
  if (sensoresDraft[ubIdx]) {
    sensoresDraft[ubIdx].splice(sIdx, 1);
    renderSensoresDraft(ubIdx);
  }
}

function renderSensoresDraft(ubIdx) {
  const container = document.getElementById(`lista_sensores_draft_${ubIdx}`);
  if (!container) return;
  const list = sensoresDraft[ubIdx] || [];
  if (list.length === 0) {
    container.innerHTML = `<span style="font-size: 11px; color: var(--text-muted);">Sin sensores asociados.</span>`;
    return;
  }
  container.innerHTML = list.map((s, idx) => `
    <span class="badge badge-info" style="margin:2px; display:inline-flex; align-items:center; gap:4px;">
      ${s.tipo_sensor} (${s.metros ? s.metros + 'm' : '-'})${s.sn ? ' [S/N: ' + s.sn + ']' : ''}
      <button type="button" onclick="eliminarSensorDraft(${ubIdx}, ${idx})" style="border:none; background:transparent; color:red; cursor:pointer; font-weight:bold;">×</button>
    </span>
  `).join(" ");
}

function renderUbicacionesList() {
  const container = document.getElementById("contenedorUbicaciones");
  if (!container) return;

  container.innerHTML = "";
  const ubicaciones = certificadoState.ubicaciones || [];

  if (ubicaciones.length === 0) {
    container.innerHTML = `<div class="subtitle">No hay ubicaciones registradas.</div>`;
    return;
  }

  ubicaciones.forEach((ub, ubIdx) => {
    const card = document.createElement("div");
    card.className = "ubicacion-card";
    const coordsStr = ub.coordenadas ? ` (${ub.coordenadas})` : "";
    const elementos = ub.elementos || [];

    let elementosRows = "";
    elementos.forEach((elem, elIdx) => {
      const nombreEq = elem.nombre || elem.name || "";
      const tipoEq = elem.tipo || "-";
      const labelEq = nombreEq ? `<strong>${nombreEq}</strong> (${tipoEq})` : `<strong>${tipoEq}</strong>`;
      const serieStr = elem.serie || elem.mac || "-";
      
      let sensoresHtml = "";
      if (elem.sensores && elem.sensores.length > 0) {
        const sensoresOrd = [...elem.sensores].sort((a, b) => parseFloat(a.metros || 0) - parseFloat(b.metros || 0));
        sensoresHtml = sensoresOrd.map(s => {
          const snStr = s.sn ? ` [S/N: ${s.sn}]` : '';
          return `<span class="badge badge-info" style="margin:2px;">${s.tipo_sensor} (${s.metros ? s.metros + 'm' : '-'})${snStr}</span>`;
        }).join(" ");
      } else if (elem.metraje) {
        sensoresHtml = `<span class="badge badge-secondary">${elem.metraje}m</span>`;
      } else {
        sensoresHtml = `<span style="color:#aaa;">Sin sensores</span>`;
      }

      elementosRows += `
        <tr>
          <td>${labelEq}</td>
          <td><code>${serieStr}</code></td>
          <td>${sensoresHtml}</td>
          <td style="width: 40px; text-align: center;">
            <button class="btn btn-small btn-secondary" onclick="eliminarElementoUbicacion(${ubIdx}, ${elIdx})" title="Eliminar equipo">❌</button>
          </td>
        </tr>
      `;
    });

    const motesList = certificadoState.motes || [];
    const motesOrdenados = [...motesList].sort((a, b) => {
      const nameA = a.asociacion || a.name || "";
      const nameB = b.asociacion || b.name || "";
      return nameA.localeCompare(nameB, undefined, { numeric: true, sensitivity: 'base' });
    });

    let motesOptionsHtml = `<option value="">-- Seleccionar Mote detectado (${motesList.length} detectados) --</option>`;
    motesOrdenados.forEach(m => {
      const name = m.asociacion || m.name || `Equipo ${m.mote || ''}`;
      motesOptionsHtml += `<option value="${m.mac}" data-name="${name}">${name} (MAC: ${m.mac})</option>`;
    });

    const motesDropdownElemHtml = motesList.length > 0 ? `
      <div class="form-group" style="grid-column: span 3;">
        <label style="color: var(--primary-color, #2563eb);">Asignar MAC y Nombre de Mote Detectado</label>
        <select id="select_mote_elem_${ubIdx}" onchange="
          if(this.value){ 
            document.getElementById('elem_serie_${ubIdx}').value = this.value; 
            const selectedOpt = this.options[this.selectedIndex];
            if(selectedOpt && selectedOpt.dataset.name) {
              document.getElementById('elem_nombre_${ubIdx}').value = selectedOpt.dataset.name;
            }
          }">
          ${motesOptionsHtml}
        </select>
      </div>
    ` : '';

    card.innerHTML = `
      <div class="ubicacion-header">
        <div>
          <h3>${ub.nombre} <span style="font-size:12px; color:var(--text-muted);">${coordsStr}</span></h3>
        </div>
        <div>
          <button class="btn btn-small btn-primary" onclick="mostrarFormNuevoElemento(${ubIdx})">➕ Elemento</button>
          <button class="btn btn-small btn-secondary" onclick="eliminarUbicacion(${ubIdx})">❌ Eliminar</button>
        </div>
      </div>

      <div id="formNuevoElem_${ubIdx}" class="inline-form-card" style="display: none;">
        <h3>Agregar Equipo Instalado en ${ub.nombre}</h3>
        <div class="form-grid">
          ${motesDropdownElemHtml}
          <div class="form-group">
            <label>Tipo Equipo</label>
            <select id="elem_tipo_${ubIdx}">
              ${TIPOS_EQUIPOS.map(t => `<option value="${t}">${t}</option>`).join("")}
            </select>
          </div>
          <div class="form-group">
            <label>Nombre / Identificador Equipo</label>
            <input type="text" id="elem_nombre_${ubIdx}" placeholder="ej. Name 1 / Mote 01">
          </div>
          <div class="form-group">
            <label>MAC</label>
            <input type="text" id="elem_serie_${ubIdx}" placeholder="ej. 00:15:8D:00:09:24:53:F7">
          </div>
        </div>

        <div style="margin-top: 12px; padding: 10px; background: var(--bg-color, #f8fafc); border-radius: 6px; border: 1px solid var(--border-color, #e2e8f0);">
          <h4 style="font-size: 12px; font-weight: 600; margin-bottom: 8px;">Sensores Asociados a este Equipo</h4>
          <div class="form-grid">
            <div class="form-group">
              <label>Tipo Sensor</label>
              <select id="elem_sensor_tipo_${ubIdx}">
                ${TIPOS_SENSORES.map(s => `<option value="${s}">${s}</option>`).join("")}
              </select>
            </div>
            <div class="form-group">
              <label>Metros (m)</label>
              <input type="text" id="elem_sensor_metros_${ubIdx}" placeholder="ej. 5">
            </div>
            <div class="form-group">
              <label>S/N Sensor (Opcional)</label>
              <input type="text" id="elem_sensor_sn_${ubIdx}" placeholder="ej. SN-98765">
            </div>
            <div class="form-group" style="display: flex; align-items: flex-end;">
              <button type="button" class="btn btn-small btn-secondary" onclick="agregarSensorDraft(${ubIdx})">➕ Agregar Sensor</button>
            </div>
          </div>
          <div id="lista_sensores_draft_${ubIdx}" style="margin-top: 6px;"></div>
        </div>

        <div class="form-buttons" style="margin-top: 12px;">
          <button class="btn btn-primary btn-small" onclick="guardarElementoUbicacion(${ubIdx})">Guardar Equipo</button>
          <button class="btn btn-secondary btn-small" onclick="ocultarFormNuevoElemento(${ubIdx})">Cancelar</button>
        </div>
      </div>

      ${elementos.length > 0 ? `
        <table class="elementos-table">
          <thead><tr><th>Equipo / Elemento</th><th>MAC</th><th>Sensores Asociados (Tipo — Metros)</th><th>Acción</th></tr></thead>
          <tbody>${elementosRows}</tbody>
        </table>
      ` : `<div class="subtitle" style="margin-top:8px;">Sin equipos instalados.</div>`}
    `;

    container.appendChild(card);
  });
}

function guardarNuevaUbicacionInline() {
  const nombre = document.getElementById("nueva_ub_nombre").value.trim();
  const coords = document.getElementById("nueva_ub_coords").value.trim();
  if (!nombre) return;

  if (!certificadoState.ubicaciones) certificadoState.ubicaciones = [];
  certificadoState.ubicaciones.push({ nombre: nombre, coordenadas: coords, elementos: [] });

  document.getElementById("nueva_ub_nombre").value = "";
  document.getElementById("nueva_ub_coords").value = "";
  document.getElementById("formNuevaUbicacion").style.display = "none";

  renderUbicacionesList();
  renderLiveHtmlSheet();
}

function eliminarUbicacion(idx) {
  certificadoState.ubicaciones.splice(idx, 1);
  renderUbicacionesList();
  renderLiveHtmlSheet();
}

function mostrarFormNuevoElemento(ubIdx) {
  sensoresDraft[ubIdx] = [];
  const f = document.getElementById(`formNuevoElem_${ubIdx}`);
  if (f) f.style.display = "block";
  renderSensoresDraft(ubIdx);
}

function ocultarFormNuevoElemento(ubIdx) {
  sensoresDraft[ubIdx] = [];
  const f = document.getElementById(`formNuevoElem_${ubIdx}`);
  if (f) f.style.display = "none";
}

function guardarElementoUbicacion(ubIdx) {
  const tipo = document.getElementById(`elem_tipo_${ubIdx}`).value;
  const nombre = document.getElementById(`elem_nombre_${ubIdx}`).value.trim();
  const serie = document.getElementById(`elem_serie_${ubIdx}`).value.trim();

  const ub = certificadoState.ubicaciones[ubIdx];
  if (!ub.elementos) ub.elementos = [];

  const sensores = sensoresDraft[ubIdx] || [];

  ub.elementos.push({
    tipo: tipo,
    nombre: nombre,
    serie: serie,
    mac: serie,
    sensores: [...sensores]
  });

  sensoresDraft[ubIdx] = [];
  ocultarFormNuevoElemento(ubIdx);
  renderUbicacionesList();
  renderLiveHtmlSheet();
}

function eliminarElementoUbicacion(ubIdx, elIdx) {
  certificadoState.ubicaciones[ubIdx].elementos.splice(elIdx, 1);
  renderUbicacionesList();
  renderLiveHtmlSheet();
}

function renderRepuestosList() {
  const container = document.getElementById("listaRepuestos");
  if (!container) return;

  container.innerHTML = "";
  const repuestos = certificadoState.equipos_repuesto || [];

  if (repuestos.length === 0) {
    container.innerHTML = `<div class="subtitle">No hay equipos de repuesto registrados.</div>`;
    return;
  }

  repuestos.forEach((rep, idx) => {
    const item = document.createElement("div");
    item.className = "repuesto-item";
    const esJennic = (rep.tipo || "").toLowerCase().includes("jennic");
    let identStr = esJennic ? (rep.mac ? ` — MAC: ${rep.mac}` : '') : (` ${rep.metraje ? rep.metraje + 'm' : ''}` + (rep.serie ? ` — S/N: ${rep.serie}` : ''));

    item.innerHTML = `
      <div class="info"><strong>${idx + 1}. ${rep.tipo}</strong>${identStr}</div>
      <button class="btn btn-small btn-secondary" onclick="eliminarRepuesto(${idx})"></button>
    `;
    container.appendChild(item);
  });
}

function renderMotesList() {
  const container = document.getElementById("contenedorMotesList");
  if (!container) return;

  const motes = certificadoState.motes || [];
  if (motes.length === 0) {
    container.innerHTML = `
      <div style="padding: 12px; background: var(--bg-tertiary, #f8fafc); border-radius: 6px; border: 1px dashed var(--border-color, #cbd5e1); font-size: 13px; color: var(--text-muted);">
        No se han detectado equipos Jennic. Pegue la salida del comando <code>cmd motes</code> o <code>cmd status</code> en el <strong>Auto-rellenado Inteligente</strong> para importar la lista de MACs automáticamente.
      </div>
    `;
    return;
  }

  let rowsHtml = "";
  motes.forEach((m, idx) => {
    const moteNo = m.mote || (idx + 1);
    const mac = m.mac || "-";
    const signal = m.signal || "-";
    const lastRx = m.last_rx || "-";
    const asoc = m.asociacion || m.name || `Equipo ${moteNo}`;

    rowsHtml += `
      <tr>
        <td><strong>Mote ${moteNo}</strong></td>
        <td><code>${mac}</code></td>
        <td>${signal}</td>
        <td>${lastRx}</td>
        <td><span class="badge badge-info">${asoc}</span></td>
        <td style="text-align: center;">
          <button class="btn btn-small btn-secondary" onclick="copiarMacAlPortapapeles('${mac}')" title="Copiar MAC">Copiar</button>
        </td>
      </tr>
    `;
  });

  container.innerHTML = `
    <table class="elementos-table">
      <thead>
        <tr>
          <th>N° Mote</th>
          <th>MAC Address</th>
          <th>Señal</th>
          <th>Last Rx</th>
          <th>Asociación / Nombre</th>
          <th>Acción</th>
        </tr>
      </thead>
      <tbody>${rowsHtml}</tbody>
    </table>
  `;
}

function renderRepuestosMotesDropdown() {
  const sel = document.getElementById("rep_mac_select");
  if (!sel) return;

  const motes = certificadoState.motes || [];
  if (motes.length === 0) {
    sel.innerHTML = `<option value="">-- No hay motes detectados (Pegue cmd motes en autofill) --</option>`;
    return;
  }

  let html = `<option value="">-- Seleccionar MAC de cmd motes (${motes.length} detectados) --</option>`;
  motes.forEach(m => {
    const name = m.asociacion || m.name || `Equipo ${m.mote || ''}`;
    html += `<option value="${m.mac}">Mote ${m.mote || ''}: ${m.mac} (${name})</option>`;
  });
  sel.innerHTML = html;
}

function copiarMacAlPortapapeles(mac) {
  if (!mac) return;
  if (navigator.clipboard) {
    navigator.clipboard.writeText(mac).then(() => {
      mostrarToast(`MAC ${mac} copiada al portapapeles`, "success");
    }).catch(() => {
      mostrarToast(`MAC: ${mac}`, "info");
    });
  } else {
    mostrarToast(`MAC: ${mac}`, "info");
  }
}

function guardarNuevoRepuestoInline() {
  const tipo = document.getElementById("rep_tipo_select").value;
  const esJennic = tipo === "Equipo Jennic";
  const mac = document.getElementById("rep_mac_input").value.trim();
  const serie = document.getElementById("rep_serie_input").value.trim();
  const metraje = document.getElementById("rep_metraje_input").value.trim();

  if (!certificadoState.equipos_repuesto) certificadoState.equipos_repuesto = [];
  certificadoState.equipos_repuesto.push({
    tipo: tipo, cant: 1, cantidad: 1, descripcion: tipo, metraje: esJennic ? "" : metraje,
    mac: esJennic ? mac : "", serie: esJennic ? "" : serie, identificacion: esJennic ? mac : serie,
    ubicacion: certificadoState.ubicacion_repuestos || ""
  });

  document.getElementById("rep_mac_input").value = "";
  document.getElementById("rep_serie_input").value = "";
  document.getElementById("rep_metraje_input").value = "";
  document.getElementById("formNuevoRepuesto").style.display = "none";

  renderRepuestosList();
  renderLiveHtmlSheet();
}

function eliminarRepuesto(idx) {
  certificadoState.equipos_repuesto.splice(idx, 1);
  renderRepuestosList();
  renderLiveHtmlSheet();
}

async function cargarListaCertificadosHeader(autoLoadFirst = false) {
  const headerSel = document.getElementById("headerCertSelect");
  if (!headerSel) return;

  try {
    const res = await fetch("/api/list?año=2026");
    const data = await res.json();
    headerSel.innerHTML = "<option value=''>Cargar Certificado...</option>";

    if (data.status === "ok" && data.certificados.length > 0) {
      data.certificados.forEach(c => {
        const opt = document.createElement("option");
        opt.value = c;
        opt.textContent = c;
        headerSel.appendChild(opt);
      });

      if (autoLoadFirst && (!certificadoState.datos_generales || !certificadoState.datos_generales.location)) {
        headerSel.value = data.certificados[0];
        await cargarCertificadoPorLocation(data.certificados[0]);
      }
    }
  } catch (err) {
    headerSel.innerHTML = "<option value=''>Error de red</option>";
  }
}

async function cargarCertificadoPorLocation(locationId) {
  try {
    const res = await fetch("/api/load", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ location: locationId, año: 2026 })
    });
    const data = await res.json();

    if (data.status === "ok") {
      certificadoState = data.certificado;
      poblarFormularioDesdeState();
      mostrarToast(`Certificado cargado: ${locationId}`, "success");
    }
  } catch (err) {
    mostrarToast("Error al cargar certificado", "error");
  }
}

async function eliminarCertificadoPorLocation(locationId) {
  try {
    const res = await fetch("/api/delete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ location: locationId, año: 2026 })
    });
    const data = await res.json();

    if (data.status === "ok") {
      crearNuevoCertificadoSinPopup();
      await cargarListaCertificadosHeader(false);
      mostrarToast(data.mensaje || "Certificado eliminado exitosamente.", "success");
    } else {
      mostrarToast(data.mensaje || "Error al eliminar certificado", "error");
    }
  } catch (err) {
    mostrarToast("Error al eliminar certificado: " + err.message, "error");
  }
}

function validarCamposObligatorios() {
  const dg = certificadoState.datos_generales || {};
  const loc = (dg.location || "").trim();
  const nom = (dg.nombre_centro || "").trim();

  if (!loc || !nom) {
    mostrarToast("Location ID y Nombre del Centro son campos obligatorios.", "error");
    const tabBtn = document.querySelector(".tab-btn[data-tab='generales']");
    if (tabBtn) tabBtn.click();
    
    if (!loc) {
      const inputLoc = document.getElementById("gen_location");
      if (inputLoc) inputLoc.focus();
    } else if (!nom) {
      const inputNom = document.getElementById("gen_nombre_centro");
      if (inputNom) inputNom.focus();
    }
    return false;
  }
  return true;
}

// Compilar y Mostrar PDF Oficial
async function compilarYMostrarPDF() {
  if (!validarCamposObligatorios()) return;

  mostrarToast("Compilando PDF Oficial ReportLab...", "info");
  try {
    const res = await fetch("/api/generate_pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ certificado: certificadoState })
    });
    const data = await res.json();

    if (data.status === "ok" && data.pdf_preview_url) {
      const urlConCacheBuster = data.pdf_preview_url + "?t=" + new Date().getTime();
      window.open(urlConCacheBuster, "_blank");
      mostrarToast("✓ PDF Oficial generado y abierto en nueva pestaña.", "success");
      cargarListaCertificadosHeader(false);
    } else {
      mostrarToast("Error al compilar PDF: " + (data.mensaje || "Error desconocido"), "error");
    }
  } catch (err) {
    mostrarToast("Error al generar PDF: " + err.message, "error");
  }
}

function abrirVistaPreviaPopout() {
  const loc = certificadoState.datos_generales.location || "ce-tranqui1";
  const url = `/api/pdf_preview/2026/${loc}/certificado_inst_${loc}.pdf`;
  window.open(url, "_blank", "width=900,height=1000");
}

function verificarYEjecutarAutofill(nuevoHost, accionEjecutar) {
  const parsed = parseLocationInfo(nuevoHost);
  const locationActual = (certificadoState.datos_generales?.location || "").toLowerCase().trim();
  const locationNueva = (parsed.location || "").toLowerCase().trim();

  // Solo confirmar si realmente es un centro DISTINTO al actual y ninguno es el default vacío
  const esCentroDistinto = Boolean(
    locationActual &&
    locationNueva &&
    locationNueva !== "texto-pegado" &&
    locationActual !== "ce-tranqui1" &&
    locationActual !== locationNueva
  );

  if (!esCentroDistinto) {
    // Es el mismo centro, texto de consola pegado o inicio de ficha: ejecutar combinando directamente
    accionEjecutar({ limpiar: false });
    return;
  }

  const modal = document.getElementById("modalConfirmarCambioCentro");
  const modalTexto = document.getElementById("modalConfirmarTexto");
  const nombreCentroActual = certificadoState.datos_generales?.nombre_centro || locationActual || "Centro Previo";
  
  if (modalTexto) {
    modalTexto.innerHTML = `
      La ficha actual contiene datos cargados de <strong>${htmlEscapeAttr(nombreCentroActual)}</strong> (<em>${htmlEscapeAttr(locationActual)}</em> con ${certificadoState.motes?.length || 0} equipos y ${certificadoState.ubicaciones?.length || 0} ubicaciones).
      <br><br>
      ¿Desea <strong>limpiar e iniciar una ficha nueva</strong> para <strong>${htmlEscapeAttr(parsed.nombre_centro || nuevoHost)}</strong> o prefiere combinar los datos?
    `;
  }

  if (modal) modal.style.display = "flex";

  const btnLimpiar = document.getElementById("btnModalCambioLimpiar");
  const btnGuardar = document.getElementById("btnModalCambioGuardarPrimero");
  const btnCombinar = document.getElementById("btnModalCambioCombinar");
  const btnCancelar = document.getElementById("btnModalCambioCancelar");

  const cleanupListeners = () => {
    if (modal) modal.style.display = "none";
    if (btnLimpiar) btnLimpiar.onclick = null;
    if (btnGuardar) btnGuardar.onclick = null;
    if (btnCombinar) btnCombinar.onclick = null;
    if (btnCancelar) btnCancelar.onclick = null;
  };

  if (btnCancelar) {
    btnCancelar.onclick = () => {
      cleanupListeners();
      mostrarToast("Operación cancelada.", "info");
    };
  }

  if (btnLimpiar) {
    btnLimpiar.onclick = () => {
      cleanupListeners();
      crearNuevoCertificadoSinPopup();
      accionEjecutar({ limpiar: true });
    };
  }

  if (btnGuardar) {
    btnGuardar.onclick = async () => {
      cleanupListeners();
      mostrarToast("Guardando certificado anterior...", "info");
      await guardarAvance();
      crearNuevoCertificadoSinPopup();
      accionEjecutar({ limpiar: true });
    };
  }

  if (btnCombinar) {
    btnCombinar.onclick = () => {
      cleanupListeners();
      accionEjecutar({ limpiar: false });
    };
  }
}

async function procesarAutofill() {
  const texto = document.getElementById("autofillText")?.value || "";
  if (!texto.trim()) {
    mostrarToast("Por favor pegue la salida de consola en el cuadro", "warning");
    return;
  }

  const matchHost = texto.match(/static hostname:\s*([^\s\n]+)/i) || texto.match(/([a-z]{2}-[a-z0-9_-]+(?:\.acuimatic\.com)?)/i);
  const targetHost = matchHost ? matchHost[1] : "";

  verificarYEjecutarAutofill(targetHost || "Texto Pegado", async (opciones) => {
    try {
      const res = await fetch("/api/autofill", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          texto: texto,
          certificado: certificadoState,
          limpiar_previos: opciones?.limpiar ?? false
        })
      });
      const data = await res.json();

      if (data.status === "ok") {
        certificadoState = data.certificado;
        if (targetHost && targetHost !== "Texto Pegado") {
          const parsedTarget = parseLocationInfo(targetHost);
          if (!certificadoState.datos_generales) certificadoState.datos_generales = {};
          if (parsedTarget.location && (!certificadoState.datos_generales.location || certificadoState.datos_generales.location === "ce-tranqui1")) {
            certificadoState.datos_generales.location = parsedTarget.location;
          }
          if (parsedTarget.empresa && (!certificadoState.datos_generales.empresa || certificadoState.datos_generales.empresa === "Otro...")) {
            certificadoState.datos_generales.empresa = parsedTarget.empresa;
          }
          if (parsedTarget.nombre_centro && (!certificadoState.datos_generales.nombre_centro || certificadoState.datos_generales.nombre_centro === "TRANQUI 1")) {
            certificadoState.datos_generales.nombre_centro = parsedTarget.nombre_centro;
          }
        }
        poblarFormularioDesdeState();
        mostrarToast("Documento autorellenado y complementado con éxito.", "success");
        
        // Cambiar automáticamente de pestaña: "Auto-relleno Rápido" -> "1. Datos generales"
        activarSeccionTab("generales");
        document.querySelectorAll(".tab-btn").forEach(t => {
          if (t.dataset.tab === "generales") t.classList.add("active");
          else t.classList.remove("active");
        });
      } else {
        mostrarToast(`❌ Error al procesar: ${data.mensaje || "Error desconocido"}`, "error");
      }
    } catch (err) {
      mostrarToast(`❌ Error de conexión al parsear datos: ${err.message}`, "error");
    }
  });
}

async function ejecutarSSHAutofill() {
  const host = document.getElementById("ssh_autofill_host")?.value.trim();
  if (!host) {
    mostrarToast("Ingrese la IP o DNS del equipo remoto para conectar", "warning");
    return;
  }

  verificarYEjecutarAutofill(host, async (opciones) => {
    await realizarLlamadaSSHAutofill(opciones?.limpiar ?? false);
  });
}

async function realizarLlamadaSSHAutofill(limpiarPrevios = false) {
  const host = document.getElementById("ssh_autofill_host")?.value.trim();
  const usuario = document.getElementById("ssh_autofill_user")?.value.trim() || "innovex";
  const clave = document.getElementById("ssh_autofill_pass")?.value || "";
  const puerto_ssh = document.getElementById("ssh_autofill_port")?.value.trim() || "22";
  const puerto_telnet = document.getElementById("ssh_autofill_telnet_port")?.value.trim() || "9999";

  if (!host) {
    mostrarToast("Ingrese la IP o DNS del equipo remoto", "warning");
    return;
  }

  const btn = document.getElementById("btnEjecutarSSHAutofill");
  const origText = btn ? btn.textContent : "";
  if (btn) {
    btn.disabled = true;
    btn.textContent = "Conectando...";
  }

  try {
    const res = await fetch("/api/ssh_autofill", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        host, usuario, clave, puerto_ssh, puerto_telnet,
        certificado: certificadoState,
        limpiar_previos: limpiarPrevios
      })
    });
    const data = await res.json();

    if (data.status === "ok" && data.certificado) {
      certificadoState = data.certificado;
      if (host) {
        const parsedHost = parseLocationInfo(host);
        if (!certificadoState.datos_generales) certificadoState.datos_generales = {};
        if (parsedHost.location) {
          certificadoState.datos_generales.location = parsedHost.location;
        }
        if (parsedHost.empresa && (!certificadoState.datos_generales.empresa || certificadoState.datos_generales.empresa === "Otro...")) {
          certificadoState.datos_generales.empresa = parsedHost.empresa;
        }
        if (parsedHost.nombre_centro && (!certificadoState.datos_generales.nombre_centro || certificadoState.datos_generales.nombre_centro === "TRANQUI 1")) {
          certificadoState.datos_generales.nombre_centro = parsedHost.nombre_centro;
        }
        if (!certificadoState.infraestructura) certificadoState.infraestructura = {};
        certificadoState.infraestructura.pc_id = host;
        if (clave) certificadoState.infraestructura.pc_password = clave;
      }
      poblarFormularioDesdeState();
      mostrarToast("Auto-rellenado por SSH/Telnet completado con éxito.", "success");
      
      // Cambiar automáticamente de pestaña: "Auto-relleno Rápido" -> "1. Datos generales"
      activarSeccionTab("generales");
      document.querySelectorAll(".tab-btn").forEach(t => {
        if (t.dataset.tab === "generales") t.classList.add("active");
        else t.classList.remove("active");
      });
    } else {
      mostrarToast(`❌ ${data.mensaje || "No se pudo consultar el equipo remoto"}`, "error");
    }
  } catch (err) {
    mostrarToast(`❌ Error de conexión SSH: ${err.message}`, "error");
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = origText;
    }
  }
}

function copiarComandoPortapapeles() {
  const cmdInput = document.getElementById("codeCommandCopy");
  if (cmdInput) {
    cmdInput.select();
    if (navigator.clipboard) {
      navigator.clipboard.writeText(cmdInput.value).then(() => {
        mostrarToast("Comando copiado al portapapeles", "success");
      });
    } else {
      document.execCommand("copy");
      mostrarToast("Comando copiado", "success");
    }
  }
}

function setupNavButtons() {
  document.addEventListener("click", (e) => {
    const prevBtn = e.target.closest(".nav-prev-btn");
    const nextBtn = e.target.closest(".nav-next-btn");

    if (prevBtn) {
      const targetTab = prevBtn.dataset.prev;
      activarSeccionTab(targetTab);
      document.querySelectorAll(".tab-btn").forEach(t => {
        if (t.dataset.tab === targetTab) t.classList.add("active");
        else t.classList.remove("active");
      });
    } else if (nextBtn) {
      const targetTab = nextBtn.dataset.next;
      activarSeccionTab(targetTab);
      document.querySelectorAll(".tab-btn").forEach(t => {
        if (t.dataset.tab === targetTab) t.classList.add("active");
        else t.classList.remove("active");
      });
    }
  });
}

async function guardarAvance() {
  if (!validarCamposObligatorios()) return;

  try {
    const res = await fetch("/api/save", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ certificado: certificadoState })
    });
    const data = await res.json();

    if (data.status === "ok") {
      mostrarToast("Certificado guardado exitosamente.", "success");
      cargarListaCertificadosHeader();
    }
  } catch (err) {
    mostrarToast("Error al guardar", "error");
  }
}

// ----------------------------------------------------
// MÓDULO REVISOR DE EQUIPOS Y VERIFICACIÓN DE INGRESO
// ----------------------------------------------------
let ultimoResultadoRevisor = null;

function setInputValue(id, val) {
  const el = document.getElementById(id);
  if (el) {
    el.value = (val !== undefined && val !== null) ? String(val) : "";
  }
}

async function ejecutarRevisorEquipos() {
  const centro = document.getElementById("rev_centro").value.trim();
  const host = document.getElementById("rev_host").value.trim();
  const usuario = document.getElementById("rev_usuario").value.trim();
  const contrasena = document.getElementById("rev_contrasena").value;
  const clave_pc = document.getElementById("rev_clave_pc")?.value || contrasena;
  const puerto_ssh = document.getElementById("rev_puerto_ssh").value.trim();
  const puerto_telnet = document.getElementById("rev_puerto_telnet").value.trim();

  const btn = document.getElementById("btnEjecutarRevisor");
  const origText = btn.textContent;
  btn.disabled = true;
  btn.textContent = "Ejecutando revisión...";

  try {
    const response = await fetch("/api/revisor/verificar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        centro, host, usuario, contrasena, clave_pc, puerto_ssh, puerto_telnet
      })
    });
    const data = await response.json();
    if (data.status === "error" || (data.resultado && data.resultado.error && !data.resultado.log_cacheton_raw && !data.resultado.status_raw && !data.resultado.motes_raw && !data.resultado.motes_texto_raw)) {
      const errMsg = data.mensaje || data.resultado?.error || "No fue posible conectar con el equipo. Verifique DNS/Host y credenciales SSH/Telnet.";
      mostrarToast(`❌ Error de conexión: ${errMsg}`, "error");
      return;
    }

    if (data.status === "ok" && data.resultado) {
      const res = data.resultado;
      ultimoResultadoRevisor = res;

      setInputValue("rev_tipo_conexion", res.tipo_conexion || "Wifi");
      setInputValue("rev_sistema_operativo", res.sistema_operativo || "N/D");
      setInputValue("rev_kernel", res.kernel || "N/D");
      setInputValue("rev_clave_pc", res.clave_pc || clave_pc || contrasena || "No configurada");
      setInputValue("rev_dataweb", res.dataweb || "Ok");

      setInputValue("rev_pcinnovex", res.pcinnovex || "N/A");
      setInputValue("rev_cacheton", res.cacheton || "N/A");
      setInputValue("rev_python3", res.python3_cacheton || res.python3 || "N/A");
      setInputValue("rev_weather_davis", res.weather_davis || "N/A");
      setInputValue("rev_visibility_cam", res.visibility_cam || "N/A");

      setInputValue("rev_version_equipos", res.version_equipos || "v2.0.2");
      setInputValue("rev_senal", res.senal || "N/A");
      setInputValue("rev_voltajes", res.voltajes || "N/A");

      setInputValue("rev_saturacion", res.saturacion || "OK");
      setInputValue("rev_salinidad", res.salinidad || "OK");
      setInputValue("rev_temperatura", res.temperatura || "OK");
      setInputValue("rev_camara", res.camara_estado || "OK");
      setInputValue("rev_estacion", res.estacion_estado || "OK");

      setInputValue("rev_repuesto_equipo", res.repuesto_equipo || "OK");
      setInputValue("rev_repuesto_sensor", res.repuesto_sensor || "OK");
      setInputValue("rev_repuesto_kit", res.repuesto_kit || "OK");
      setInputValue("rev_telefono", res.telefono || "");
      setInputValue("rev_correo", res.correo || "");

      const txtPlanoRev = res.plantilla_texto || construirPlantillaRevisorTextoClientSide();
      const txtAreaRev = document.getElementById("txtPlantillaRevisor");
      if (txtAreaRev) txtAreaRev.value = txtPlanoRev;

      const preDerechoRev = document.getElementById("preTextoPlanoDerecho");
      if (preDerechoRev && moduloActivoActual === "revisor") {
        preDerechoRev.textContent = txtPlanoRev;
      }

      generarPlantillaRevisor();
      actualizarVistaPreviaDerechaPorModulo();

      if (data.resultado.error) {
        mostrarToast(`⚠️ Revisión completada con observaciones: ${data.resultado.error}`, "warning");
      } else {
        mostrarToast("✅ Verificación completada y formulario autollenado con éxito", "success");
      }
    } else {
      mostrarToast(`❌ Error: ${data.mensaje || "No se pudo realizar la revisión"}`, "error");
    }
  } catch (err) {
    mostrarToast(`Error al ejecutar revisión: ${err.message}`, "error");
  } finally {
    btn.disabled = false;
    btn.textContent = origText;
  }
}

function construirPlantillaRevisorTextoClientSide() {
  const centroRaw = document.getElementById("rev_centro")?.value.trim() || document.getElementById("rev_host")?.value.trim() || "CENTRO";
  const centroClean = centroRaw.split(".")[0].trim();
  const parsed = parseLocationInfo(centroClean);
  let centroTitulo = centroClean.toUpperCase();
  if (centroClean.includes("-")) {
    const parts = centroClean.split("-");
    const prefix = parts[0].toUpperCase();
    if (parsed.nombre_centro) {
      centroTitulo = `${prefix}-${parsed.nombre_centro.toUpperCase()}`;
    }
  }

  const tipo_conexion = document.getElementById("rev_tipo_conexion")?.value || "Wifi";
  const so = document.getElementById("rev_sistema_operativo")?.value.trim() || "N/D";
  const kernel = document.getElementById("rev_kernel")?.value.trim() || "N/D";
  const clave_pc = document.getElementById("rev_clave_pc")?.value.trim() || document.getElementById("rev_contrasena")?.value.trim() || "No configurada";
  const dataweb = document.getElementById("rev_dataweb")?.value.trim() || "Ok";

  function fmtChangeset(val) {
    let str = (val || "").trim();
    if (!str || str.toUpperCase() === "N/A" || str.toUpperCase() === "NO DETECTADO" || str.toUpperCase() === "NONE") return "N/A";
    const m = str.match(/changeset:\s*(\d+)/i);
    if (m) return `changeset:   ${m[1]}`;
    const m2 = str.match(/^(\d+)$/);
    if (m2) return `changeset:   ${m2[1]}`;
    return str;
  }

  const pcinnovex = fmtChangeset(document.getElementById("rev_pcinnovex")?.value);
  const cacheton = fmtChangeset(document.getElementById("rev_cacheton")?.value);
  const python3_ver = fmtChangeset(document.getElementById("rev_python3")?.value);
  const weather_davis = document.getElementById("rev_weather_davis")?.value.trim() || "N/A";
  const visibility_cam = document.getElementById("rev_visibility_cam")?.value.trim() || "N/A";

  let version_equipos = document.getElementById("rev_version_equipos")?.value.trim() || "v2.0.2";
  if (version_equipos && !version_equipos.startsWith("v") && !version_equipos.startsWith("V")) {
    version_equipos = "v" + version_equipos;
  }

  let senal = document.getElementById("rev_senal")?.value.trim() || "N/A";
  if (senal && !senal.startsWith("igual o mayor a") && senal.toUpperCase() !== "N/A") {
    senal = "igual o mayor a " + senal;
  }

  let voltajes = document.getElementById("rev_voltajes")?.value.trim() || "N/A";
  if (voltajes && !voltajes.startsWith("igual o mayor a") && voltajes.toUpperCase() !== "N/A") {
    const vVal = voltajes.endsWith("V") || voltajes.endsWith("v") ? voltajes : voltajes + "V";
    voltajes = "igual o mayor a " + vVal;
  }

  const saturacion = document.getElementById("rev_saturacion")?.value.trim() || "OK";
  const salinidad = document.getElementById("rev_salinidad")?.value.trim() || "OK";
  const temperatura = document.getElementById("rev_temperatura")?.value.trim() || "OK";

  const camara_estado = document.getElementById("rev_camara")?.value || "OK";
  const estacion_estado = document.getElementById("rev_estacion")?.value || "OK";

  const repuesto_equipo = document.getElementById("rev_repuesto_equipo")?.value || "OK";
  const repuesto_sensor = document.getElementById("rev_repuesto_sensor")?.value || "OK";
  const repuesto_kit = document.getElementById("rev_repuesto_kit")?.value || "OK";

  const telefono = document.getElementById("rev_telefono")?.value.trim() || "";
  const correo = document.getElementById("rev_correo")?.value.trim() || "";
  const obs_raw = document.getElementById("rev_observaciones")?.value.trim() || "";

  let obs_formatted = "- ----";
  if (obs_raw && obs_raw !== "-") {
    const lines = obs_raw.split("\n").map(l => l.trim()).filter(Boolean);
    if (lines.length > 0) {
      obs_formatted = lines.map(l => l.startsWith("-") ? l : `- ${l}`).join("\n");
    }
  }

  return `VERIFICACIÓN INGRESO  ${centroTitulo}
1. Datos computador:
* Tipo Conexión: ${tipo_conexion}
* Sistema Operativo: ${so}
* Kernel: ${kernel}
* Clave: ${clave_pc}
* Visualización Dataweb: ${dataweb}
2. Paquetería computador:
* pcinnovex: ${pcinnovex}
* cacheton: ${cacheton}
* python3: ${python3_ver}
* Weather Davis: ${weather_davis}
* Visibility-cam: ${visibility_cam}
3. Equipos:
* Versión: ${version_equipos}
* Señal: ${senal}
* Voltajes: ${voltajes}
4. Validación de Variación de Mediciones en Superficie:
* Saturación 95% - 105%:  ${saturacion}
* Salinidad: 0Psu - 1Psu: ${salinidad}
* Temperatura Ambiente: ${temperatura}
5. Cámara: ${camara_estado}
6. Estación: ${estacion_estado}
7. Repuesto:
* Equipo: ${repuesto_equipo}
* Sensor: ${repuesto_sensor}
* Kit de limpieza: ${repuesto_kit}
8. Datos del centro:
* Teléfono: ${telefono}
* Correo: ${correo}
9. Observaciones:
${obs_formatted}`;
}

function renderHtmlLiveRevisorClientSide() {
  const centroRaw = document.getElementById("rev_centro")?.value.trim() || document.getElementById("rev_host")?.value.trim() || "CENTRO";
  const centroClean = centroRaw.split(".")[0].trim();
  const parsed = parseLocationInfo(centroClean);
  let centroTitulo = centroClean.toUpperCase();
  if (centroClean.includes("-")) {
    const parts = centroClean.split("-");
    const prefix = parts[0].toUpperCase();
    if (parsed.nombre_centro) {
      centroTitulo = `${prefix}-${parsed.nombre_centro.toUpperCase()}`;
    }
  }

  const host = document.getElementById("rev_host")?.value.trim() || "N/D";
  const tipo_conexion = document.getElementById("rev_tipo_conexion")?.value || "Wifi";
  const so = document.getElementById("rev_sistema_operativo")?.value.trim() || "N/D";
  const kernel = document.getElementById("rev_kernel")?.value.trim() || "N/D";
  const clave_pc = document.getElementById("rev_clave_pc")?.value.trim() || document.getElementById("rev_contrasena")?.value.trim() || "No configurada";
  const dataweb = document.getElementById("rev_dataweb")?.value.trim() || "Ok";

  function fmtChangeset(val) {
    let str = (val || "").trim();
    if (!str || str.toUpperCase() === "N/A" || str.toUpperCase() === "NO DETECTADO" || str.toUpperCase() === "NONE") return "N/A";
    const m = str.match(/changeset:\s*(\d+)/i);
    if (m) return `changeset:   ${m[1]}`;
    const m2 = str.match(/^(\d+)$/);
    if (m2) return `changeset:   ${m2[1]}`;
    return str;
  }

  const pcinnovex = fmtChangeset(document.getElementById("rev_pcinnovex")?.value);
  const cacheton = fmtChangeset(document.getElementById("rev_cacheton")?.value);
  const python3_ver = fmtChangeset(document.getElementById("rev_python3")?.value);
  const weather_davis = document.getElementById("rev_weather_davis")?.value.trim() || "N/A";
  const visibility_cam = document.getElementById("rev_visibility_cam")?.value.trim() || "N/A";

  let version_equipos = document.getElementById("rev_version_equipos")?.value.trim() || "v2.0.2";
  if (version_equipos && !version_equipos.startsWith("v") && !version_equipos.startsWith("V")) {
    version_equipos = "v" + version_equipos;
  }

  let senal = document.getElementById("rev_senal")?.value.trim() || "N/A";
  if (senal && !senal.startsWith("igual o mayor a") && senal.toUpperCase() !== "N/A") {
    senal = "igual o mayor a " + senal;
  }

  let voltajes = document.getElementById("rev_voltajes")?.value.trim() || "N/A";
  if (voltajes && !voltajes.startsWith("igual o mayor a") && voltajes.toUpperCase() !== "N/A") {
    const vVal = voltajes.endsWith("V") || voltajes.endsWith("v") ? voltajes : voltajes + "V";
    voltajes = "igual o mayor a " + vVal;
  }
  const voltDefaultVal = (voltajes && voltajes.toUpperCase() !== "N/A") ? (voltajes.replace("igual o mayor a", "").trim() || "N/D") : "N/D";

  const saturacion = document.getElementById("rev_saturacion")?.value.trim() || "OK";
  const salinidad = document.getElementById("rev_salinidad")?.value.trim() || "OK";
  const temperatura = document.getElementById("rev_temperatura")?.value.trim() || "OK";

  const camara_estado = document.getElementById("rev_camara")?.value || "OK";
  const estacion_estado = document.getElementById("rev_estacion")?.value || "OK";

  const repuesto_equipo = document.getElementById("rev_repuesto_equipo")?.value || "OK";
  const repuesto_sensor = document.getElementById("rev_repuesto_sensor")?.value || "OK";
  const repuesto_kit = document.getElementById("rev_repuesto_kit")?.value || "OK";

  const telefono = document.getElementById("rev_telefono")?.value.trim() || "N/D";
  const correo = document.getElementById("rev_correo")?.value.trim() || "N/D";
  const obs_raw = document.getElementById("rev_observaciones")?.value.trim() || "";

  let obs_formatted = "- ----";
  if (obs_raw && obs_raw !== "-") {
    const lines = obs_raw.split("\n").map(l => l.trim()).filter(Boolean);
    if (lines.length > 0) {
      obs_formatted = lines.map(l => l.startsWith("-") ? l : `- ${l}`).join("\n");
    }
  }

  const nodos = ultimoResultadoRevisor?.nodos_detalle || [];
  let filasNodosHtml = "";
  if (nodos.length > 0) {
    filasNodosHtml = nodos.map(item => {
      const nid = item.nodo || "-";
      const nom = htmlEscapeAttr(item.nombre || `Equipo ${nid}`);
      const mac = htmlEscapeAttr(item.mac || "N/D");
      const sig = htmlEscapeAttr(item.signal || "N/D");
      const vStr = htmlEscapeAttr(item.voltaje || voltDefaultVal);
      const lrx = htmlEscapeAttr(item.last_rx || "N/D");
      const lect = htmlEscapeAttr(item.lecturas_sensores || "Sin datos");
      const est = item.estado || "OK";
      const badgeCls = String(est).toUpperCase().includes("OK") ? "badge-ok" : "badge-warn";
      return `
        <tr>
          <td style="text-align: center;"><strong>#${nid}</strong></td>
          <td>${nom}</td>
          <td><code>${mac}</code></td>
          <td style="text-align: center;">${sig}</td>
          <td style="text-align: center;">${vStr}</td>
          <td>${lect}</td>
          <td style="text-align: center;">${lrx} s</td>
          <td><span class="badge ${badgeCls}">${htmlEscapeAttr(est)}</span></td>
        </tr>
      `;
    }).join("");
  } else {
    const defaultMotes = [
      { id: 1, nom: "3", mac: "00:15:8D:00:08:E4:BF:C5", sig: "114:120", rx: "12", est: "OK" },
      { id: 2, nom: "1", mac: "00:15:8D:00:08:BA:90:5D", sig: "78:84", rx: "17", est: "OK" },
      { id: 3, nom: "MALO", mac: "00:15:8D:00:09:F3:09:96", sig: "174:183", rx: "22", est: "MALO" },
      { id: 4, nom: "4", mac: "00:15:8D:00:09:F3:09:E3", sig: "57:72", rx: "109", est: "OK" },
      { id: 5, nom: "1", mac: "00:15:8D:00:05:69:EA:30", sig: "189:189", rx: "8", est: "OK" },
      { id: 6, nom: "2", mac: "00:15:8D:00:09:6C:A4:35", sig: "198:201", rx: "22", est: "OK" },
      { id: 7, nom: "1", mac: "00:15:8D:00:09:24:3D:A4", sig: "141:150", rx: "18", est: "OK" }
    ];
    filasNodosHtml = defaultMotes.map(m => {
      const badgeCls = m.est === "OK" ? "badge-ok" : "badge-warn";
      return `
        <tr>
          <td style="text-align: center;"><strong>#${m.id}</strong></td>
          <td>${htmlEscapeAttr(m.nom)}</td>
          <td><code>${m.mac}</code></td>
          <td style="text-align: center;">${m.sig}</td>
          <td style="text-align: center;">${htmlEscapeAttr(voltDefaultVal)}</td>
          <td>Sin datos</td>
          <td style="text-align: center;">${m.rx} s</td>
          <td><span class="badge ${badgeCls}">${m.est}</span></td>
        </tr>
      `;
    }).join("");
  }

  const motesRaw = ultimoResultadoRevisor?.motes_texto_raw || "1 00:15:8D:00:08:E4:BF:C5   114:120      12  3\n2 00:15:8D:00:08:BA:90:5D   78:84      17  1\n3 00:15:8D:00:09:F3:09:96   174:183      22  MALO\n4 00:15:8D:00:09:F3:09:E3   57:72      109  4\n5 00:15:8D:00:05:69:EA:30   189:189      8  1\n6 00:15:8D:00:09:6C:A4:35   198:201      22  2\n7 00:15:8D:00:09:24:3D:A4   141:150      18  1";
  const statusRaw = ultimoResultadoRevisor?.salida_status || "Pancoordinator status\nVersion v2.0.2\nMicrolib version 2fa37f3\nMAC: 00:15:8D:00:08:DD:0B:8A\nPan ID: 1313\nChannel: 19\nN of motes attached: 7";

  return `
    <div class="reportlab-header-box" style="justify-content: center; text-align: center;">
      <div class="reportlab-header-center" style="width: 100%; text-align: center; font-size: 15px; font-weight: 800; letter-spacing: 0.5px;">
        VERIFICACIÓN DE INGRESO — ${htmlEscapeAttr(centroTitulo)}
      </div>
    </div>

    <div class="reportlab-sec-title">1. Datos del Computador</div>
    <table class="reportlab-attr-table">
      <tr><td class="attr">Tipo Conexión</td><td class="val">${htmlEscapeAttr(tipo_conexion)}</td></tr>
      <tr><td class="attr">Sistema Operativo</td><td class="val">${htmlEscapeAttr(so)}</td></tr>
      <tr><td class="attr">Kernel</td><td class="val">${htmlEscapeAttr(kernel)}</td></tr>
      <tr><td class="attr">Clave PC</td><td class="val">${htmlEscapeAttr(clave_pc)}</td></tr>
      <tr><td class="attr">Visualización Dataweb</td><td class="val">${htmlEscapeAttr(dataweb)}</td></tr>
    </table>

    <div class="reportlab-sec-title">2. Paquetería del Computador</div>
    <table class="reportlab-attr-table">
      <tr><td class="attr">pcinnovex</td><td class="val">${htmlEscapeAttr(pcinnovex)}</td></tr>
      <tr><td class="attr">cacheton</td><td class="val">${htmlEscapeAttr(cacheton)}</td></tr>
      <tr><td class="attr">python3</td><td class="val">${htmlEscapeAttr(python3_ver)}</td></tr>
      <tr><td class="attr">Weather Davis</td><td class="val">${htmlEscapeAttr(weather_davis)}</td></tr>
      <tr><td class="attr">Visibility-cam</td><td class="val">${htmlEscapeAttr(visibility_cam)}</td></tr>
    </table>

    <div class="reportlab-sec-title">3. Equipos</div>
    <table class="reportlab-attr-table">
      <tr><td class="attr">Versión</td><td class="val">${htmlEscapeAttr(version_equipos)}</td></tr>
      <tr><td class="attr">Señal</td><td class="val">${htmlEscapeAttr(senal)}</td></tr>
      <tr><td class="attr">Voltajes</td><td class="val">${htmlEscapeAttr(voltajes)}</td></tr>
    </table>

    <div class="reportlab-sec-title">Detalle de Nodos Conectados</div>
    <table class="reportlab-list-table">
      <thead>
        <tr>
          <th style="width: 35px; text-align: center;">Nodo</th>
          <th>Nombre Equipo</th>
          <th>Dirección MAC</th>
          <th style="width: 65px; text-align: center;">Señal</th>
          <th style="width: 65px; text-align: center;">Voltaje</th>
          <th>Lecturas Sensores</th>
          <th style="width: 65px; text-align: center;">Last RX</th>
          <th style="width: 55px;">Estado</th>
        </tr>
      </thead>
      <tbody>
        ${filasNodosHtml}
      </tbody>
    </table>

    <div class="reportlab-sec-title">4. Validación de Variación de Mediciones en Superficie</div>
    <table class="reportlab-attr-table">
      <tr><td class="attr">Saturación 95% - 105%</td><td class="val">${htmlEscapeAttr(saturacion)}</td></tr>
      <tr><td class="attr">Salinidad 0Psu - 1Psu</td><td class="val">${htmlEscapeAttr(salinidad)}</td></tr>
      <tr><td class="attr">Temperatura Ambiente</td><td class="val">${htmlEscapeAttr(temperatura)}</td></tr>
    </table>

    <div class="reportlab-sec-title">5. Cámara & 6. Estación</div>
    <table class="reportlab-attr-table">
      <tr><td class="attr">5. Cámara</td><td class="val">${htmlEscapeAttr(camara_estado)}</td></tr>
      <tr><td class="attr">6. Estación</td><td class="val">${htmlEscapeAttr(estacion_estado)}</td></tr>
    </table>

    <div class="reportlab-sec-title">7. Repuesto</div>
    <table class="reportlab-attr-table">
      <tr><td class="attr">Equipo</td><td class="val">${htmlEscapeAttr(repuesto_equipo)}</td></tr>
      <tr><td class="attr">Sensor</td><td class="val">${htmlEscapeAttr(repuesto_sensor)}</td></tr>
      <tr><td class="attr">Kit de limpieza</td><td class="val">${htmlEscapeAttr(repuesto_kit)}</td></tr>
    </table>

    <div class="reportlab-sec-title">8. Datos del Centro</div>
    <table class="reportlab-attr-table">
      <tr><td class="attr">Teléfono</td><td class="val">${htmlEscapeAttr(telefono)}</td></tr>
      <tr><td class="attr">Correo</td><td class="val">${htmlEscapeAttr(correo)}</td></tr>
    </table>

    <div class="reportlab-sec-title">9. Observaciones</div>
    <div style="background: #f8fafc; border: 1px solid #cccccc; padding: 8px 12px; border-radius: 4px; font-family: monospace; white-space: pre-wrap;">${htmlEscapeAttr(obs_formatted)}</div>

    <div class="reportlab-sec-title">Consola Técnica Raw (STATUS & CMD MOTES)</div>
    <pre class="console">--- CMD MOTES OUTPUT ---
${htmlEscapeAttr(motesRaw)}

--- STATUS OUTPUT ---
${htmlEscapeAttr(statusRaw)}</pre>
  `;
}

let temporizadorActualizacionRevisor = null;
let secuenciaGeneracionRevisor = 0;

function programarActualizacionRevisor() {
  window.clearTimeout(temporizadorActualizacionRevisor);
  // Actualizar la vista previa de inmediato en JS
  construirPlantillaRevisorDesdeFormulario();
  temporizadorActualizacionRevisor = window.setTimeout(() => {
    temporizadorActualizacionRevisor = null;
    generarPlantillaRevisor();
  }, 300);
}

function construirPlantillaRevisorDesdeFormulario() {
  const txt = construirPlantillaRevisorTextoClientSide();
  const txtArea = document.getElementById("txtPlantillaRevisor");
  if (txtArea) txtArea.value = txt;

  if (moduloActivoActual === "revisor") {
    if (modoVistaPreviaModulos === "texto") {
      const pre = document.getElementById("preTextoPlanoDerecho");
      if (pre) pre.textContent = txt;
    } else {
      mostrarVistaPreviaRevisorDerecha();
    }
  }
}

async function generarPlantillaRevisor({ notificar = false } = {}) {
  window.clearTimeout(temporizadorActualizacionRevisor);
  temporizadorActualizacionRevisor = null;
  const solicitudActual = ++secuenciaGeneracionRevisor;

  const centroRaw = document.getElementById("rev_centro")?.value.trim() || document.getElementById("rev_host")?.value.trim() || "CENTRO";
  const centroClean = centroRaw.split(".")[0].trim();
  const parsed = parseLocationInfo(centroClean);
  let centroTitulo = centroClean.toUpperCase();
  if (centroClean.includes("-")) {
    const parts = centroClean.split("-");
    const prefix = parts[0].toUpperCase();
    if (parsed.nombre_centro) {
      centroTitulo = `${prefix}-${parsed.nombre_centro.toUpperCase()}`;
    }
  }

  const host = document.getElementById("rev_host")?.value.trim() || "";
  const tipo_conexion = document.getElementById("rev_tipo_conexion")?.value || "Wifi";
  const sistema_operativo = document.getElementById("rev_sistema_operativo")?.value.trim() || "N/D";
  const kernel = document.getElementById("rev_kernel")?.value.trim() || "N/D";
  const clave_pc = document.getElementById("rev_clave_pc")?.value.trim() || document.getElementById("rev_contrasena")?.value.trim() || "No configurada";
  const dataweb = document.getElementById("rev_dataweb")?.value.trim() || "Ok";

  function fmtChangeset(val) {
    let str = (val || "").trim();
    if (!str || str.toUpperCase() === "N/A" || str.toUpperCase() === "NO DETECTADO" || str.toUpperCase() === "NONE") return "N/A";
    const m = str.match(/changeset:\s*(\d+)/i);
    if (m) return `changeset:   ${m[1]}`;
    const m2 = str.match(/^(\d+)$/);
    if (m2) return `changeset:   ${m2[1]}`;
    return str;
  }

  const pcinnovex = fmtChangeset(document.getElementById("rev_pcinnovex")?.value);
  const cacheton = fmtChangeset(document.getElementById("rev_cacheton")?.value);
  const python3_ver = fmtChangeset(document.getElementById("rev_python3")?.value);
  const weather_davis = document.getElementById("rev_weather_davis")?.value.trim() || "N/A";
  const visibility_cam = document.getElementById("rev_visibility_cam")?.value.trim() || "N/A";

  let version_equipos = document.getElementById("rev_version_equipos")?.value.trim() || "v2.0.2";
  if (version_equipos && !version_equipos.startsWith("v") && !version_equipos.startsWith("V")) {
    version_equipos = "v" + version_equipos;
  }

  let senal = document.getElementById("rev_senal")?.value.trim() || "N/A";
  if (senal && !senal.startsWith("igual o mayor a") && senal.toUpperCase() !== "N/A") {
    senal = "igual o mayor a " + senal;
  }

  let voltajes = document.getElementById("rev_voltajes")?.value.trim() || "N/A";
  if (voltajes && !voltajes.startsWith("igual o mayor a") && voltajes.toUpperCase() !== "N/A") {
    const vVal = voltajes.endsWith("V") || voltajes.endsWith("v") ? voltajes : voltajes + "V";
    voltajes = "igual o mayor a " + vVal;
  }

  const saturacion = document.getElementById("rev_saturacion")?.value.trim() || "OK";
  const salinidad = document.getElementById("rev_salinidad")?.value.trim() || "OK";
  const temperatura = document.getElementById("rev_temperatura")?.value.trim() || "OK";

  const camara_estado = document.getElementById("rev_camara")?.value || "OK";
  const estacion_estado = document.getElementById("rev_estacion")?.value || "OK";

  const repuesto_equipo = document.getElementById("rev_repuesto_equipo")?.value || "OK";
  const repuesto_sensor = document.getElementById("rev_repuesto_sensor")?.value || "OK";
  const repuesto_kit = document.getElementById("rev_repuesto_kit")?.value || "OK";

  const telefono = document.getElementById("rev_telefono")?.value.trim() || "";
  const correo = document.getElementById("rev_correo")?.value.trim() || "";
  const observaciones = document.getElementById("rev_observaciones")?.value || "";

  const nodos_detalle = ultimoResultadoRevisor?.nodos_detalle || [];
  const motes_texto_raw = ultimoResultadoRevisor?.motes_texto_raw || "";
  const salida_status = ultimoResultadoRevisor?.salida_status || "";

  const payload = {
    centro: centroTitulo,
    host,
    tipo_conexion,
    sistema_operativo,
    kernel,
    clave_pc,
    dataweb,
    pcinnovex,
    cacheton,
    python3_cacheton: python3_ver,
    weather_davis,
    visibility_cam,
    version_equipos,
    senal,
    voltajes,
    saturacion,
    salinidad,
    temperatura,
    camara_estado,
    estacion_estado,
    repuesto_equipo,
    repuesto_sensor,
    repuesto_kit,
    telefono,
    correo,
    observaciones,
    nodos_detalle,
    motes_texto_raw,
    salida_status
  };

  try {
    const response = await fetch("/api/revisor/generar_plantilla", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (solicitudActual !== secuenciaGeneracionRevisor) return "";

    if (data.status === "ok") {
      const txt = data.plantilla_texto || "";
      const htmlDoc = data.documento_live_html || "";

      document.getElementById("txtPlantillaRevisor").value = txt;
      if (!ultimoResultadoRevisor) ultimoResultadoRevisor = {};
      Object.assign(ultimoResultadoRevisor, payload, {
        plantilla_texto: txt,
        documento_live_html: htmlDoc
      });

      actualizarFrameDocumentoLive();

      if (moduloActivoActual === "revisor" && modoVistaPreviaModulos === "texto") {
        const pre = document.getElementById("preTextoPlanoDerecho");
        if (pre) pre.textContent = txt || "Sin texto disponible.";
      }

      if (notificar) mostrarToast("Plantilla y Documento Live actualizados", "success");
      return txt;
    }
  } catch (err) {
    console.error("Error al generar plantilla Revisor:", err);
  }
  return "";
}

async function copiarPlantillaRevisor() {
  let txt = document.getElementById("txtPlantillaRevisor")?.value || "";
  if (!txt.trim()) {
    txt = construirPlantillaRevisorTextoClientSide();
  }
  if (!txt.trim()) {
    mostrarToast("No hay plantilla para copiar.", "warning");
    return;
  }
  const copiado = await copiarTextoAlPortapapeles(txt);
  const btn = document.getElementById("btnCopiarPlantillaRevisor");
  if (btn && copiado) {
    const orig = btn.textContent;
    btn.textContent = "✓ ¡Copiado!";
    setTimeout(() => { btn.textContent = orig; }, 1800);
  }
  mostrarToast(
    copiado ? "Plantilla copiada al portapapeles con éxito" : "No se pudo copiar automáticamente al portapapeles",
    copiado ? "success" : "error"
  );
}

function actualizarFrameDocumentoLive() {
  const frame = document.getElementById("frameDocumentoLive");
  if (frame && ultimoResultadoRevisor && ultimoResultadoRevisor.documento_live_html) {
    if (frame.srcdoc !== ultimoResultadoRevisor.documento_live_html) {
      frame.srcdoc = ultimoResultadoRevisor.documento_live_html;
    }
  }
}

function autoRellenarDesdeRevisor() {
  if (!ultimoResultadoRevisor) {
    const centro = document.getElementById("rev_centro")?.value.trim();
    if (centro) {
      if (!certificadoState.datos_generales) certificadoState.datos_generales = {};
      certificadoState.datos_generales.location = centro.toLowerCase().replace(/[^a-z0-9_-]/g, "");
      certificadoState.datos_generales.nombre_centro = centro.toUpperCase();
      poblarFormularioDesdeState();
      mostrarToast("Datos principales actualizados en la ficha del certificado", "success");
    } else {
      mostrarToast("Ingrese al menos el nombre del centro para autorellenar", "warning");
    }
    return;
  }

  const r = ultimoResultadoRevisor;
  if (!certificadoState.datos_generales) certificadoState.datos_generales = {};
  if (!certificadoState.infraestructura) certificadoState.infraestructura = {};
  if (!certificadoState.acceso_remoto) certificadoState.acceso_remoto = {};
  if (!certificadoState.monitoreo_abiotico) certificadoState.monitoreo_abiotico = {};

  if (r.centro) {
    certificadoState.datos_generales.location = r.centro.toLowerCase().replace(/[^a-z0-9_-]/g, "");
    certificadoState.datos_generales.nombre_centro = r.centro.toUpperCase();
    const info = parseLocationInfo(r.centro);
    if (info.empresa) certificadoState.datos_generales.empresa = info.empresa;
  }
  if (r.sistema_operativo) certificadoState.infraestructura.sistema_operativo = r.sistema_operativo;
  if (r.kernel) certificadoState.infraestructura.kernel = r.kernel;
  if (r.host) certificadoState.acceso_remoto.tun0 = r.host;
  if (r.version_equipos) certificadoState.monitoreo_abiotico.version = r.version_equipos;
  if (r.telefono) certificadoState.datos_generales.telefono_centro = r.telefono;
  if (r.correo) certificadoState.datos_generales.correo_centro = r.correo;
  if (r.observaciones) certificadoState.observaciones = r.observaciones;

  poblarFormularioDesdeState();
  renderLiveHtmlSheet();
  mostrarToast("Ficha de certificado actualizada desde el Revisor (Centro, S.O., Kernel, Versión)", "success");
}

function extraerCuerpoHTML(htmlCompleto) {
  if (!htmlCompleto) return "";
  const m = htmlCompleto.match(/<body[^>]*>([\s\S]*)<\/body>/i);
  return m ? m[1].trim() : htmlCompleto;
}

function mostrarVistaPreviaRevisorDerecha() {
  if (modoVistaPreviaModulos === "texto") {
    mostrarTextoPlanoEnPanelDerecho();
    return;
  }

  const liveSheet = document.getElementById("liveHtmlSheet");
  if (!liveSheet) return;

  document.getElementById("liveHtmlContainer").style.display = "block";
  document.getElementById("btnToggleVistaHTML").classList.add("active");
  if (document.getElementById("btnToggleVistaPDF")) document.getElementById("btnToggleVistaPDF").classList.remove("active");
  if (document.getElementById("btnToggleVistaTexto")) document.getElementById("btnToggleVistaTexto").classList.remove("active");

  liveSheet.innerHTML = renderHtmlLiveRevisorClientSide();
}

function mostrarTextoPlanoEnPanelDerecho() {
  modoVistaPreviaModulos = "texto";
  const liveSheet = document.getElementById("liveHtmlSheet");
  if (!liveSheet) return;

  document.getElementById("liveHtmlContainer").style.display = "block";
  document.getElementById("btnToggleVistaHTML").classList.remove("active");
  if (document.getElementById("btnToggleVistaPDF")) document.getElementById("btnToggleVistaPDF").classList.remove("active");
  if (document.getElementById("btnToggleVistaTexto")) document.getElementById("btnToggleVistaTexto").classList.add("active");

  let textoPlano = "";
  if (moduloActivoActual === "revisor") {
    textoPlano = document.getElementById("txtPlantillaRevisor") ? document.getElementById("txtPlantillaRevisor").value : "";
    if (!textoPlano) {
      textoPlano = construirPlantillaRevisorTextoClientSide();
    }
  } else if (moduloActivoActual === "ingreso_tecnico") {
    textoPlano = document.getElementById("txtPlantillaIngresoTecnico") ? document.getElementById("txtPlantillaIngresoTecnico").value : "";
    if (!textoPlano) {
      textoPlano = construirPlantillaIngresoTextoClientSide();
    }
  }

  liveSheet.innerHTML = `
    <div class="plain-text-preview">
      <div class="plain-text-preview-header">
        <h3>Vista Texto Plano</h3>
      </div>
      <pre id="preTextoPlanoDerecho" class="plain-text-preview-content">${htmlEscapeAttr(textoPlano || "Sin texto disponible.")}</pre>
    </div>
  `;
}

function htmlEscapeAttr(str) {
  if (!str) return "";
  return String(str).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#39;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

async function copiarTextoAlPortapapeles(texto) {
  if (!texto) return false;

  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(texto);
      return true;
    }
  } catch (err) {
    console.warn("Portapapeles moderno falló, usando método fallback:", err);
  }

  try {
    const areaTemporal = document.createElement("textarea");
    areaTemporal.value = texto;
    areaTemporal.style.position = "fixed";
    areaTemporal.style.top = "-9999px";
    areaTemporal.style.left = "-9999px";
    areaTemporal.style.opacity = "0";
    areaTemporal.setAttribute("readonly", "");
    document.body.appendChild(areaTemporal);
    areaTemporal.focus();
    areaTemporal.select();
    areaTemporal.setSelectionRange(0, areaTemporal.value.length);
    const copiado = document.execCommand("copy");
    document.body.removeChild(areaTemporal);
    return !!copiado;
  } catch (err2) {
    console.error("Error en fallback execCommand:", err2);
    return false;
  }
}

async function copiarTextoPlanoDerecho() {
  let texto = document.getElementById("preTextoPlanoDerecho")?.textContent || "";
  if (!texto.trim() || texto === "Sin texto disponible.") {
    if (moduloActivoActual === "revisor") {
      texto = construirPlantillaRevisorTextoClientSide();
    } else if (moduloActivoActual === "ingreso_tecnico") {
      texto = construirPlantillaIngresoTextoClientSide();
    }
  }

  const copiado = await copiarTextoAlPortapapeles(texto);
  const btn = document.getElementById("btnCopiarTextoPlanoDerecho");
  if (btn && copiado) {
    const orig = btn.textContent;
    btn.textContent = "✓ ¡Copiado!";
    setTimeout(() => { btn.textContent = orig; }, 1800);
  }
  mostrarToast(
    copiado ? "Texto plano copiado al portapapeles" : "No se pudo copiar el texto plano",
    copiado ? "success" : "error"
  );
}

// MÓDULO INFORMACIÓN PARA INGRESO DE TÉCNICO
let ultimoResultadoIngreso = null;
let temporizadorActualizacionIngreso = null;
let secuenciaGeneracionIngreso = 0;

function construirPlantillaIngresoTextoClientSide() {
  const dns_host = document.getElementById("ingreso_host")?.value.trim() || "";
  const clave_pc = document.getElementById("ingreso_clave_pc")?.value.trim() || document.getElementById("ingreso_contrasena")?.value.trim() || "No configurada";
  const acceso_remoto = document.getElementById("ingreso_acceso_remoto")?.value.trim() || "OK";

  const antena_status = (document.getElementById("ingreso_antena_status")?.value || "").trim();
  const equipos_conectados = (document.getElementById("ingreso_equipos_conectados")?.value || "").trim();
  const voltaje_pilas = (document.getElementById("ingreso_voltaje_pilas")?.value || "").trim();

  const observaciones = (document.getElementById("ingreso_observaciones")?.value || "").trim();
  const observaciones_generales = (document.getElementById("ingreso_observaciones_generales")?.value || PLANTILLA_OBS_GENERALES_DEFAULT).trim();

  function indentTextObs(text) {
    if (!text) return "";
    return text.split("\n").map(l => {
      const s = l.trim();
      if (!s) return "";
      if (l.startsWith("    ") || l.startsWith("\t")) return `      - ${s}`;
      return `  • ${s}`;
    }).join("\n");
  }

  function indentTextGen(text) {
    if (!text) return "";
    return text.split("\n").map(l => {
      const s = l.trim();
      if (!s) return "";
      if (l.startsWith("    ") || l.startsWith("\t")) return `      - ${s}`;
      return `  ✓ ${s}`;
    }).join("\n");
  }

  return `DNS:${dns_host}
Clave PC:${clave_pc}
Acceso remoto: ${acceso_remoto}

Antena status:
${antena_status || "Sin datos: no fue posible obtener cmd status."}

Equipos conectados:
${equipos_conectados || "Sin datos: no fue posible obtener cmd motes."}

Voltaje pilas:
${voltaje_pilas || "Sin datos: se requieren credenciales SSH para consultar los voltajes."}

Observaciones:

${indentTextObs(observaciones)}

Observaciones generales:

${indentTextGen(observaciones_generales)}`;
}

function renderHtmlLiveIngresoClientSide() {
  const dns_host = htmlEscapeAttr(document.getElementById("ingreso_host")?.value.trim() || "ce-yelcho.acuimatic.com");
  const clave_pc = htmlEscapeAttr(document.getElementById("ingreso_clave_pc")?.value.trim() || document.getElementById("ingreso_contrasena")?.value.trim() || "No configurada");
  const acceso_remoto = htmlEscapeAttr(document.getElementById("ingreso_acceso_remoto")?.value.trim() || "OK");

  const rep_equipo = htmlEscapeAttr(document.getElementById("ingreso_repuesto_equipo")?.value || "OK");
  const rep_sensor = htmlEscapeAttr(document.getElementById("ingreso_repuesto_sensor")?.value || "OK");
  const rep_kit = htmlEscapeAttr(document.getElementById("ingreso_repuesto_kit")?.value || "OK");

  const antena_status_raw = document.getElementById("ingreso_antena_status")?.value || "Sin datos";
  const equipos_conectados_raw = document.getElementById("ingreso_equipos_conectados")?.value || "Sin datos";
  const voltaje_pilas_raw = document.getElementById("ingreso_voltaje_pilas")?.value || "Sin datos";
  const observaciones = htmlEscapeAttr(document.getElementById("ingreso_observaciones")?.value || "Sin observaciones registradas.");
  const obs_generales_raw = document.getElementById("ingreso_observaciones_generales")?.value || PLANTILLA_OBS_GENERALES_DEFAULT;

  return `
    <div class="reportlab-header-box" style="justify-content: center; text-align: center;">
      <div class="reportlab-header-center" style="width: 100%; text-align: center; font-size: 15px; font-weight: 800; letter-spacing: 0.5px;">
        INFORMACIÓN PARA INGRESO DE TÉCNICO
      </div>
    </div>

    <div class="reportlab-sec-title">1. Datos Generales & Acceso Remoto</div>
    <table class="reportlab-attr-table">
      <tr><td class="attr">DNS / Host</td><td class="val">${dns_host}</td></tr>
      <tr><td class="attr">Clave PC</td><td class="val">${clave_pc}</td></tr>
      <tr><td class="attr">Acceso Remoto</td><td class="val">${acceso_remoto}</td></tr>
    </table>

    <div class="reportlab-sec-title">2. Estado de Repuestos</div>
    <table class="reportlab-attr-table">
      <tr><td class="attr">Equipo Repuesto</td><td class="val">${rep_equipo}</td></tr>
      <tr><td class="attr">Sensor Repuesto</td><td class="val">${rep_sensor}</td></tr>
      <tr><td class="attr">Kit de Limpieza</td><td class="val">${rep_kit}</td></tr>
    </table>

    <div class="reportlab-sec-title">3. Antena Status</div>
    <pre class="console">${htmlEscapeAttr(antena_status_raw)}</pre>

    <div class="reportlab-sec-title">4. Equipos Conectados (cmd motes)</div>
    <pre class="console">${htmlEscapeAttr(equipos_conectados_raw)}</pre>

    <div class="reportlab-sec-title">5. Voltajes & Logs</div>
    <pre class="console">${htmlEscapeAttr(voltaje_pilas_raw)}</pre>

    <div class="reportlab-sec-title">6. Observaciones</div>
    <div style="background: #f8fafc; border: 1px solid #cccccc; padding: 8px 12px; border-radius: 4px; font-family: monospace; white-space: pre-wrap;">${observaciones}</div>

    <div class="reportlab-sec-title">7. Observaciones Generales</div>
    <div style="background: #f8fafc; border: 1px solid #cccccc; padding: 8px 12px; border-radius: 4px; font-family: monospace; white-space: pre-wrap;">${htmlEscapeAttr(obs_generales_raw)}</div>
  `;
}

function programarActualizacionIngreso() {
  window.clearTimeout(temporizadorActualizacionIngreso);
  const txt = construirPlantillaIngresoTextoClientSide();
  const txtArea = document.getElementById("txtPlantillaIngresoTecnico");
  if (txtArea) txtArea.value = txt;

  if (moduloActivoActual === "ingreso_tecnico") {
    if (modoVistaPreviaModulos === "texto") {
      const pre = document.getElementById("preTextoPlanoDerecho");
      if (pre) pre.textContent = txt;
    } else {
      mostrarVistaPreviaIngresoDerecha();
    }
  }

  temporizadorActualizacionIngreso = window.setTimeout(() => {
    temporizadorActualizacionIngreso = null;
    generarPlantillaIngreso();
  }, 450);
}

const PLANTILLA_OBS_GENERALES_DEFAULT = `Actualizar paquetería PC

Fotos de los repuestos en su ubicación final
    Bolso Innovex
    Equipo con su tapa y pantalla visible
    Sensor/es de repuesto con vista a su S/N, cabezal y tapa protectora


Fotos notebook/otros
    Entradas USB, cualquier conexión conectada/ocupada
    Componentes (Switch POE/Hub, antena, meteo-stick entre otros)
    Tomas de corriente
Fotos equipos transmisores
    Pantallas visibles
    Pedestales con metrajes claros
    Sin tapa (si es que la climática lo permite)
Información acerca del tipo de estación y cámara
Corroborar u obtener datos del centro, teléfono y correo electrónico.`;

function inicializarObservacionesGeneralesDefault() {
  const el = document.getElementById("ingreso_observaciones_generales");
  if (el && !el.value.trim()) {
    el.value = PLANTILLA_OBS_GENERALES_DEFAULT;
  }
}

function prellenarDatosHostIngresoTecnico() {
  // Dejar espacio en blanco por defecto como solicitó el usuario
}

async function ejecutarIngresoTecnico() {
  const host = document.getElementById("ingreso_host").value.trim();
  const usuario = document.getElementById("ingreso_usuario").value.trim() || "innovex";
  const contrasena = document.getElementById("ingreso_contrasena").value;
  const clave_pc = document.getElementById("ingreso_clave_pc").value.trim() || contrasena || "No configurada";
  document.getElementById("ingreso_clave_pc").value = clave_pc;

  const accesoRemotoInput = document.getElementById("ingreso_acceso_remoto");
  const acceso_remoto = accesoRemotoInput.value.trim() || "OK";
  accesoRemotoInput.value = acceso_remoto;
  const repuestos_equipo = document.getElementById("ingreso_repuesto_equipo")?.value || "OK";
  const repuestos_sensor = document.getElementById("ingreso_repuesto_sensor")?.value || "OK";
  const repuestos_kit = document.getElementById("ingreso_repuesto_kit")?.value || "OK";

  const observaciones = document.getElementById("ingreso_observaciones").value;
  const observaciones_generales = document.getElementById("ingreso_observaciones_generales").value;

  const btn = document.getElementById("btnEjecutarIngresoTecnico");
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = "Consultando / Generando...";
  }

  try {
    const response = await fetch("/api/revisor/ingreso_tecnico", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        host,
        usuario,
        contrasena,
        clave_pc,
        acceso_remoto,
        repuestos_equipo,
        repuestos_sensor,
        repuestos_kit,
        observaciones,
        observaciones_generales
      })
    });
    const data = await response.json();
    if (data.status === "ok" && data.resultado) {
      const res = data.resultado;
      ultimoResultadoIngreso = res;

      if (res.antena_status) document.getElementById("ingreso_antena_status").value = res.antena_status;
      if (res.equipos_conectados) document.getElementById("ingreso_equipos_conectados").value = res.equipos_conectados;
      if (res.voltaje_pilas) document.getElementById("ingreso_voltaje_pilas").value = res.voltaje_pilas;
      if (res.dns !== undefined) document.getElementById("ingreso_host").value = res.dns;
      if (res.clave_pc) document.getElementById("ingreso_clave_pc").value = res.clave_pc;
      if (res.acceso_remoto) document.getElementById("ingreso_acceso_remoto").value = res.acceso_remoto;

      // Sincronizar plantilla de texto plano de inmediato tanto en el input como en la vista previa
      const txtPlano = res.plantilla_texto || construirPlantillaIngresoTextoClientSide();
      const txtArea = document.getElementById("txtPlantillaIngresoTecnico");
      if (txtArea) txtArea.value = txtPlano;

      const preDerecho = document.getElementById("preTextoPlanoDerecho");
      if (preDerecho && moduloActivoActual === "ingreso_tecnico") {
        preDerecho.textContent = txtPlano;
      }

      actualizarFrameDocumentoIngresoLive();
      actualizarVistaPreviaDerechaPorModulo();
      generarPlantillaIngreso();

      mostrarToast("Información para ingreso de técnico cargada con éxito", "success");
    } else {
      mostrarToast("" + (data.mensaje || "Error al procesar consulta"), "error");
    }
  } catch (err) {
    console.error("Error en consulta ingreso técnico:", err);
    mostrarToast("Error de red o servidor al ejecutar consulta", "error");
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = "🔍 Consultar Remotamente";
    }
  }
}

async function generarPlantillaIngreso({ notificar = false } = {}) {
  window.clearTimeout(temporizadorActualizacionIngreso);
  temporizadorActualizacionIngreso = null;
  const solicitudActual = ++secuenciaGeneracionIngreso;
  const host = document.getElementById("ingreso_host").value.trim();
  const clave_pc = document.getElementById("ingreso_clave_pc").value.trim() || document.getElementById("ingreso_contrasena")?.value.trim() || "No configurada";
  document.getElementById("ingreso_clave_pc").value = clave_pc;

  const accesoRemotoInput = document.getElementById("ingreso_acceso_remoto");
  const acceso_remoto = accesoRemotoInput.value.trim() || "OK";
  accesoRemotoInput.value = acceso_remoto;
  const repuestos_equipo = document.getElementById("ingreso_repuesto_equipo")?.value || "OK";
  const repuestos_sensor = document.getElementById("ingreso_repuesto_sensor")?.value || "OK";
  const repuestos_kit = document.getElementById("ingreso_repuesto_kit")?.value || "OK";

  const antena_status = document.getElementById("ingreso_antena_status").value;
  const equipos_conectados = document.getElementById("ingreso_equipos_conectados").value;
  const voltaje_pilas = document.getElementById("ingreso_voltaje_pilas").value;
  const observaciones = document.getElementById("ingreso_observaciones").value;
  const observaciones_generales = document.getElementById("ingreso_observaciones_generales").value;

  try {
    const response = await fetch("/api/revisor/generar_plantilla_ingreso", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        dns: host,
        clave_pc,
        acceso_remoto,
        repuestos_equipo,
        repuestos_sensor,
        repuestos_kit,
        antena_status,
        equipos_conectados,
        voltaje_pilas,
        observaciones,
        observaciones_generales
      })
    });
    const data = await response.json();
    if (solicitudActual !== secuenciaGeneracionIngreso) return "";

    if (data.status === "ok") {
      document.getElementById("txtPlantillaIngresoTecnico").value = data.plantilla_texto || "";
      ultimoResultadoIngreso = {
        dns: host,
        clave_pc,
        acceso_remoto,
        repuestos_equipo,
        repuestos_sensor,
        repuestos_kit,
        antena_status,
        equipos_conectados,
        voltaje_pilas,
        observaciones,
        observaciones_generales,
        plantilla_texto: data.plantilla_texto,
        documento_live_html: data.documento_live_html
      };
      actualizarFrameDocumentoIngresoLive();
      if (moduloActivoActual === "ingreso_tecnico" && modoVistaPreviaModulos === "texto") {
        const pre = document.getElementById("preTextoPlanoDerecho");
        if (pre) pre.textContent = data.plantilla_texto || "Sin texto disponible.";
      }
      if (notificar) mostrarToast("Plantilla y Documento Live actualizados", "success");
      return data.plantilla_texto || "";
    }
  } catch (err) {
    console.error("Error al generar plantilla ingreso:", err);
    if (notificar) mostrarToast("No se pudo actualizar la plantilla", "error");
  }

  return "";
}

function actualizarFrameDocumentoIngresoLive() {
  const frame = document.getElementById("frameDocumentoIngresoLive");
  if (frame && ultimoResultadoIngreso && ultimoResultadoIngreso.documento_live_html) {
    frame.srcdoc = ultimoResultadoIngreso.documento_live_html;
  }
}

function mostrarVistaPreviaIngresoDerecha() {
  if (modoVistaPreviaModulos === "texto") {
    mostrarTextoPlanoEnPanelDerecho();
    return;
  }

  const liveSheet = document.getElementById("liveHtmlSheet");
  if (!liveSheet) return;

  document.getElementById("liveHtmlContainer").style.display = "block";
  document.getElementById("btnToggleVistaHTML").classList.add("active");
  if (document.getElementById("btnToggleVistaPDF")) document.getElementById("btnToggleVistaPDF").classList.remove("active");
  if (document.getElementById("btnToggleVistaTexto")) document.getElementById("btnToggleVistaTexto").classList.remove("active");

  liveSheet.innerHTML = renderHtmlLiveIngresoClientSide();
}

async function copiarPlantillaIngreso() {
  let txt = document.getElementById("txtPlantillaIngresoTecnico")?.value || "";
  if (!txt.trim()) {
    txt = construirPlantillaIngresoTextoClientSide();
  }

  const copiado = await copiarTextoAlPortapapeles(txt);
  const btn = document.getElementById("btnCopiarPlantillaIngreso");
  if (btn && copiado) {
    const orig = btn.textContent;
    btn.textContent = "✓ ¡Copiado!";
    setTimeout(() => { btn.textContent = orig; }, 1800);
  }
  mostrarToast(
    copiado ? "Plantilla de Ingreso de Técnico copiada al portapapeles" : "No se pudo copiar la plantilla",
    copiado ? "success" : "error"
  );
}

// ===================================================================
// FUNCIONALIDADES DEL PORTAL UNIFICADO DE SOPORTE INNOVEX
// ===================================================================

function restaurarVistaActivaPortal() {
  let vista = "";
  let submodulo = "";

  let rawHash = window.location.hash.replace(/^#+/, "").trim();
  if (rawHash) {
    rawHash = rawHash.split("?")[0].replace(/\/+$/, "");
    const parts = rawHash.split("/");
    vista = parts[0] || "";
    submodulo = parts[1] || "";
  }

  if (!vista || !document.getElementById(`view-${vista}`)) {
    try {
      vista = (localStorage.getItem("active_portal_view") || "").split("?")[0].replace(/\/+$/, "").trim();
      submodulo = (localStorage.getItem("active_portal_submodule") || "").split("?")[0].replace(/\/+$/, "").trim();
    } catch (e) {}
  }

  if (vista && document.getElementById(`view-${vista}`)) {
    window.navegarSeccionPortal(vista, submodulo);
  } else {
    window.navegarSeccionPortal("dashboard");
  }
}

function iniciarPortalUnificado() {
  iniciarRelojSidebar();
  setupSidebarNavigation();
  setupBitacoraHandlers();
  setupCorreosMasivosHandlers();
  setupGestorDestinatariosHandlers();
  setupPoseidon();
  setupTracSearch();
  // setupMusicPlayer(); // Deshabilitado temporalmente a petición del usuario

  // Escuchar cambios de navegación en la URL para mantener sección sin resetear a home
  window.addEventListener("hashchange", restaurarVistaActivaPortal);
  window.addEventListener("popstate", restaurarVistaActivaPortal);

  // Restaurar sección activa previa en F5 o enlace directo
  restaurarVistaActivaPortal();

  // Carga inicial de datos de fondo
  cargarBitacora();
  cargarDatosCorreosMasivos();
  cargarListaDestinatarios();
  cargarIndiceTracWiki();
}

// --- 1. Navegación entre Secciones del Portal ---
window.navegarSeccionPortal = function(vista, submodulo) {
  // Persistir vista activa en localStorage y Hash de la URL para que no vuelva al home tras F5
  try {
    localStorage.setItem("active_portal_view", vista);
    if (submodulo) {
      localStorage.setItem("active_portal_submodule", submodulo);
    } else {
      localStorage.removeItem("active_portal_submodule");
    }

    const hashTarget = submodulo ? `${vista}/${submodulo}` : vista;
    if (window.location.hash !== `#${hashTarget}`) {
      history.replaceState(null, "", `#${hashTarget}`);
    }
  } catch (e) {}

  // Actualizar estado activo en los botones del sidebar
  document.querySelectorAll(".sidebar-nav .nav-item:not(.external)").forEach(item => {
    const v = item.getAttribute("data-view");
    const sub = item.getAttribute("data-submodule");
    if (v === vista && (!submodulo || sub === submodulo)) {
      item.classList.add("active");
    } else {
      item.classList.remove("active");
    }
  });

  // Mostrar la vista correspondiente y ocultar las demás
  document.querySelectorAll(".portal-view").forEach(v => {
    v.classList.remove("active");
    v.style.display = "none";
  });

  const targetView = document.getElementById(`view-${vista}`);
  if (targetView) {
    targetView.classList.add("active");
    targetView.style.display = "block";
  }

  // Título en la barra superior (Breadcrumb)
  const titulos = {
    "dashboard": "Dashboard General",
    "bitacora": "Pizarra de Turno",
    "certificado-suite": "Suite de Certificados",
    "tickets-soporte": "Generador de Tickets de Falla",
    "correos-masivos": "Correos Masivos Fin de Semana",
    "gestionar-correos": "Gestor de Destinatarios",
    "poseidon": "Poseidón (Dual Monitor)",
    "calendario": "Calendario de Turnos",
    "trac-wiki": "Buscador Trac Wiki",
    "listado-comandos": "Listado de Comandos",
    "music": "Control Multimedia"
  };

  const titleElem = document.getElementById("currentViewTitle");
  if (titleElem) {
    titleElem.textContent = titulos[vista] || vista;
  }

  // Controles contextuales del módulo Certificado en la barra superior (solo en submódulo certificado)
  const certControls = document.getElementById("certContextControls");
  if (certControls) {
    const esCert = (vista === "certificado-suite" && (submodulo === "certificado" || (!submodulo && moduloActivoActual === "certificado")));
    certControls.style.display = esCert ? "flex" : "none";
  }

  // Si se entra a la suite de certificados, activar el submódulo correcto
  if (vista === "certificado-suite") {
    cambiarModuloActivo(submodulo || moduloActivoActual || "certificado");
  }

  // Recargar datos relevantes al entrar en ciertas vistas
  if (vista === "bitacora" || vista === "dashboard") {
    cargarBitacora();
  } else if (vista === "tickets-soporte") {
    inicializarModuloTicketsSoporte();
  } else if (vista === "correos-masivos") {
    cargarDatosCorreosMasivos();
  } else if (vista === "gestionar-correos") {
    cargarListaDestinatarios();
  } else if (vista === "trac-wiki") {
    cargarIndiceTracWiki();
  }
};

window.copiarComandoTexto = function(btn) {
  const codeBox = btn.closest('.cmd-box')?.querySelector('code');
  if (!codeBox) return;
  const text = codeBox.textContent.trim();
  navigator.clipboard.writeText(text).then(() => {
    const orig = btn.innerHTML;
    btn.innerHTML = "✅ ¡Copiado!";
    btn.style.background = "#10b981";
    btn.style.color = "#ffffff";
    if (typeof mostrarToast === "function") {
      mostrarToast("Comando copiado al portapapeles", "success");
    }
    setTimeout(() => {
      btn.innerHTML = orig;
      btn.style.background = "";
      btn.style.color = "";
    }, 2000);
  });
};

window.scrollAComando = function(secId) {
  const el = document.getElementById(secId);
  if (el) {
    el.scrollIntoView({ behavior: "smooth", block: "start" });
  }
};

window.filtrarComandos = function(query) {
  const q = query.toLowerCase().trim();
  document.querySelectorAll(".cmd-card-item").forEach(card => {
    const text = card.textContent.toLowerCase();
    if (!q || text.includes(q)) {
      card.style.display = "block";
    } else {
      card.style.display = "none";
    }
  });
};

function setupSidebarNavigation() {
  document.querySelectorAll(".sidebar-nav .nav-item:not(.external)").forEach(item => {
    item.addEventListener("click", (e) => {
      const btn = e.target.closest(".nav-item");
      if (!btn) return;
      const view = btn.getAttribute("data-view");
      const sub = btn.getAttribute("data-submodule");
      if (view) {
        window.navegarSeccionPortal(view, sub);
        // En móviles, cerrar sidebar al hacer clic
        if (window.innerWidth <= 768) {
          document.getElementById("portalSidebar")?.classList.remove("open");
        }
      }
    });
  });

  document.getElementById("btnToggleSidebar")?.addEventListener("click", () => {
    document.getElementById("portalSidebar")?.classList.toggle("open");
  });

  window.addEventListener("popstate", () => {
    restaurarVistaActivaPortal();
  });
}

function iniciarRelojSidebar() {
  const clockElem = document.getElementById("sidebarClock");
  if (!clockElem) return;
  const updateClock = () => {
    const now = new Date();
    const hrs = String(now.getHours()).padStart(2, '0');
    const min = String(now.getMinutes()).padStart(2, '0');
    const sec = String(now.getSeconds()).padStart(2, '0');
    clockElem.textContent = `${hrs}:${min}:${sec}`;
  };
  updateClock();
  setInterval(updateClock, 1000);
}

// --- 2. Bitácora / Pizarra de Turno (Autosave + Live Polling) ---
let debounceBitacoraTimer = null;
let isUserTypingBitacora = false;

async function cargarBitacora() {
  try {
    const res = await fetch("/api/bitacora");
    const data = await res.json();
    if (data.status === "ok") {
      if (!isUserTypingBitacora) {
        const dashT = document.getElementById("dashBitacoraTexto");
        const fullT = document.getElementById("fullBitacoraTexto");
        if (dashT && document.activeElement !== dashT) dashT.value = data.texto || "";
        if (fullT && document.activeElement !== fullT) fullT.value = data.texto || "";
      }
      actualizarStatusBitacora(`Sincronizado (${data.actualizado_en || 'Hoy'})`, false);
    }
  } catch (err) {
    console.error("Error al cargar bitacora:", err);
  }
}

async function guardarBitacora(texto) {
  actualizarStatusBitacora("Guardando...", true);
  try {
    const res = await fetch("/api/bitacora", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ texto })
    });
    const data = await res.json();
    if (data.status === "ok") {
      actualizarStatusBitacora(`Guardado (${data.actualizado_en})`, false);
    }
  } catch (err) {
    actualizarStatusBitacora("Error de conexión", true);
  }
}

function actualizarStatusBitacora(txt, isWarning) {
  const s1 = document.getElementById("dashBitacoraStatus");
  const s2 = document.getElementById("fullBitacoraStatus");
  [s1, s2].forEach(elem => {
    if (elem) {
      elem.innerHTML = `<span class="dot-indicator" style="background:${isWarning ? '#f59e0b' : '#10b981'};"></span> ${txt}`;
    }
  });
}

function setupBitacoraHandlers() {
  const dashT = document.getElementById("dashBitacoraTexto");
  const fullT = document.getElementById("fullBitacoraTexto");

  const onInput = (e) => {
    isUserTypingBitacora = true;
    const val = e.target.value;
    if (dashT && e.target !== dashT) dashT.value = val;
    if (fullT && e.target !== fullT) fullT.value = val;

    actualizarStatusBitacora("Escribiendo...", true);
    clearTimeout(debounceBitacoraTimer);
    debounceBitacoraTimer = setTimeout(() => {
      isUserTypingBitacora = false;
      guardarBitacora(val);
    }, 1000);
  };

  if (dashT) dashT.addEventListener("input", onInput);
  if (fullT) fullT.addEventListener("input", onInput);

  // Live polling cada 5 segundos
  setInterval(() => {
    if (!isUserTypingBitacora) {
      cargarBitacora();
    }
  }, 5000);

  document.getElementById("btnCopiarBitacora")?.addEventListener("click", async () => {
    const val = fullT?.value || dashT?.value || "";
    if (await copiarTextoAlPortapapeles(val)) {
      mostrarToast("Bitácora copiada al portapapeles", "success");
    }
  });
}

// --- 3. Correos Masivos Fin de Semana ---
function formatDateCorreos(dateStr) {
  if (!dateStr) return '--/--/----';
  const parts = dateStr.split('-');
  if (parts.length === 3) {
    return `${parts[2]}/${parts[1]}/${parts[0]}`;
  }
  return dateStr;
}

function getCargoCalculadoCorreos(nombre) {
  if (!nombre) return 'ASISTENTE DE SOPORTE';
  const n = String(nombre).toLowerCase();
  if (n.includes('hector') || n.includes('héctor') || n.includes('leonidas')) {
    return 'ASISTENTE DE SOPORTE SENIOR';
  } else if (n.includes('leonardo') || n.includes('gabriel') || n.includes('felipe') || n.includes('edwin')) {
    return 'ASISTENTE DE SOPORTE INTERMEDIO';
  } else if (n.includes('ivan') || n.includes('iván')) {
    return 'ASISTENTE DE SOPORTE';
  }
  return 'ASISTENTE DE SOPORTE';
}

function updatePreviewCorreoLive() {
  const select = document.getElementById('correoPersonalSelect');
  if (!select) return;
  const opt = select.options[select.selectedIndex];
  
  const fechaSab = document.getElementById('correoFechaSabado')?.value;
  const fechaDom = document.getElementById('correoFechaDomingo')?.value;

  const elSab = document.getElementById('pv-sabado');
  const elDom = document.getElementById('pv-domingo');
  if (elSab) elSab.textContent = formatDateCorreos(fechaSab);
  if (elDom) elDom.textContent = formatDateCorreos(fechaDom);

  if (opt && opt.value) {
    const nombre = opt.getAttribute('data-nombre') || opt.text;
    const telefono = opt.getAttribute('data-telefono') || '';
    const correo = 'soporte@innovex.cl';
    const cargo = getCargoCalculadoCorreos(nombre);

    const elNombre = document.getElementById('pv-nombre');
    const elTel = document.getElementById('pv-telefono');
    const elCorreo = document.getElementById('pv-correo');
    const elSigNombre = document.getElementById('pv-sig-nombre');
    const elSigCargo = document.getElementById('pv-sig-cargo');
    const elSigContacto = document.getElementById('pv-sig-contacto');

    if (elNombre) elNombre.textContent = nombre;
    if (elTel) elTel.textContent = telefono;
    if (elCorreo) elCorreo.textContent = correo;
    if (elSigNombre) elSigNombre.textContent = nombre;
    if (elSigCargo) elSigCargo.textContent = cargo;
    if (elSigContacto) elSigContacto.textContent = `📞 ${telefono} | ${correo}`;
  }
}

function setupCorreosMasivosHandlers() {
  document.getElementById("btnEnviarCorreosMasivos")?.addEventListener("click", () => {
    procesarEnvioPrevisualizacionCorreos(true);
  });

  document.getElementById("correoPersonalSelect")?.addEventListener("change", updatePreviewCorreoLive);
  document.getElementById("correoFechaSabado")?.addEventListener("change", updatePreviewCorreoLive);
  document.getElementById("correoFechaDomingo")?.addEventListener("change", updatePreviewCorreoLive);
}

async function cargarDatosCorreosMasivos() {
  try {
    const [resFechas, resAsist] = await Promise.all([
      fetch("/api/fechas_fin_semana").then(r => r.json()),
      fetch("/api/asistentes").then(r => r.json())
    ]);

    if (resFechas.status === "ok") {
      const semEl = document.getElementById("correoSemana");
      if (semEl) semEl.value = resFechas.semana;
    }

    const today = new Date();
    const dayOfWeek = today.getDay(); // 0 is Sunday, 6 is Saturday
    const nextSab = new Date(today);
    const distSab = (6 - dayOfWeek + 7) % 7;
    nextSab.setDate(today.getDate() + (distSab === 0 ? 0 : distSab));
    const nextDom = new Date(nextSab);
    nextDom.setDate(nextSab.getDate() + 1);

    const sabInput = document.getElementById("correoFechaSabado");
    const domInput = document.getElementById("correoFechaDomingo");
    if (sabInput && !sabInput.value) {
      sabInput.value = nextSab.toISOString().split("T")[0];
    }
    if (domInput && !domInput.value) {
      domInput.value = nextDom.toISOString().split("T")[0];
    }

    if (resAsist.status === "ok") {
      const select = document.getElementById("correoPersonalSelect");
      if (select) {
        select.innerHTML = '<option value="">Seleccione al asistente...</option>';
        resAsist.asistentes.forEach(a => {
          const opt = document.createElement("option");
          opt.value = a.id;
          opt.textContent = a.nombre;
          opt.setAttribute("data-nombre", a.nombre);
          opt.setAttribute("data-telefono", a.telefono || "");
          opt.setAttribute("data-correo", a.correo || "");
          opt.setAttribute("data-cargo", a.cargo || "");
          select.appendChild(opt);
        });
        if (select.options.length > 1 && !select.value) {
          select.selectedIndex = 1;
        }
      }
    }
    updatePreviewCorreoLive();
  } catch (err) {
    console.error("Error al cargar datos de correos masivos:", err);
  }
}

async function procesarEnvioPrevisualizacionCorreos(esEnvioReal) {
  const semana = document.getElementById("correoSemana")?.value;
  const personal_id = document.getElementById("correoPersonalSelect")?.value;
  const fecha_sabado = document.getElementById("correoFechaSabado")?.value || "";
  const fecha_domingo = document.getElementById("correoFechaDomingo")?.value || "";
  const correo_prueba = document.getElementById("correoPrueba")?.value || "";

  if (!personal_id) {
    mostrarToast("Debe seleccionar al personal de turno", "error");
    return;
  }
  if (!fecha_sabado || !fecha_domingo) {
    mostrarToast("Debe ingresar las fechas de sábado y domingo", "error");
    return;
  }

  const btn = document.getElementById("btnEnviarCorreosMasivos");
  const alertBox = document.getElementById("statusAlertCorreosMasivos");

  if (btn) {
    btn.disabled = true;
    btn.innerHTML = `⏳ Enviando correos masivos...`;
  }

  if (alertBox) {
    alertBox.className = "status-alert-banner info";
    alertBox.innerHTML = `<span>⏳ <strong>Procesando envío...</strong> Por favor espere mientras se despachan los correos masivos.</span>`;
  }

  try {
    const res = await fetch("/api/enviar_correos_masivos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        semana,
        personal_id,
        fecha_sabado,
        fecha_domingo,
        correo_prueba
      })
    });
    const data = await res.json();
    if (data.status === "ok") {
      mostrarToast(data.mensaje, "success");
      if (alertBox) {
        alertBox.className = "status-alert-banner success";
        alertBox.innerHTML = `<span>✅ <strong>¡Envío completado con éxito!</strong> ${data.mensaje}</span>`;
      }
    } else {
      mostrarToast(data.mensaje || "Error al enviar correo masivo", "error");
      if (alertBox) {
        alertBox.className = "status-alert-banner error";
        alertBox.innerHTML = `<span>❌ <strong>Error en el envío:</strong> ${data.mensaje || "Ocurrió una falla durante el envío."}</span>`;
      }
    }
  } catch (err) {
    mostrarToast("Error de conexión al procesar correo masivo", "error");
    if (alertBox) {
      alertBox.className = "status-alert-banner error";
      alertBox.innerHTML = `<span>❌ <strong>Error de conexión:</strong> No se pudo comunicar con el servidor para enviar los correos.</span>`;
    }
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = `✉️ Enviar Correos Masivos`;
    }
  }
}


// --- 4. Gestor de Destinatarios y Empresas ---
let listaDestinatariosCache = [];

function setupGestorDestinatariosHandlers() {
  document.getElementById("searchDestinatario")?.addEventListener("input", renderizarTablaDestinatarios);
  document.getElementById("filterEmpresaDestinatario")?.addEventListener("change", renderizarTablaDestinatarios);

  document.getElementById("btnAbrirModalNuevoDestinatario")?.addEventListener("click", () => {
    poblarEmpresasFiltroDestinatarios();
    const modal = document.getElementById("modalNuevoDestinatario");
    if (modal) modal.style.display = "flex";
  });

  document.getElementById("btnCerrarModalDestinatario")?.addEventListener("click", () => {
    const modal = document.getElementById("modalNuevoDestinatario");
    if (modal) modal.style.display = "none";
  });

  document.getElementById("btnGuardarNuevoDestinatario")?.addEventListener("click", async () => {
    const empresa = document.getElementById("nuevoDestEmpresa")?.value.trim();
    const correo = document.getElementById("nuevoDestCorreo")?.value.trim();
    if (!empresa || !correo) {
      mostrarToast("Complete la empresa y el correo", "warning");
      return;
    }

    try {
      const res = await fetch("/api/destinatarios", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "create", empresa, correo })
      });
      const data = await res.json();
      if (data.status === "ok") {
        document.getElementById("nuevoDestEmpresa").value = "";
        document.getElementById("nuevoDestCorreo").value = "";
        document.getElementById("modalNuevoDestinatario").style.display = "none";
        mostrarToast("Destinatario agregado correctamente", "success");
        cargarListaDestinatarios();
      }
    } catch (err) {
      mostrarToast("Error al guardar destinatario", "error");
    }
  });
}

async function cargarListaDestinatarios() {
  try {
    const res = await fetch("/api/destinatarios");
    const data = await res.json();
    if (data.status === "ok") {
      listaDestinatariosCache = data.destinatarios || [];
      poblarEmpresasFiltroDestinatarios();
      renderizarTablaDestinatarios();
    }
  } catch (err) {
    console.error("Error cargando destinatarios:", err);
  }
}

function poblarEmpresasFiltroDestinatarios() {
  const select = document.getElementById("filterEmpresaDestinatario");
  const datalist = document.getElementById("listEmpresasExistentes");
  const empresas = [...new Set(listaDestinatariosCache.map(d => d.empresa))].filter(Boolean).sort();

  if (select) {
    select.innerHTML = '<option value="">Todas las Empresas</option>';
    empresas.forEach(emp => {
      const opt = document.createElement("option");
      opt.value = emp;
      opt.textContent = emp;
      select.appendChild(opt);
    });
  }

  if (datalist) {
    datalist.innerHTML = "";
    empresas.forEach(emp => {
      const opt = document.createElement("option");
      opt.value = emp;
      datalist.appendChild(opt);
    });
  }
}

function renderizarTablaDestinatarios() {
  const tbody = document.getElementById("tablaDestinatariosBody");
  if (!tbody) return;

  const q = document.getElementById("searchDestinatario")?.value.toLowerCase().trim() || "";
  const filterEmp = document.getElementById("filterEmpresaDestinatario")?.value || "";

  const filtrados = listaDestinatariosCache.filter(d => {
    const matchQ = !q || (d.correo && d.correo.toLowerCase().includes(q)) || (d.empresa && d.empresa.toLowerCase().includes(q));
    const matchEmp = !filterEmp || d.empresa === filterEmp;
    return matchQ && matchEmp;
  });

  tbody.innerHTML = "";
  if (filtrados.length === 0) {
    tbody.innerHTML = '<tr><td colspan="4" style="text-align:center; color: var(--text-muted); padding: 20px;">No se encontraron destinatarios.</td></tr>';
    return;
  }

  filtrados.forEach(d => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><strong>${d.correo}</strong></td>
      <td><span class="badge" style="background: rgba(2,132,199,0.15); color: #38bdf8;">${d.empresa}</span></td>
      <td style="text-align: center;">
        <label class="switch">
          <input type="checkbox" ${d.activo ? 'checked' : ''} onchange="toggleDestinatarioActivo(${d.id}, this.checked)">
          <span class="slider"></span>
        </label>
      </td>
      <td style="text-align: right;">
        <button class="btn btn-danger btn-small" onclick="eliminarDestinatario(${d.id})">Eliminar</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

window.toggleDestinatarioActivo = async function(id, activo) {
  try {
    const res = await fetch("/api/destinatarios", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: "toggle_destinatario", id, activo })
    });
    const data = await res.json();
    if (data.status === "ok") {
      const item = listaDestinatariosCache.find(d => d.id === id);
      if (item) item.activo = activo;
      mostrarToast(`Destinatario ${activo ? 'activado' : 'desactivado'}`, "success");
    }
  } catch (err) {
    mostrarToast("Error al cambiar estado", "error");
  }
};

window.eliminarDestinatario = async function(id) {
  if (!confirm("¿Está seguro de eliminar este destinatario?")) return;
  try {
    const res = await fetch("/api/destinatarios", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: "delete_destinatario", id })
    });
    const data = await res.json();
    if (data.status === "ok") {
      listaDestinatariosCache = listaDestinatariosCache.filter(d => d.id !== id);
      renderizarTablaDestinatarios();
      mostrarToast("Destinatario eliminado", "success");
    }
  } catch (err) {
    mostrarToast("Error al eliminar", "error");
  }
};

// --- 5. Poseidón (Monitor Dual Multipantalla) ---
function setupPoseidon() {
  document.getElementById("btnLaunchPoseidon")?.addEventListener("click", () => {
    const width = Math.floor(window.screen.availWidth / 2);
    const height = window.screen.availHeight;

    // Ventana Izquierda (Llancacheo)
    window.open(
      "http://ce-llancacheo-inyeccion.acuimatic.com:8000/",
      "monitor_llancacheo",
      `width=${width},height=${height},left=0,top=0,location=no,toolbar=no,menubar=no`
    );

    // Ventana Derecha (Aulen)
    window.open(
      "http://ce-aulen-inyeccion.acuimatic.com:8000/",
      "monitor_aulen",
      `width=${width},height=${height},left=${width},top=0,location=no,toolbar=no,menubar=no`
    );

    mostrarToast("Monitores de inyección abiertos en modo dual", "success");
  });
}

// --- 6. Buscador & Índice Trac Wiki ---
async function cargarIndiceTracWiki() {
  try {
    const res = await fetch("/api/wiki/indice");
    const data = await res.json();
    if (data.status === "ok" && data.indice) {
      const container = document.getElementById("tracIndexContainer");
      if (!container) return;
      container.innerHTML = "";
      for (const [cat, items] of Object.entries(data.indice)) {
        const card = document.createElement("div");
        card.className = "trac-cat-card";
        let linksHtml = "";
        items.forEach(it => {
          linksHtml += `<a href="${it.url}" target="_blank" class="trac-link-item">📄 ${it.titulo}</a>`;
        });
        card.innerHTML = `<h4>📁 ${cat}</h4><div class="trac-link-list">${linksHtml}</div>`;
        container.appendChild(card);
      }
    }
  } catch (err) {
    console.error("Error al cargar indice wiki:", err);
  }
}

function setupTracSearch() {
  const input = document.getElementById("inputTracSearch");
  const resultsDiv = document.getElementById("tracSearchResults");
  let timeout;

  if (!input || !resultsDiv) return;

  input.addEventListener("input", () => {
    clearTimeout(timeout);
    const q = input.value.trim();
    if (q.length < 2) {
      resultsDiv.style.display = "none";
      return;
    }

    timeout = setTimeout(async () => {
      resultsDiv.style.display = "block";
      resultsDiv.innerHTML = '<p style="color: var(--text-muted);">Buscando en la Wiki...</p>';
      try {
        const res = await fetch(`/api/wiki/buscar?q=${encodeURIComponent(q)}`);
        const data = await res.json();
        if (data.results && data.results.length > 0) {
          let html = '<div style="display: flex; flex-direction: column; gap: 10px;">';
          data.results.forEach(r => {
            html += `
              <a href="${r.link}" target="_blank" style="padding: 12px; background: rgba(0,0,0,0.25); border: 1px solid var(--border-color); border-left: 4px solid var(--innovex-cyan); border-radius: 6px; text-decoration: none; color: inherit;">
                <h4 style="color: var(--innovex-cyan); margin-bottom: 4px;">${r.title}</h4>
                <p style="color: var(--text-muted); font-size: 12px; margin: 0;">${r.snippet}</p>
              </a>
            `;
          });
          html += '</div>';
          resultsDiv.innerHTML = html;
        } else {
          resultsDiv.innerHTML = `<p style="color: #f59e0b;">No se encontraron resultados para "${q}".</p>`;
        }
      } catch (err) {
        resultsDiv.innerHTML = '<p style="color: #ef4444;">Error al consultar la Wiki.</p>';
      }
    }, 400);
  });
}

// --- 7. Control Multimedia Host (Deshabilitado temporalmente) ---
function setupMusicPlayer() {
  // Deshabilitado temporalmente: no realiza llamadas fetch ni intervalos GET
}

// =========================================================
// --- 8. MÓDULO DE GENERACIÓN DE TICKETS DE FALLA ---
// =========================================================

const estadoTickets = {
  tipo: "conexion",
  centros: [],
  asistentes: [],
  zonas: [],
  imagenes: {
    conexion_evidencia: "",
    equipo_grafica: "",
    equipo_defectuoso: "",
    equipo_repuesto: "",
    sensor_repuesto: "",
    sensor_defectuoso: "",
    sensor_grafica: ""
  },
  previewTimer: null,
  pasteListenerAttached: false
};

window.inicializarModuloTicketsSoporte = async function() {
  await Promise.all([
    cargarCentrosTickets(),
    cargarAsistentesTickets(),
    cargarZonasTickets()
  ]);

  if (!estadoTickets.pasteListenerAttached) {
    setupPasteListenersTickets();
    estadoTickets.pasteListenerAttached = true;
  }

  actualizarPrevisualizacionTicketLive(true);
};

async function cargarCentrosTickets() {
  try {
    const res = await fetch("/api/tickets/centros");
    const data = await res.json();
    if (data.status === "ok" && data.centros) {
      estadoTickets.centros = data.centros;
      poblarSelectoresEmpresaYCentro();
    }
  } catch (err) {
    console.error("Error cargando centros de tickets:", err);
  }
}

async function cargarAsistentesTickets() {
  try {
    const res = await fetch("/api/asistentes");
    const data = await res.json();
    if (data.asistentes) {
      estadoTickets.asistentes = data.asistentes;
      const select = document.getElementById("ticketAsistenteSelect");
      if (select) {
        select.innerHTML = '<option value="">Seleccione Asistente de Soporte...</option>';
        data.asistentes.forEach(a => {
          const opt = document.createElement("option");
          opt.value = a.id;
          opt.textContent = `${a.nombre} (${a.cargo})`;
          select.appendChild(opt);
        });
        if (data.asistentes.length > 0) {
          select.selectedIndex = 1;
        }
      }
    }
  } catch (err) {
    console.error("Error cargando asistentes para tickets:", err);
  }
}

async function cargarZonasTickets() {
  try {
    const res = await fetch("/api/personal/estructura");
    const data = await res.json();
    if (data.status === "ok" && data.todas_las_zonas) {
      estadoTickets.zonas = data.todas_las_zonas;
      const select = document.getElementById("ticketZonaSelect");
      const modalSelect = document.getElementById("editCentroZonaSelect");
      
      const renderOptions = (sel) => {
        if (!sel) return;
        sel.innerHTML = '<option value="">Seleccione Zona...</option>';
        data.todas_las_zonas.forEach(z => {
          const opt = document.createElement("option");
          opt.value = z;
          opt.textContent = z;
          sel.appendChild(opt);
        });
      };
      
      renderOptions(select);
      renderOptions(modalSelect);
    }
  } catch (err) {
    console.error("Error cargando zonas para tickets:", err);
  }
}

function poblarSelectoresEmpresaYCentro() {
  const empSelect = document.getElementById("ticketEmpresaSelect");
  if (!empSelect) return;

  const empresasUnicas = [...new Set(estadoTickets.centros.map(c => c.empresa).filter(Boolean))].sort();
  empSelect.innerHTML = '<option value="">Seleccione Empresa...</option>';
  empresasUnicas.forEach(emp => {
    const opt = document.createElement("option");
    opt.value = emp;
    opt.textContent = emp;
    empSelect.appendChild(opt);
  });

  if (empresasUnicas.length > 0) {
    empSelect.value = empresasUnicas[0];
    alCambiarEmpresaTicket();
  }
}

window.alCambiarEmpresaTicket = function() {
  const emp = document.getElementById("ticketEmpresaSelect").value;
  const centroSelect = document.getElementById("ticketCentroSelect");
  if (!centroSelect) return;

  centroSelect.innerHTML = '<option value="">Seleccione Centro...</option>';
  const centrosFiltrados = estadoTickets.centros.filter(c => c.empresa === emp);
  centrosFiltrados.forEach(c => {
    const opt = document.createElement("option");
    opt.value = c.nombre_centro;
    opt.textContent = c.nombre_centro + (c.codigo_location ? ` (${c.codigo_location})` : "");
    opt.dataset.id = c.id;
    centroSelect.appendChild(opt);
  });

  if (centrosFiltrados.length > 0) {
    centroSelect.selectedIndex = 1;
    alCambiarCentroTicket();
  } else {
    actualizarPrevisualizacionTicketLive();
  }
};

window.alCambiarCentroTicket = function() {
  const emp = document.getElementById("ticketEmpresaSelect").value;
  const centroNombre = document.getElementById("ticketCentroSelect").value;
  const centroObj = estadoTickets.centros.find(c => c.empresa === emp && c.nombre_centro === centroNombre);

  if (centroObj) {
    const inputTo = document.getElementById("ticketDestinatariosTo");
    const inputCc = document.getElementById("ticketDestinatariosCc");
    const selectZona = document.getElementById("ticketZonaSelect");

    if (inputTo) inputTo.value = centroObj.destinatarios_to || "";
    if (inputCc) inputCc.value = centroObj.destinatarios_cc || "";
    if (selectZona && centroObj.zona) selectZona.value = centroObj.zona;
  }

  actualizarPrevisualizacionTicketLive();
};

window.cambiarTipoTicket = function(tipo) {
  estadoTickets.tipo = tipo;

  // Actualizar botones pills
  document.querySelectorAll("#ticketTypePills .ticket-pill").forEach(pill => {
    if (pill.getAttribute("data-type") === tipo) {
      pill.classList.add("active");
    } else {
      pill.classList.remove("active");
    }
  });

  // Alternar formularios
  const cConexion = document.getElementById("ticketCamposConexion");
  const cEquipo = document.getElementById("ticketCamposEquipo");
  const cSensor = document.getElementById("ticketCamposSensor");
  const badge = document.getElementById("ticketPreviewBadge");

  if (cConexion) cConexion.style.display = tipo === "conexion" ? "block" : "none";
  if (cEquipo) cEquipo.style.display = tipo === "falla_equipo" ? "block" : "none";
  if (cSensor) cSensor.style.display = tipo === "falla_sensor" ? "block" : "none";

  const opcionGuia = document.getElementById("ticketOpcionAdjuntarGuia");
  if (opcionGuia) {
    opcionGuia.style.display = tipo === "conexion" ? "none" : "flex";
  }

  if (badge) {
    const titulos = {
      conexion: "Conexión",
      falla_equipo: "Falla de Equipo",
      falla_sensor: "Falla de Sensor"
    };
    badge.textContent = titulos[tipo] || tipo;
  }

  actualizarPrevisualizacionTicketLive(true);
};

window.triggerFileInput = function(inputId) {
  const elem = document.getElementById(inputId);
  if (elem) elem.click();
};

/**
 * Redimensiona una imagen base64 a un tamaño máximo manteniendo proporción.
 * Comprime como JPEG al 80% para mantener el payload ligero en preview.
 */
function redimensionarImagenBase64(dataUrl, maxDim = 800, quality = 0.80) {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = function() {
      let w = img.width, h = img.height;
      if (w > maxDim || h > maxDim) {
        if (w > h) { h = Math.round(h * maxDim / w); w = maxDim; }
        else { w = Math.round(w * maxDim / h); h = maxDim; }
      }
      const canvas = document.createElement("canvas");
      canvas.width = w;
      canvas.height = h;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(img, 0, 0, w, h);
      resolve(canvas.toDataURL("image/jpeg", quality));
    };
    img.onerror = function() { resolve(dataUrl); };
    img.src = dataUrl;
  });
}

window.alSeleccionarImagenTicket = function(event, key) {
  const file = event.target.files && event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = async function(e) {
    const resized = await redimensionarImagenBase64(e.target.result);
    estadoTickets.imagenes[key] = resized;
    mostrarPreviewDropzone(key, resized);
    actualizarPrevisualizacionTicketLive(true);
  };
  reader.readAsDataURL(file);
};

window.removerImagenTicket = function(event, key) {
  if (event) event.stopPropagation();
  estadoTickets.imagenes[key] = "";
  ocultarPreviewDropzone(key);
  actualizarPrevisualizacionTicketLive(true);
};

function mostrarPreviewDropzone(key, dataUrl) {
  const kHyphen = key.replace(/_/g, "-");
  const prompt = document.getElementById(`dz-prompt-${kHyphen}`);
  const preview = document.getElementById(`dz-preview-${kHyphen}`);
  const img = document.getElementById(`img-preview-${kHyphen}`);

  if (prompt) prompt.style.display = "none";
  if (preview) preview.style.display = "flex";
  if (img) img.src = dataUrl;
}

function ocultarPreviewDropzone(key) {
  const kHyphen = key.replace(/_/g, "-");
  const prompt = document.getElementById(`dz-prompt-${kHyphen}`);
  const preview = document.getElementById(`dz-preview-${kHyphen}`);
  const img = document.getElementById(`img-preview-${kHyphen}`);
  const fileInput = document.getElementById(`file-${kHyphen}`);

  if (prompt) prompt.style.display = "block";
  if (preview) preview.style.display = "none";
  if (img) img.src = "";
  if (fileInput) fileInput.value = "";
}

function setupPasteListenersTickets() {
  document.addEventListener("paste", function(e) {
    // Solo interceptar si estamos en la vista de tickets
    const viewTickets = document.getElementById("view-tickets-soporte");
    if (!viewTickets || viewTickets.style.display === "none") return;

    // Si el usuario está escribiendo en un input o textarea normal, no bloquear texto
    const target = e.target;
    if (target && (target.tagName === "INPUT" || target.tagName === "TEXTAREA") && target.type !== "file") {
      // Permitir pegar texto en inputs
      if (!e.clipboardData.files.length) return;
    }

    const items = e.clipboardData && e.clipboardData.items;
    if (!items) return;

    for (let i = 0; i < items.length; i++) {
      if (items[i].type.indexOf("image") !== -1) {
        const blob = items[i].getAsFile();
        const reader = new FileReader();
        reader.onload = async function(event) {
          const b64 = await redimensionarImagenBase64(event.target.result);
          asignarImagenPegadaSegunTipo(b64);
        };
        reader.readAsDataURL(blob);
        e.preventDefault();
        break;
      }
    }
  });

  // Drag & drop highlight
  document.querySelectorAll(".ticket-dropzone").forEach(dz => {
    dz.addEventListener("dragover", e => { e.preventDefault(); dz.classList.add("dragover"); });
    dz.addEventListener("dragleave", e => { e.preventDefault(); dz.classList.remove("dragover"); });
    dz.addEventListener("drop", e => {
      e.preventDefault();
      dz.classList.remove("dragover");
      if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        const file = e.dataTransfer.files[0];
        if (file.type.startsWith("image/")) {
          const dzId = dz.id.replace("dz-", "").replace(/-/g, "_");
          const reader = new FileReader();
          reader.onload = async (ev) => {
            const resized = await redimensionarImagenBase64(ev.target.result);
            estadoTickets.imagenes[dzId] = resized;
            mostrarPreviewDropzone(dzId, resized);
            actualizarPrevisualizacionTicketLive(true);
          };
          reader.readAsDataURL(file);
        }
      }
    });
  });
}

function asignarImagenPegadaSegunTipo(b64) {
  const tipo = estadoTickets.tipo;
  let targetKey = "";

  if (tipo === "conexion") {
    targetKey = "conexion_evidencia";
  } else if (tipo === "falla_equipo") {
    if (!estadoTickets.imagenes.equipo_grafica) targetKey = "equipo_grafica";
    else if (!estadoTickets.imagenes.equipo_defectuoso) targetKey = "equipo_defectuoso";
    else targetKey = "equipo_repuesto";
  } else if (tipo === "falla_sensor") {
    if (!estadoTickets.imagenes.sensor_repuesto) targetKey = "sensor_repuesto";
    else if (!estadoTickets.imagenes.sensor_defectuoso) targetKey = "sensor_defectuoso";
    else targetKey = "sensor_grafica";
  }

  if (targetKey) {
    estadoTickets.imagenes[targetKey] = b64;
    mostrarPreviewDropzone(targetKey, b64);
    actualizarPrevisualizacionTicketLive(true);
  }
}

window.actualizarPrevisualizacionTicketLive = function(forzar = false) {
  clearTimeout(estadoTickets.previewTimer);

  const delay = forzar ? 0 : 300;
  estadoTickets.previewTimer = setTimeout(async () => {
    const payload = recolectarDatosTicket();

    try {
      const res = await fetch("/api/tickets/previsualizar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          tipo_ticket: estadoTickets.tipo,
          datos: payload
        })
      });
      const data = await res.json();
      if (data.status === "ok") {
        const subjectElem = document.getElementById("ticketPreviewSubjectText");
        const htmlContainer = document.getElementById("ticketPreviewHtmlContainer");
        if (subjectElem) subjectElem.textContent = data.asunto;
        if (htmlContainer) htmlContainer.innerHTML = data.html;
      }
    } catch (err) {
      console.error("Error en previsualización de ticket:", err);
    }
  }, delay);
};

function recolectarDatosTicket() {
  const emp = document.getElementById("ticketEmpresaSelect")?.value || "";
  const centro = document.getElementById("ticketCentroSelect")?.value || "Centro";
  const personalId = document.getElementById("ticketAsistenteSelect")?.value || "";
  const tipo = estadoTickets.tipo;

  const payload = {
    empresa: emp,
    nombre_centro: centro,
    personal_id: personalId,
    imagen_evidencia: estadoTickets.imagenes.conexion_evidencia,
    imagen_grafica: estadoTickets.imagenes.equipo_grafica || estadoTickets.imagenes.sensor_grafica,
    imagen_defectuoso: estadoTickets.imagenes.equipo_defectuoso || estadoTickets.imagenes.sensor_defectuoso,
    imagen_repuesto: estadoTickets.imagenes.equipo_repuesto || estadoTickets.imagenes.sensor_repuesto,
  };

  if (tipo === "falla_equipo") {
    payload.numero_equipo = document.getElementById("ticketEquipoNumero")?.value || "";
    payload.ubicacion = document.getElementById("ticketEquipoUbicacion")?.value || "";
    payload.identificador_repuesto = document.getElementById("ticketEquipoRepuestoId")?.value || "Name A1";
    payload.texto_referencia = document.getElementById("ticketEquipoReferencia")?.value || "";
  } else if (tipo === "falla_sensor") {
    payload.tipo_sensor = document.getElementById("ticketSensorTipo")?.value || "oxígeno";
    payload.profundidad = document.getElementById("ticketSensorProfundidad")?.value || "10";
    payload.numero_jaula = document.getElementById("ticketSensorJaula")?.value || "105";
  }

  return payload;
}

window.ejecutarEnvioTicket = async function() {
  const btn = document.getElementById("btnEnviarTicket");
  const destTo = document.getElementById("ticketDestinatariosTo")?.value || "";
  const destCc = document.getElementById("ticketDestinatariosCc")?.value || "";
  const correoPrueba = document.getElementById("ticketCorreoPrueba")?.value || "";
  const adjuntarGuia = document.getElementById("ticketAdjuntarGuia")?.checked ?? true;
  const personalId = document.getElementById("ticketAsistenteSelect")?.value || "";

  if (!correoPrueba && !destTo) {
    alert("Por favor ingrese los correos destinatarios o un correo de prueba.");
    return;
  }

  const payload = recolectarDatosTicket();

  if (btn) {
    btn.disabled = true;
    btn.innerHTML = '⏳ Enviando ticket...';
  }

  try {
    const res = await fetch("/api/tickets/enviar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        tipo_ticket: estadoTickets.tipo,
        datos: payload,
        personal_id: personalId,
        destinatarios_to: destTo,
        destinatarios_cc: destCc,
        correo_prueba: correoPrueba,
        adjuntar_guia: adjuntarGuia
      })
    });
    const data = await res.json();
    if (data.status === "ok") {
      alert("✅ " + data.mensaje);
      cargarHistorialTickets();
    } else {
      alert("❌ Error: " + (data.mensaje || "No se pudo enviar el ticket"));
    }
  } catch (err) {
    alert("❌ Error de red al enviar el ticket: " + err.message);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
        Enviar Ticket de Falla
      `;
    }
  }
};

window.toggleVistaHistorialTickets = function() {
  const panelPv = document.getElementById("panelVistaPreviaTicket");
  const panelHist = document.getElementById("panelHistorialTickets");
  const btn = document.getElementById("btnToggleHistorialTickets");

  if (!panelHist || !panelPv) return;

  if (panelHist.style.display === "none") {
    panelHist.style.display = "block";
    panelPv.style.display = "none";
    if (btn) btn.innerHTML = '<span>👁️</span> Ver Vista Previa';
    cargarHistorialTickets();
  } else {
    panelHist.style.display = "none";
    panelPv.style.display = "block";
    if (btn) btn.innerHTML = '<span>📜</span> Historial de Envíos';
  }
};

window.cargarHistorialTickets = async function() {
  const container = document.getElementById("ticketHistorialListContainer");
  if (!container) return;

  container.innerHTML = '<div style="text-align: center; color: var(--text-muted); padding: 1rem;">Cargando...</div>';

  try {
    const res = await fetch("/api/tickets/historial");
    const data = await res.json();
    if (data.status === "ok" && data.historial && data.historial.length > 0) {
      let html = `
        <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem;">
          <thead>
            <tr style="background: var(--bg-surface-elevated, #f1f5f9); text-align: left;">
              <th style="padding: 6px 8px;">Fecha</th>
              <th style="padding: 6px 8px;">Tipo</th>
              <th style="padding: 6px 8px;">Centro</th>
              <th style="padding: 6px 8px;">Destinatarios</th>
              <th style="padding: 6px 8px;">Emisor</th>
            </tr>
          </thead>
          <tbody>
      `;
      data.historial.forEach(h => {
        const modoTag = h.es_prueba ? '<span style="color: #f59e0b; font-weight: bold;">[PRUEBA]</span> ' : '';
        html += `
          <tr style="border-bottom: 1px solid var(--border-color, #e2e8f0);">
            <td style="padding: 6px 8px; color: var(--text-muted);">${h.fecha_envio}</td>
            <td style="padding: 6px 8px; font-weight: 600;">${h.tipo_display}</td>
            <td style="padding: 6px 8px;">${h.empresa} - ${h.centro}</td>
            <td style="padding: 6px 8px;">${modoTag}${h.destinatarios_to}</td>
            <td style="padding: 6px 8px;">${h.asistente}</td>
          </tr>
        `;
      });
      html += '</tbody></table>';
      container.innerHTML = html;
    } else {
      container.innerHTML = '<div style="text-align: center; color: var(--text-muted); padding: 1.5rem;">No hay tickets registrados en el historial todavía.</div>';
    }
  } catch (err) {
    container.innerHTML = '<div style="color: #ef4444; text-align: center; padding: 1rem;">Error cargando historial.</div>';
  }
};

// Modal Directorio de Centros
window.abrirModalGestionCentrosTickets = function() {
  const modal = document.getElementById("modalGestionCentrosTickets");
  if (modal) {
    modal.style.display = "flex";
    cargarTablaCentrosContactos();
  }
};

window.cerrarModalGestionCentrosTickets = function() {
  const modal = document.getElementById("modalGestionCentrosTickets");
  if (modal) modal.style.display = "none";
};

window.cargarTablaCentrosContactos = function() {
  const tbody = document.getElementById("tbodyCentrosContactos");
  if (!tbody) return;

  if (estadoTickets.centros.length === 0) {
    tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 12px; color: var(--text-muted);">No hay centros registrados.</td></tr>';
    return;
  }

  let html = "";
  estadoTickets.centros.forEach(c => {
    html += `
      <tr style="border-bottom: 1px solid var(--border-color, #e2e8f0);">
        <td style="padding: 8px 12px; font-weight: 600;">${c.empresa}</td>
        <td style="padding: 8px 12px;">${c.nombre_centro}</td>
        <td style="padding: 8px 12px; color: var(--text-muted);">${c.zona || "-"}</td>
        <td style="padding: 8px 12px; font-size: 0.78rem; max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${c.destinatarios_to || "-"}</td>
        <td style="padding: 8px 12px; text-align: center; white-space: nowrap;">
          <button class="btn btn-secondary btn-sm" onclick="editarCentroContacto(${c.id})" style="padding: 2px 6px; font-size: 0.75rem;">✏️</button>
          <button class="btn btn-secondary btn-sm" onclick="eliminarCentroContacto(${c.id})" style="padding: 2px 6px; font-size: 0.75rem; color: #ef4444;">🗑️</button>
        </td>
      </tr>
    `;
  });
  tbody.innerHTML = html;
};

window.limpiarFormCentroContacto = function() {
  document.getElementById("editCentroId").value = "";
  document.getElementById("editCentroEmpresa").value = "";
  document.getElementById("editCentroNombre").value = "";
  document.getElementById("editCentroLocation").value = "";
  document.getElementById("editCentroZonaSelect").value = "";
  document.getElementById("editCentroDestinatariosTo").value = "";
  document.getElementById("editCentroDestinatariosCc").value = "";
  document.getElementById("btnGuardarCentroContacto").textContent = "Guardar Centro";
};

window.editarCentroContacto = function(id) {
  const c = estadoTickets.centros.find(item => item.id === id);
  if (!c) return;

  document.getElementById("editCentroId").value = c.id;
  document.getElementById("editCentroEmpresa").value = c.empresa;
  document.getElementById("editCentroNombre").value = c.nombre_centro;
  document.getElementById("editCentroLocation").value = c.codigo_location || "";
  document.getElementById("editCentroZonaSelect").value = c.zona || "";
  document.getElementById("editCentroDestinatariosTo").value = c.destinatarios_to || "";
  document.getElementById("editCentroDestinatariosCc").value = c.destinatarios_cc || "";
  document.getElementById("btnGuardarCentroContacto").textContent = "Actualizar Centro";
};

window.guardarCentroContactoDesdeModal = async function() {
  const cid = document.getElementById("editCentroId").value;
  const empresa = document.getElementById("editCentroEmpresa").value;
  const nombreCentro = document.getElementById("editCentroNombre").value;
  const codigoLocation = document.getElementById("editCentroLocation").value;
  const zonaNombre = document.getElementById("editCentroZonaSelect").value;
  const destTo = document.getElementById("editCentroDestinatariosTo").value;
  const destCc = document.getElementById("editCentroDestinatariosCc").value;

  try {
    const res = await fetch("/api/tickets/centros", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id: cid ? parseInt(cid) : undefined,
        empresa: empresa,
        nombre_centro: nombreCentro,
        codigo_location: codigoLocation,
        destinatarios_to: destTo,
        destinatarios_cc: destCc,
      })
    });
    const data = await res.json();
    if (data.status === "ok") {
      limpiarFormCentroContacto();
      await cargarCentrosTickets();
      cargarTablaCentrosContactos();
    } else {
      alert("Error: " + (data.mensaje || "No se pudo guardar"));
    }
  } catch (err) {
    alert("Error al guardar centro: " + err.message);
  }
};

window.eliminarCentroContacto = async function(id) {
  if (!confirm("¿Está seguro de eliminar este centro del directorio?")) return;

  try {
    const res = await fetch("/api/tickets/centros", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: "delete", id: id })
    });
    const data = await res.json();
    if (data.status === "ok") {
      await cargarCentrosTickets();
      cargarTablaCentrosContactos();
    }
  } catch (err) {
    alert("Error al eliminar centro: " + err.message);
  }
};


