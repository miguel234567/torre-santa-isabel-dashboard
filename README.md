# Contro360 — Dashboard Torre Santa Isabel

[![Deploy](https://img.shields.io/badge/deploy-surge.sh-brightgreen)](https://torre-santa-isabel.surge.sh)
[![Stack](https://img.shields.io/badge/stack-HTML%20%2B%20CSS%20%2B%20JS%20vanilla-blue)]()
[![Backend](https://img.shields.io/badge/backend-Google%20Sheets%20%2B%20localStorage-orange)]()
[![Status](https://img.shields.io/badge/roadmap-~40%25-yellow)]()

Dashboard de gestión de obra **single-file HTML** para Torre Santa Isabel (CVA Constructora).
Objetivo a largo plazo: evolucionar a un ERP completo de construcción ("Contro360").

🌐 **Producción:** https://torre-santa-isabel.surge.sh _(deploy automático en cada push a `main`)_

---

## 🚀 Módulos activos (14 tabs)

| Grupo | Tabs |
|---|---|
| **Análisis** | KPIs & Salud · Cronograma Gantt · Fases del Proyecto |
| **Gestión** | Tablero Kanban · Actualizar Avance · Calendario · Planeación 360 |
| **Compras** | Requisiciones · Órdenes de Compra · Proveedores |
| **Finanzas** | Presupuesto BIM (EDT + APU + EVM) |
| **Registro** | Bitácora · Equipos · Personal |
| **Admin** | Gestión usuarios (rol-bound) |

## 🧱 Arquitectura

- **Single-file:** todo en `gantt-santa-isabel.html` (~5500 líneas, CSS + HTML + JS inline)
- **Sin frameworks:** vanilla JS puro, sin build step
- **BD híbrida:**
  - Google Sheets vía JSONP gviz (datos del cronograma, fases)
  - localStorage (notas Kanban, Personal, Bitácora, sesión usuario)
- **Diseño v2:** sistema de tokens semánticos (`--surf`, `--bdr`, `--acc`, `--grn/--amb/--red`), light/dark mode
- **Fuentes:** Plus Jakarta Sans · Inter · JetBrains Mono · Material Symbols

## 📂 Estructura del repo

```
.
├── gantt-santa-isabel.html              ← Dashboard principal (TODO está aquí)
├── deploy-torre/
│   └── index.html                        ← Copia que se deploya a surge.sh
├── Presupuesto_TorreSantaIsabel_BIM.xlsx ← Template Excel con 5 hojas y 79 fórmulas
├── Presupuesto_README.md                 ← Guía de conexión Excel → Drive → Dashboard
├── scripts/
│   └── build_presupuesto.py              ← Generador reproducible del Excel
├── IMAGENES_LOGOS/                       ← Logos CVA, 1A, TSI
├── Resumen/                              ← Resúmenes ejecutivos
├── CLAUDE.md                             ← Contrato del proyecto (patrones críticos)
├── .github/workflows/deploy.yml          ← CI/CD: push → surge
└── README.md                             ← este archivo
```

## 🛠 Desarrollo local

### Requisitos
- Python 3 (para servir el archivo localmente)
- Navegador moderno (Chrome 120+, Edge 120+, Firefox 122+)

### Levantar servidor
```bash
cd "ruta-al-proyecto"
python -m http.server 3000
# Abrir: http://localhost:3000/gantt-santa-isabel.html
```

### Validar JS sin ejecutar
```bash
node -e "const fs=require('fs');const h=fs.readFileSync('gantt-santa-isabel.html','utf8');const m=[...h.matchAll(/<script>([\s\S]*?)<\/script>/g)];m.forEach((s,i)=>{try{new Function(s[1]);console.log('✅ script',i+1)}catch(e){console.error('❌',e.message)}})"
```

### Regenerar Excel Presupuesto
```bash
python scripts/build_presupuesto.py
```

## 🚢 Deploy

### Automático (en cada push a `main`)
GitHub Actions:
1. Valida sintaxis JS
2. Copia `gantt-santa-isabel.html` → `deploy-torre/index.html`
3. Deploya `deploy-torre/` a `torre-santa-isabel.surge.sh`

### Manual (emergencia)
```bash
cp gantt-santa-isabel.html deploy-torre/index.html
npx surge deploy-torre torre-santa-isabel.surge.sh
```

## 🗺 Roadmap

```
✅ Capa 0  Gestión obra    100%   KPIs · Gantt · Fases · Kanban · Bitácora
🟡 Capa 1  Compras          30%   UI lista, mock data
🟡 Capa 2  Presupuesto/Bod  25%   Presupuesto UI ✅ · Bodega/Subc/Docs ⚪
⚪ Capa 3  Admin/Financiero  0%   Nóminas · Contabilidad · FE DIAN · Venta
⚪ Capa 4  Dashboards gerenciales
⚪ Capa 5  Integración BIM (IFC, 4D, 5D)

Total ERP: ~40%
```

## 🤝 Contribuir

**Patrones críticos** (NO romper):
- **NUNCA dividir** en múltiples archivos (constraint single-file)
- Para nuevo módulo: prefix CSS único (ej. `oc-*` Compras, `bp-*` Presupuesto)
- TODOS los tokens nuevos requieren override en `body.light-mode`
- Patrón nuevo tab: botón sidebar → `<section id="tab-X">` → `renderedTabs.X = false` → `case` en `switchTab()`
- Validar JS antes de cada commit
- Commits descriptivos: `feat(modulo): descripción` · `fix(area): descripción`

Ver `CLAUDE.md` para detalles completos del contrato del proyecto.

## 📝 Licencia

Privado · CVA Constructora · Torre Santa Isabel · Junio 2026

**Mantenedor:** Miguel Salazar · `miguel.salazar@esing.edu.co`
