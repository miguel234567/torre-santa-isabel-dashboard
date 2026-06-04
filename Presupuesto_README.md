# 📊 Presupuesto BIM — Excel ↔ Dashboard

Guía completa para usar `Presupuesto_TorreSantaIsabel_BIM.xlsx` y conectarlo al dashboard `gantt-santa-isabel.html`.

---

## 🗂 Estructura del Excel (5 hojas interconectadas)

| Hoja | Contenido | Qué editas tú | Qué se calcula solo |
|---|---|---|---|
| **PORTADA** | Datos del proyecto + KPIs ejecutivos | Datos del proyecto (azul) | KPIs traídos del Resumen (verde) |
| **EDT** | Presupuesto base por capítulos y partidas | Metrado, V.Unit, Ejecutado (azul) | Presupuesto = Metrado × V.Unit, totales por capítulo, % ejec |
| **APU** | Análisis de Precios Unitarios partida 02.03 | Cantidades, jornales, AIU% (azul) | Costo directo, AIU absoluto, costo total, desviación vs real |
| **OrdenesCambio** | Registro de OCC del proyecto | Código, descripción, valor (azul) | Suma total alimenta el Resumen |
| **Resumen** | EVM completo (CPI, EAC, etc.) | Nada — todo automático | Todas las métricas + conclusión gerencial |

### Convención de colores (estándar industria)

| Color | Significado |
|---|---|
| 🔵 **Azul** | Inputs editables (escribir aquí) |
| ⚫ **Negro** | Fórmulas locales (NO tocar) |
| 🟢 **Verde** | Referencias entre hojas (NO tocar) |
| 🟡 **Fondo amarillo** | Totales / KPIs clave |
| 🔴 **Fondo rojo** | Partida con sobrecosto (>100% ejec.) |

---

## 📝 Cómo llenar el Excel

### 1. PORTADA
- Edita los **8 campos azules** (Proyecto, Contratista, Director, Fechas, Plazo, Modelo IFC, Versión)
- Los KPIs (Presupuesto total, CPI, EAC, etc.) se llenan automáticamente cuando llenes el resto.

### 2. EDT (lo más importante)
Para cada **partida**:
1. Llena **Metrado** (columna E) → cantidad física a ejecutar
2. Llena **V. Unit.** (columna F) → precio unitario presupuestado
3. La columna **Presupuesto** (G) se calcula automático: `=E × F`
4. Llena **Ejecutado** (H) → valor ya gastado a la fecha (se actualiza con cada corte)
5. La columna **% Ejec** (I) se colorea: verde si 95-100%, rojo si >100% (sobrecosto)

Para **capítulos** (filas grises 01, 02, 03, etc.) **NO escribas nada** — la suma se calcula con `SUMIFS` automáticamente.

### 3. APU (opcional, para partidas BIM críticas)
- Cambia el código en `C4` para indicar qué partida estás analizando
- Llena materiales (cantidad, desperdicio %, V.unit) y MO (rendimiento, prestaciones %, jornal)
- El **costo directo + AIU** se calcula solo
- La **desviación** compara contra el V.unit real del EDT automáticamente

### 4. OrdenesCambio
Cada vez que apruebes una OCC:
- Agrega una fila con `OC-Cxxx`, descripción, partida afectada, fase, valor, impacto plazo, solicitante, estado
- El **total** se suma automático y alimenta el Resumen → desviación total

### 5. Resumen
**NO TOCAR.** Lee todo desde las otras hojas. Te da en automático:
- Presupuesto base, Comprometido, Ejecutado (AC), Desviación
- PV, EV, AC, **CPI**, **EAC**, VAC, **SPI**
- Conclusión gerencial escrita en lenguaje natural

---

## 🌐 Conectar al Dashboard (gantt-santa-isabel.html)

El dashboard ya tiene la infraestructura lista — solo necesitas pegar el Sheet ID.

### Paso 1: Subir el Excel a Google Drive
1. Abre [drive.google.com](https://drive.google.com)
2. Arrastra `Presupuesto_TorreSantaIsabel_BIM.xlsx` a la carpeta:
   `https://drive.google.com/drive/folders/1HLYI4F_hIw6pYYnswoHg2GM9CQH7OIJ7`
3. Click derecho en el archivo → **Abrir con → Hojas de cálculo de Google**
4. Esto crea una copia como **Google Sheet** (la versión que se puede leer por API)

### Paso 2: Compartir como público (necesario para JSONP)
1. En el Sheet, click en **Compartir** (botón azul arriba derecha)
2. En "Acceso general" → **Cualquier persona con el enlace**
3. Rol: **Lector**
4. Click en **Copiar enlace**

### Paso 3: Extraer el Sheet ID
La URL se ve así:
```
https://docs.google.com/spreadsheets/d/  1AbCdEfGhIjKlMnOpQrStUvWxYz1234567890  /edit?gid=0
                                       └──────────────── este es el SHEET ID ────────────┘
```
Copia **solo la parte entre `/d/` y `/edit`**.

### Paso 4: Pegarlo en el dashboard
1. Abre `gantt-santa-isabel.html` en un editor de texto
2. Busca: `const SHEET_ID_PRESUPUESTO = '';`
3. Reemplaza por:
   ```js
   const SHEET_ID_PRESUPUESTO = '1AbCdEfGhIjKlMnOpQrStUvWxYz1234567890';
   ```
4. Guarda. Refresca el dashboard. La pestaña **Presupuesto BIM** ahora lee del Sheet.

### Paso 5: Configurar nombres de hojas (si los cambiaste)
Si renombraste alguna hoja, edita también:
```js
const SHEETS_PRESUPUESTO_TABS = {
  edt: 'EDT',           // ← cambiar si renombraste
  apu: 'APU',
  occ: 'OrdenesCambio',
  resumen: 'Resumen'
};
```

---

## 🔧 Formato esperado de las columnas (Google Sheet)

Para que el JSONP funcione, **NO modifiques estos encabezados**:

### Hoja EDT (lo más importante)
| A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|
| Código | Descripción | BIM | Unidad | Metrado | V.Unit | Presupuesto | Ejecutado | % Ejec |

### Hoja OrdenesCambio
| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| Código | Descripción | Partida | Fase | Valor | Impacto | Solicitante | Estado |

### Hoja Resumen
La hoja Resumen se lee directamente — el dashboard busca las celdas:
- `C5` → Presupuesto base
- `C7` → Ejecutado (AC)
- `C14` → CPI
- `C15` → EAC

---

## 🔄 Endpoint JSONP (técnico, para referencia)

El dashboard hace una llamada como esta:
```
https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=responseHandler:cb&sheet=EDT
```

- ✅ Sin OAuth (solo lectura, sheet compartido público)
- ✅ Sin CORS (gviz devuelve JSONP)
- ✅ Cache de 60s (mismo patrón que `syncWithSheet()`)
- ❌ Solo lectura (para escribir necesitas Apps Script proxy — pendiente del roadmap)

---

## ⚠ Tips operativos

| Situación | Qué hacer |
|---|---|
| Quiero agregar un capítulo nuevo | En el Sheet: inserta una fila gris con código (ej. `06`) y nombre. El SUMIFS lo capturará automático si las partidas empiezan con `06.xx` |
| Quiero agregar una partida nueva | Inserta fila después de la última de su capítulo. Llena código `XX.YY`, descripción, unidad, metrado, V.unit. Las fórmulas en G, H, I se autocompletan al copiar la fila previa |
| El CPI me sale negativo o > 2 | Revisa que la columna **Ejecutado** del EDT esté llena. Si todo está en 0, CPI dará error |
| El dashboard no muestra los nuevos datos | (1) Refresca `Ctrl+Shift+R`. (2) Verifica que el Sheet sea público. (3) Confirma SHEET_ID correcto. (4) Mira la consola DevTools por errores |
| Quiero versionar el presupuesto | Duplica el Sheet con nombre `Presupuesto_v2_TSI`. Tendrás un Sheet ID nuevo. La versión anterior queda como respaldo |

---

## 📅 Roadmap de mejoras futuras al Excel

- [ ] Hoja **Cronograma** que vincule cada partida a una fase del Gantt
- [ ] Hoja **Recursos** con base de datos de salarios + insumos del país (auto-actualiza APUs)
- [ ] Macro VBA / Apps Script para **importar metrado desde IFC** (cuando se integre BIM real)
- [ ] Conexión **bidireccional Sheet ↔ Dashboard** (write-back con Apps Script proxy)

---

**Mantenedor del template:** Miguel Salazar · CVA Constructora · Junio 2026
