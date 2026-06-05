# Torre Santa Isabel — Dashboard de Programación

## Contexto del proyecto
Dashboard HTML de gestión de obra para **Torre Santa Isabel** (proyecto de construcción colombiano).
Desarrollado como una **single-file app** (`gantt-santa-isabel.html`) con todo CSS + JS inline.

## Archivo principal
```
gantt-santa-isabel.html   ← TODO está aquí: CSS, HTML, JS en un solo archivo
index.html                ← Landing page de ObraFlow (SaaS de construcción)
```

## Stack técnico
- **Sin frameworks** — HTML/CSS/JS vanilla puro
- **Google Sheets como base de datos** — lectura via JSONP gviz endpoint (sin CORS)
- **SHEET_ID:** `1vZE1-3OY__CoKq_AErCDDMAoJ35vHMVH`
- **Fuentes:** Inter + JetBrains Mono (Google Fonts)
- **Persistencia local:** `localStorage` con key `torre_santa_isabel_v1`

## Arquitectura del archivo HTML

### Variables CSS (`:root`)
- `--bg-app`, `--bg-card`, `--bg-el` → fondos en capas
- `--border`, `--border-s`, `--border-f` → bordes
- `--txt`, `--txt-s`, `--txt-m`, `--txt-a` → textos
- `--grp-g/e/m/a/x` → colores por grupo (Gestión/Estructura/MEP/Acabados/Exteriores)
- `body.light-mode` → sobrescribe variables para tema claro

### Datos principales (JS)
```js
const PHASES = [...] // 29 fases (F0–F28) con: id, code, name, group, start, end, progress, owner, critical
const SUBACTIVITIES_RAW = {...} // sub-tareas por fase con EDT, nombre, duración, responsable
```

### Tabs del dashboard
| Tab | ID | Función de render |
|-----|-----|-------------------|
| KPIs | `tab-kpis` | `renderKPIs()` |
| Gantt | `tab-gantt` | `renderGantt()` |
| Fases | `tab-phases` | `renderTable()` |
| Actualizar | `tab-update` | `renderUpdatePanel()` |
| Tablero Kanban | `tab-board` | `renderBoard()` |
| Calendario | `tab-calendar` | `renderCalendar()` |

### Funciones clave
- `syncWithSheet()` → lee Google Sheets via JSONP, auto-sync cada 60s
- `renderGantt()` → SVG con barras, hoy-line, tooltips
- `renderTable()` → tabla con filas expandibles (sub-actividades)
- `renderBoard()` → Kanban 4 columnas estilo ClickUp
- `renderCalendar()` → vistas Semana/Mes/Año con estados LIBERADO/EN_PROGRESO/etc
- `toggleTheme()` → light/dark mode con `body.light-mode`
- `getSubActivities(phaseId)` → calcula fechas de sub-tareas desde startMs del padre
- `reRenderAll()` → re-renderiza todos los tabs activos tras sync

### Sistema de estados de fase
```js
// Calculado en PHASES como propiedad `status`:
'COMPLETADO'  // progress >= 100
'ATRASADO'    // progress < expected && today > start
'EN_PROGRESO' // progress > 0 && progress < 100
'PENDIENTE'   // sin avance, no iniciada
```

### Sync con Google Sheets (solo lectura actualmente)
```js
// Endpoint JSONP:
`https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?tqx=responseHandler:${cb}`
// Columnas esperadas: A=Código, B=Nombre, C=Grupo, D=FechaInicio, E=FechaFin, F=Avance%, G=Responsable, H=Crítica
```

## Próximas funciones a implementar (Roadmap)

### 🔥 PRIORIDAD ALTA
1. **Sync bidireccional con Google Sheets**
   - Crear Google Apps Script Web App como proxy
   - Dashboard hace POST al script con `{sheetId, row, col, value}`
   - Script escribe en la celda y devuelve `{ok: true}`
   - Trigger `onEdit` en el Sheet incrementa versión en celda A1
   - Dashboard detecta cambio de versión y re-sincroniza

2. **Panel de Alertas & Riesgos** (sidebar)
   - Botón 🔔 fijo con badge contador
   - Lista: fases críticas atrasadas, % avance vs planificado, forecast de retraso

3. **Bitácora de cambios**
   - Log en localStorage: `{timestamp, phaseId, field, oldVal, newVal, user}`
   - Tab o modal "📋 Bitácora"

### PRIORIDAD MEDIA
4. **Vista Equipos** (nueva pestaña 👷)
   - Agrupar fases por `owner`
   - Barras de carga por persona
5. **Reporte PDF ejecutivo**
   - Usar `window.print()` con CSS `@media print` optimizado
   - O generar HTML → PDF con jsPDF (CDN)
6. **Dependencias en Gantt**
   - Flechas SVG entre barras dependientes
   - Ruta crítica resaltada en rojo

### PRIORIDAD BAJA
7. Curva S (planificado vs real)
8. Comentarios por fase
9. Vista mobile-first
10. Roles: Admin / Residente / Contratista

## Cómo probar cambios
1. Editar `gantt-santa-isabel.html`
2. Abrir en navegador (doble clic o arrastrar a Chrome)
3. Para verificar JS sin errores: `node -e "const fs=require('fs');const h=fs.readFileSync('gantt-santa-isabel.html','utf8');const m=h.match(/<script>([\s\S]*?)<\/script>\s*<\/body>/);try{new Function(m[1]);console.log('✅ JS OK')}catch(e){console.error('❌',e.message)}"`

## Patrones importantes a mantener
- **NUNCA** dividir en múltiples archivos — todo debe quedar en el único HTML
- **NUNCA** usar `localStorage` para almacenar el token de Google (no hay OAuth)
- Al agregar una nueva tab: (1) botón en `<nav>`, (2) sección `<section id="tab-X">`, (3) `renderedTabs.X = false`, (4) case en `switchTab()`, (5) re-render en `reRenderAll()`
- Los colores de grupo siempre desde variables CSS `--grp-*`
- El Gantt SVG usa `xOf(ms)` y `wOf(startMs, endMs)` para posicionar barras
