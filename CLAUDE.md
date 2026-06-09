# Torre Santa Isabel — Dashboard Contro360°

## Contexto del proyecto
Dashboard HTML de gestión de obra para **Torre Santa Isabel** (construcción, Dosquebradas, Colombia).
**Single-file app** (`gantt-santa-isabel.html`, ~6.400 líneas) con todo CSS + JS inline.
Producción: https://contro360-tsi.surge.sh (deploy automático por GitHub Actions en cada push a `main`).

## Archivos
```
gantt-santa-isabel.html       ← TODO el dashboard: CSS, HTML, JS en un solo archivo
index.html                    ← Landing page de ObraFlow (SaaS de construcción)
apps-script-writeback.gs      ← Apps Script para escritura al Sheet (ver instrucciones dentro)
.github/workflows/deploy.yml  ← Valida JS + copia gantt → deploy-torre/index.html + surge.sh
deploy-torre/                 ← Carpeta generada por CI (no editar a mano)
Presupuesto_TorreSantaIsabel_BIM.xlsx + Presupuesto_README.md
```

## Stack técnico
- **Sin frameworks** — HTML/CSS/JS vanilla puro
- **Google Sheets como base de datos** — lectura via JSONP gviz (sin CORS); columnas detectadas por encabezado (FASE/ID, AVANCE, INICIO, FIN, RESPONSABLE, PREDECESOR…)
- **SHEET_ID:** `1vZE1-3OY__CoKq_AErCDDMAoJ35vHMVH`
- **Write-back:** POST a `WB_URL` (Apps Script /exec) con `Content-Type: text/plain` (evita preflight CORS). `WB_URL` vacío = solo guarda local.
- **Fuentes:** Plus Jakarta Sans + Inter + JetBrains Mono; iconos Material Symbols
- **Persistencia local (localStorage):** `torre_santa_isabel_v1` (snapshot), `tsi_phases_crud_v1` (CRUD fases), `tsi_kanban_notes_v1`, `tsi_kpi_history_v1`, `tsi_users_v1`, `tsi_subprogress_v1`, `tsi_theme`; sesión en `sessionStorage.tsi_session`

## Tabs del dashboard (15)
| Tab | ID | Render |
|-----|-----|--------|
| KPIs | `tab-kpis` | `renderKPIs()` |
| Gantt | `tab-gantt` | `renderGantt()` (SVG, dependencias, hoy-line) |
| Fases | `tab-phases` | `renderTable()` (expandible, búsqueda con debounce, paginación) |
| Actualizar | `tab-update` | `renderUpdatePanel()` |
| Kanban | `tab-board` | `renderBoard()` (4 columnas + notas por fase) |
| Calendario | `tab-calendar` | `renderCalendar()` (Semana/Mes/Año, festivos CO) |
| Equipos | `tab-equipos` | agrupa fases por `owner` |
| Personal | `tab-personal` | registro de trabajadores (CRUD local) |
| Bitácora | `tab-bitacora` | `logChange()` → timeline de cambios |
| Presupuesto | `tab-presupuesto` | módulo BIM: Dashboard/EDT/APU/EVM/Reporte + curva S |
| Compras | `tab-compras` | órdenes de compra |
| Requisiciones | `tab-requisiciones` | requiere `RQ_SHEET_ID` (aún vacío) |
| Proveedores | `tab-proveedores` | directorio |
| Planeación | `tab-planeacion` | Last Planner |
| Admin | `tab-admin` | gestión de usuarios y diagnóstico |

## Auth & roles (client-side, NO es seguridad real)
- Roles: ADMIN / EDITOR / LECTOR / LIMITADO (este último restringido a `phases:[...]`)
- Usuarios en `localStorage.tsi_users_v1`; contraseñas como **SHA-256** (`passHash`, función `sha256()` inline). Login migra automáticamente usuarios legacy con `password` plano.
- ⚠️ Todo es visible en el código fuente público — el acceso real debe protegerse a nivel de hosting si importa.

## Seguridad / patrones obligatorios
- **`esc(s)`** — escapar SIEMPRE texto de usuario o del Sheet antes de interpolarlo en `innerHTML` (nombres de fase, owner, notas, personal, etc.)
- Contraseñas: nunca en texto plano; usar `sha256()` y campo `passHash`
- **NUNCA** dividir en múltiples archivos — todo en el único HTML
- **NUNCA** guardar tokens de Google en localStorage (no hay OAuth)
- Nueva tab: (1) botón en `<nav>`, (2) `<section id="tab-X">`, (3) `renderedTabs.X=false`, (4) case en `switchTab()`, (5) re-render en `reRenderAll()`
- Colores de grupo desde variables CSS `--grp-g/e/m/a/x`; light mode via `body.light-mode`
- Gantt SVG posiciona con `xOf(ms)` y `wOf(startMs, endMs)`
- Hay `@media print` (landscape) para reporte PDF via Ctrl+P — mantenerlo al agregar tabs

## Sync
- `syncWithSheet()` cada 60s, timeout 10s, JSONP. Overrides locales (CRUD/avance) tienen prioridad sobre el Sheet.
- `scheduleWriteBack()` → `doWriteBack()` (debounce 600ms) envía `{sheetId, updates:[...]}` a `WB_URL`.

## Roadmap pendiente
1. **Conectar write-back**: desplegar `apps-script-writeback.gs` y pegar URL en `WB_URL` (línea ~5360)
2. `RQ_SHEET_ID` para requisiciones
3. Centralizar usuarios/notas/bitácora en el Sheet (hoy divergen por dispositivo)
4. Curva S planificado vs real en KPIs (ya existe en Presupuesto)
5. Vista mobile-first

## Cómo probar cambios
1. Editar `gantt-santa-isabel.html` y abrir en navegador
2. Validar JS (hay 2 bloques `<script>`):
```bash
node -e "const fs=require('fs');const h=fs.readFileSync('gantt-santa-isabel.html','utf8');[...h.matchAll(/<script>([\s\S]*?)<\/script>/g)].forEach((m,i)=>{try{new Function(m[1]);console.log(i,'OK')}catch(e){console.error(i,e.message)}})"
```
3. El CI valida lo mismo antes de cada deploy
