# 🏗 RESUMEN MAESTRO — PROYECTO SANTA ISABEL DOS QUEBRADAS
## CVA Constructora SAS | Dosquebradas, Risaralda | V5.1 | Jun-2026

---

## 📌 DATOS GENERALES DEL PROYECTO

| Campo | Dato |
|---|---|
| **Proyecto** | Santa Isabel Dos Quebradas — Conjunto Residencial VIS / NO VIS |
| **Ubicación** | Diagonal 26 Transversal 9, Sector Santa Isabel, Dosquebradas |
| **Empresa** | CVA Constructora SAS |
| **Normativa** | NSR-10 · RAS 2000 · NTC 1500 · RETIE · RETTIG NTC 3631 · Decreto 1079 · Ley 1796/2016 |
| **Inicio obras** | 01/05/2026 |
| **Fin obra** | 31/10/2027 (18 meses) |
| **Fin postventa** | 29/01/2028 (21 meses total) |

---

## 🏢 UNIDADES DEL PROYECTO

| Estructura | Cantidad | Tipo | Sistema |
|---|---|---|---|
| **Torre** | 12 pisos | 89 apartamentos (VIS + NO VIS) + ascensor SCALA KL-K001 | Muros concreto reforzado |
| **Casas VIS** | 5 unidades | 2 niveles + terraza | Muros concreto f'c=21 MPa |
| **Parqueadero** | 67 cupos | 53 autos (41 ext + 12 int) + 14 motos (11 ext + 3 int) | Pórticos concreto + est. metálica |
| **Locales comerciales** | 9 unidades | Piso 1 torre | Sistema Durapanel GRC |
| **Depósitos** | 11 unidades | — | — |

---

## ⚙️ ESPECIFICACIONES TÉCNICAS CLAVE (del documento oficial)

### ESTRUCTURA TORRE
- **Cimentación**: Pilotes (147 Ø40cm L=8.5m) + vigas corridas + placa maciza
- **Muros**: Concreto reforzado (sistema FORSA/UNISPAN) · f'c columnas 28 MPa · f'c vigas 24.5 MPa · f'c resto 21 MPa
- **Cubierta**: Losa en concreto impermeabilizado + geotextil + geomembrana PVC termofusionada (garantía 10 años)
- **Paneles solares**: En aptos 905, 1201, 1202, 1207, 1208
- **Cubierta panel metálico**: Aptos 1203 y 1204 (sándwich poliuretano + galv. Aluzinc)

### ESPECIFICACIONES ACABADOS (según documento oficial)

| Zona | Aptos VIS (acabado básico) | Aptos NO VIS |
|---|---|---|
| **Pisos sala/alcobas/cocina** | Concreto a la vista (vaciado estructura, sin zócalo) | Porcelánico Esmaltado Mate Cement Antracita 60×120cm |
| **Pisos baño** | Cerámica nacional | Porcelánico Concrete Gris 75×75cm |
| **Muros baño** | Cerámica ducha 1.80m + lavamanos 20cm | Cubik Multicolor 19.8×19.8 a 1.80m (todo el baño) |
| **Cocina/zona ropas** | Concreto a la vista + salpicadero mín. 40cm | Artisan Azul 31.6×60cm + salpicadero mín. 40cm |
| **Terraza** | — | Deck WPC (Wood Plastic Composite) |
| **Cielos** | Concreto a la vista | Concreto a la vista |
| **Muros internos** | Concreto reforzado a la vista (acabado formaleta + resanes) | Ídem |
| **Fachada principal** | Muros concreto + argamasa + revestimiento plástico (graniplast) | Ídem |

### CASAS VIS — ESPECIFICACIONES CONFIRMADAS
- **Pisos sala/alcobas**: Concreto a la vista SIN enchape, SIN pulir, SIN pintura
- **Salpicadero cocina**: mín. 40cm (⚠️ corrección: documentos anteriores decían 30cm)
- **Lavadero**: Base en concreto (⚠️ corrección: no fibra de vidrio)
- **Cocina**: Integral Amalfi 1.50m + mesón acero inoxidable + lavaplatos
- **Gas**: Tubería PE-AL-PE Ø1/2" (RETTIG NTC 3631)
- **Muros**: Concreto a la vista sin pañete
- **Cubierta**: Losa e=10cm impermeabilizada a la vista (terraza sin remate)

### INSTALACIONES (todas las unidades)
- **Gas**: PE-AL-PE Ø1/2" · Prueba neumática 1.5 kg/cm² · Certificación RETTIG
- **Eléctrico**: Tablero 8 circuitos monofásico por unidad · RETIE · Generador emergencia zonas comunes
- **TV**: 4 puntos por apto (sala + cada alcoba) · 2 puntos casas (sala + alcoba ppal)
- **Teléfono/Coaxial**: 2 puntos tipo A y B (sala + alcoba principal)
- **Tanque**: Sistema bombeo centralizado + reserva contra incendio
- **Ascensor**: SCALA KL-K001 · Acero inoxidable · Fondo panorámico
- **Red CI**: Gabinetes por piso · NFPA 13

---

## 📅 CRONOGRAMA MAESTRO — LÓGICA DE INICIO ENCADENADO

```
MAYO 2026        OCT 2026       NOV 2026       DIC 2026       ENE 2027       MAR 2027
    │                │              │              │              │              │
    ▼                ▼              ▼              ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ 🏗 TORRE 12 PISOS                                                                   │
│ F0-F2 Gestión+Preobra │ F3 Cimentación │ F4 P1-4 │ F5 P5-8 │ F6 P9-12 │ F7-F27... │
└─────────────────────────────────────────────────────────────────────────────────────┘
                         │
                         ▼ Jun/2026 PARALELO
┌──────────────────────────────────┐
│ 💧 TANQUE 90,000L (2×45,000L)   │
│ F22D: 25/06 → 27/08/2026        │
└──────────────────────────────────┘
                              │
                              ▼ Fin Piso 4 = 26/10/2026
┌──────────────────────────────────────────────┐
│ 🏠 CASAS VIS (5 und)                         │
│ F21: 15/10/2026 → 15/02/2027 (85 días)      │
└──────────────────────────────────────────────┘
                                   │
                                   ▼ Fin F5 Torre (Pisos 5-8) = 23/11/2026
┌──────────────────────────────────────────────────────────┐
│ 🚗 PARQUEADERO (67 cupos + Zona Social)                  │
│ F20: 23/11/2026 → 14/09/2027 (82 días)                  │
└──────────────────────────────────────────────────────────┘
                                        │
                                        ▼ Piso 10 Torre = 14/12/2026
┌──────────────────────────────────────────────────────────────────┐
│ 🏪 LOCALES COMERCIALES (9 und — Durapanel)                       │
│ F23: 14/12/2026 → 24/05/2027 (56 días)                          │
└──────────────────────────────────────────────────────────────────┘
                                               │
                                               ▼ Torre F6 completada = 20/01/2027
┌──────────────────────────────────────────────────────────────────────────┐
│ 🌆 URBANISMO INTEGRAL (paralelo, 3 secciones)                            │
│ 🔵 Redes Húmedas F22A: 20/01 → 06/03/2027                               │
│ 🟣 Redes Secas F22B: 20/01 → 12/03/2027 (Transf. 112.5 KVA)            │
│ 🟢 Urbanismo F22G: 20/01 → 30/03/2027 (cerramiento+andenes+zonas verdes) │
│ 🛣 Vía MDC-19 F22C: 15/03 → 03/05/2027 (1,200 m² pavimento flexible)   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 ARCHIVOS GENERADOS (en 05_PROGRAMACION y outputs)

| Archivo | Contenido | Estado |
|---|---|---|
| `Programacion_Obra_SANTAISABEL_Profesional-TORRE.xlsx` | Programación maestra integrada V4.0 · 8 hojas | ✅ Guardado |
| `Programacion_Obra_OHANA_Profesional.xlsx` | V5.0 con Urbanismo+Redes+Tanque+Locales completo | ✅ Guardado |
| `Programacion_Obra_OHANA_Profesional_V5.1.xlsx` | Proceso detallado Casas+Locales (83+46 act.) + Gantt secuencial | ✅ Guardado |
| `PROCESO_TANQUE_AGUA_POTABLE.xlsx` | 55 actividades · f'c=4000 PSI · Cinta PVC Ø22 · 3 vaciados | ✅ Guardado |
| `URBANISMO_INTEGRAL_SANTA_ISABEL.xlsx` | Una hoja con 3 secciones (🔵RH+🟣RS+🟢URB) diferenciadas por color | ✅ Guardado |
| `CASAS_VIS_PROCESO_DETALLADO_COMPLETO.xlsx` | 78 actividades · 5 subfases · mismo formato Torre | ✅ Guardado |
| `MEMORIA_CANTIDADES_PARQUEADERO_SANTA_ISABEL_v2.xlsx` | 7 hojas · 258 fórmulas · cantidades exactas de Memorias | ✅ Guardado |
| `PROGRAMACION_PARQUEADERO_V2_SANTA_ISABEL.xlsx` | 95 actividades · cantidades de Memoria propia | ✅ Guardado |
| `PROGRAMACION_CASAS_SANTA_ISABEL.xlsx` | Programación casas anterior | ✅ Guardado |
| `PROGRAMACION_PARQUEADERO_SANTA_ISABEL.xlsx` | Programación parqueadero anterior | ✅ Guardado |

---

## 🔢 CANTIDADES CLAVE VERIFICADAS

### PARQUEADERO (de Memoria v2 — ETABS Anexo 1-2-3 + Planos)
| Elemento | Concreto | Acero |
|---|---|---|
| Pantallas sótano e=15-20cm | 19.452 m³ | 3,779 kg malla fy=490MPa |
| Zapatas Z1-Z8 (21 und) f'c=21MPa | 29.811 m³ | 1,144 kg #4 |
| VC-1 0.35×0.35m (9 ejes) f'c=21MPa | 9.813 m³ | 109.63 kg |
| Columnas C35×35 f'c=28MPa (41 cols) | 13.534 m³ | 2,317 kg |
| Vigas aéreas f'c=24.5MPa | 24.003 m³ | 3,250 kg |
| Placas Corpalosa T2 Cal.22 e=11cm | 73.444 m³ | 9,806 kg |
| Escaleras f'c=21MPa | 2.612 m³ | 205 kg |
| **Estructura metálica cubierta** | — | **6,317 kg (6.32 ton)** |
| **TOTAL** | **172.67 m³** | **26,930 kg + 6,317 kg met.** |

### TANQUE DE AGUA POTABLE
- 2 tanques × 45,000 L = **90,000 L total**
- f'c = **4,000 PSI (28 MPa)** + aditivo impermeabilizante integral
- Cinta PVC Ø22 en junta losa-muro
- **3 vaciados**: ① Losa fondo e=20cm + arranque 15cm → ② Muros h=2.30m → ③ Tapa e=15cm
- Impermeabilización interior: Penetron/Xypex por cristalización
- Prueba hidráulica: **48 horas** (caída ≤1cm)
- Desinfección: hipoclorito NaOCl 50 ppm 12h (NTC 813)

### VÍA INTERNA 1,200 m²
- Subbase b-600 e=20cm: **240 m³**
- Base b-400 e=15cm: **180 m³**
- Carpeta MDC-19 e=5cm: **135 ton** (densidad 2.25 t/m³)
- Bordillos: ~180 ml sardinel prefab.

### TANQUE RESERVA NSR/RAS 2000
- 89 aptos × 3 personas × 150 L/día × 2 días = 80,100 L + zonas comunes = **~90,000 L**
- Transformador: 89a×1.2kW + 9loc×3kW + parq.+común = 154 kW → Fd=0.8 → 123 kW → **112.5 KVA pad-mounted**

---

## ⚠️ CORRECCIONES DETECTADAS (especificaciones vs. programaciones)

| # | Error detectado | Corrección |
|---|---|---|
| 1 | Salpicadero cocina: programaciones decían 30cm | **Documento oficial: mín. 40cm** |
| 2 | Lavadero casas: programaciones decían fibra de vidrio | **Documento oficial: base en concreto** |
| 3 | Tanque: versión anterior era HDPE prefabricado | **Corregido: concreto f'c=4000 PSI impermeabilizado** |
| 4 | Resumen PARQUEADERO tenía referencias cruzadas incorrectas | **Corregido en v2 (258 fórmulas OK)** |
| 5 | Muros casas e=12cm | **Especificación confirma e=10cm** |
| 6 | Inicio casas: 26/10/2026 en algunos archivos | **Inicio correcto: 15/10/2026** |

---

## 📐 METODOLOGÍA DE PROGRAMACIÓN UTILIZADA

1. **CPM (Critical Path Method)** — Encadenamiento de predecesores y cálculo de fechas
2. **Last Planner System** — Condiciones de inicio verificadas antes de autorizar cada actividad (hitos de interventoría obligatorios)
3. **PMBOK 7** — Estructura de fases, WBS, gestión de riesgos, hitos de control
4. **NSR-10 como base técnica** — Tiempos mínimos inamovibles: curado 4-7 días, puntales 21 días (ACI 347), prueba gas 24h (RETTIG), prueba hidráulica 2h
5. **Rendimientos SENA/CAMACOL** — Duraciones basadas en rendimientos típicos obra VIS Colombia
6. **Paralelismo estratégico** — 4 frentes simultáneos desde oct/2026: Torre + Casas + Parqueadero + Locales + Urbanismo (ene/2027)

---

## 🔄 PENDIENTE / POR MEJORAR

- [ ] Incorporar correcciones de especificaciones (salpicadero 40cm, lavadero concreto) en el archivo maestro CASAS
- [ ] Revisar acabados aptos NO VIS en programación Torre (porcelánico 60×120, Cubik baños, Artisan cocina, deck terraza)
- [ ] Agregar actividad: Planta eléctrica emergencia (generador zonas comunes + ascensores)
- [ ] Agregar: Ducto de basuras Torre + cuarto basuras transitorio P1 + cuarto general
- [ ] Revisar que Lavadora tiene puntos HS en programación (el documento lo menciona)
- [ ] Verificar barandas escaleras internas casas: acero + platina (no solo tubería)
- [ ] Unificar todos los archivos en un solo Excel maestro definitivo

---

## 🗂 CARPETAS DEL PROYECTO

```
C:\Users\MI PC\Documents\SANTA-ISABEL-DOS-QUEBRADAS\
├── 02_DISENO_ESTRUCTURAL\
│   └── 02.1_Planos_vigentes\
│       ├── 1. PARQUEDERO ZONA SOCIAL\   ← Planos + Memorias Parqueadero
│       ├── 2. TORRE 12 PISOS\           ← Planos + Memorias Torre
│       └── 3. CASAS\                   ← Planos + Memorias Casas
├── 04_PRESUPUESTO_Y_CANTIDADES\
│   └── 04.1_Cantidades_vigentes\       ← Memorias de cantidades Excel
└── 05_PROGRAMACION\
    └── 05.1_Cronograma_maestro\        ← Todos los archivos de programación
```

