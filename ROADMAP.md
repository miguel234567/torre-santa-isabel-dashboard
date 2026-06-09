# Roadmap de Escalamiento — Contro360° Torre Santa Isabel

Plan por fases para llevar el dashboard de "archivo HTML compartido" a "plataforma de control de obra desplegada y multiusuario". Cada fase tiene objetivo, tareas, **revisión exhaustiva** (checklist de salida) y no se pasa a la siguiente sin cumplirla.

---

## FASE 1 — Base segura y verificable ✅ (casi completa)

**Objetivo:** que el código sea seguro, válido y reproducible antes de invitar usuarios.

| Tarea | Estado |
|---|---|
| Escape XSS (`esc()`) en todo `innerHTML` con datos de usuario/Sheet | ✅ Hecho |
| Contraseñas hasheadas SHA-256 (sin texto plano en el fuente) | ✅ Hecho |
| CI valida JS antes de cada deploy | ✅ Hecho |
| `deploy-torre` generado por CI, no a mano | ✅ Hecho |
| CSS de impresión para reporte PDF | ✅ Hecho |
| **Cambiar las 5 contraseñas por defecto desde el tab Admin** | ⬜ Pendiente (tú) |
| Commit + push de los cambios actuales | ⬜ Pendiente |

**Revisión exhaustiva de salida:**
- [ ] `node` valida los 2 bloques `<script>` sin errores
- [ ] Buscar `password:'` en el fuente → 0 resultados
- [ ] Abrir el sitio público y ver código fuente: ninguna credencial legible
- [ ] Probar login con cada rol (ADMIN, EDITOR, LECTOR, LIMITADO) y verificar qué puede ver/editar cada uno
- [ ] Probar en Chrome, Edge y un celular Android (los residentes usarán móvil)

---

## FASE 2 — Datos centralizados (el salto más importante)

**Objetivo:** que TODOS vean los mismos datos. Hoy avances, personal, notas y bitácora viven en el navegador de cada quien.

**Tareas:**
1. Desplegar `apps-script-writeback.gs` → pegar URL en `WB_URL` (instrucciones en el archivo)
2. Crear hojas adicionales en el Sheet: `Personal`, `Notas`, `Bitacora`, `Usuarios`
3. Extender el Apps Script con acciones `?action=personal|notas|bitacora` (lectura y escritura)
4. Migrar los módulos Personal, Notas Kanban y Bitácora de localStorage → Sheet (localStorage queda como caché offline)
5. Manejo de conflictos: timestamp por registro; el último gana + aviso visual si alguien más editó
6. Conectar `RQ_SHEET_ID` (requisiciones)

**Revisión exhaustiva de salida:**
- [ ] URL `/exec` responde `{"ok":true}` en el navegador
- [ ] Editar avance en PC A → aparece en PC B tras el sync (≤60 s)
- [ ] Crear/editar/borrar trabajador, nota y requisición desde 2 dispositivos distintos
- [ ] Simular pérdida de internet: la app no se rompe, muestra estado offline y reintenta
- [ ] Revisar cuota de Apps Script (límite ~20.000 ejecuciones/día — sobra para una obra, verificar igualmente)
- [ ] Backup: descargar copia del Sheet semanal (puede automatizarse con trigger de Apps Script)

---

## FASE 3 — Despliegue profesional

**Objetivo:** salir de surge.sh hacia un hosting con dominio propio, HTTPS y control de acceso real.

**Tareas:**
1. Migrar a **Cloudflare Pages** o **Netlify** (gratis, mejor que surge: dominio propio, headers de seguridad, analytics)
2. Dominio propio: ej. `control.cvaconstructora.com` (≈ USD 10–15/año)
3. **Protección de acceso a nivel de servidor**: Cloudflare Access (gratis hasta 50 usuarios) — pide correo autorizado ANTES de servir la página. Esto sí es seguridad real; el login interno queda solo para roles
4. Headers de seguridad: `Content-Security-Policy`, `X-Frame-Options`, `Referrer-Policy`
5. Actualizar GitHub Actions para el nuevo hosting

**Revisión exhaustiva de salida:**
- [ ] El sitio NO abre sin autorización (probar en ventana incógnito)
- [ ] HTTPS con certificado válido y dominio propio
- [ ] securityheaders.com → calificación A
- [ ] Lighthouse (Chrome DevTools): Performance y Best Practices ≥ 90
- [ ] El deploy automático sigue funcionando en cada push
- [ ] surge.sh antiguo dado de baja (`surge teardown`) para que no quede una copia vieja pública

---

## FASE 4 — Multiusuario real y auditoría

**Objetivo:** roles que se cumplen en el servidor, no solo en el navegador.

**Tareas:**
1. Usuarios y roles en la hoja `Usuarios` del Sheet (no en localStorage)
2. El Apps Script valida un token de sesión en cada escritura y rechaza si el rol no permite la acción
3. Bitácora inmutable: cada escritura al Sheet registra quién/cuándo/qué en la hoja `Bitacora` (desde el servidor)
4. Notificación por correo automática (Apps Script `MailApp`) cuando una fase crítica entra en atraso

**Revisión exhaustiva de salida:**
- [ ] Intentar escribir al Apps Script con rol LECTOR (via consola/Postman) → rechazado
- [ ] Toda edición queda en la bitácora con autor real
- [ ] Correo de alerta llega al atrasarse una fase crítica (probar forzando una fecha)
- [ ] Revisión de permisos del Sheet: solo tu cuenta tiene edición directa

---

## FASE 5 — Mantenibilidad y calidad continua

**Objetivo:** que el proyecto aguante crecer sin romperse.

**Tareas:**
1. **Build paso a single-file**: separar el código en `src/` (css/js por módulo) y un script que genere el HTML único — se mantiene el patrón "un archivo desplegado" pero se edita modular
2. Tests automáticos de lógica pura (estados de fase, fechas, EVM) con `node:test` en el CI
3. Captura de errores en producción: handler `window.onerror` que registra en una hoja `Errores` del Sheet (o Sentry gratuito)
4. Versionado visible: número de versión + fecha de build en el footer

**Revisión exhaustiva de salida:**
- [ ] `npm run build` genera el HTML idéntico en estructura al actual
- [ ] CI corre tests y falla el deploy si algo se rompe
- [ ] Provocar un error JS a propósito → queda registrado con stack y usuario
- [ ] Un desarrollador nuevo puede montar el entorno solo leyendo el README

---

## FASE 6 — Escala de producto (ObraFlow)

**Objetivo:** de "dashboard de una torre" a producto multi-proyecto (tu landing `index.html` ya apunta ahí).

**Tareas:**
1. Multi-proyecto: selector de obra → cada obra es un Sheet distinto (config en un Sheet maestro)
2. PWA: manifest + service worker → instalable en el celular, funciona offline en obra
3. Exportación Excel/PDF nativa desde cada módulo
4. Si el volumen crece (>5 obras, >30 usuarios): migrar backend de Sheets a una base real (Supabase/Firebase, capa gratuita) manteniendo el frontend
5. Curva S de cronograma, forecast de fecha fin, dashboard ejecutivo consolidado

**Revisión exhaustiva de salida:**
- [ ] Crear una obra nueva toma <15 min sin tocar código
- [ ] PWA instala y abre offline mostrando el último snapshot
- [ ] Prueba de carga: 30 usuarios sincronizando a la vez sin errores de cuota
- [ ] Un usuario no técnico (residente) completa su flujo diario sin ayuda

---

## Orden y esfuerzo estimado

| Fase | Esfuerzo | Dependencia |
|---|---|---|
| 1. Base segura | 1 hora (resta cambiar claves + push) | — |
| 2. Datos centralizados | 1–2 días | Fase 1 |
| 3. Despliegue profesional | medio día + dominio | Fase 2 |
| 4. Multiusuario real | 2–3 días | Fases 2 y 3 |
| 5. Mantenibilidad | 2–3 días | puede ir en paralelo |
| 6. Producto | por etapas, según necesidad | Fases 2–5 |

**Regla de oro:** no avanzar de fase sin pasar su checklist completo. La Fase 2 es la que cambia la vida del equipo; las Fases 3–4 son las que permiten confiar en los datos; la 5 es la que evita que el archivo de 6.400 líneas se vuelva inmanejable; la 6 es el negocio.
