/**
 * Torre Santa Isabel — Write-back de avances al Google Sheet
 * ───────────────────────────────────────────────────────────
 * CÓMO DESPLEGAR (5 minutos):
 * 1. Abre el Sheet del cronograma → Extensiones → Apps Script
 * 2. Borra el contenido y pega este archivo completo
 * 3. Implementar → Nueva implementación → tipo "Aplicación web"
 *    - Ejecutar como: Tú (tu cuenta)
 *    - Acceso: Cualquier persona
 * 4. Copia la URL que termina en /exec
 * 5. En gantt-santa-isabel.html pégala en:  const WB_URL = 'AQUÍ';
 *
 * El dashboard envía POST con body JSON:
 *   { sheetId, updates: [ { id, progress?, start?, end?, name?,
 *     predecessors?, group?, owner?, critical?, isNew?, deleted? } ] }
 */

var SHEET_NAME = ''; // vacío = primera hoja. O pon el nombre exacto, ej. 'Cronograma'

function doPost(e) {
  try {
    var body = JSON.parse(e.postData.contents);
    var ss = SpreadsheetApp.openById(body.sheetId);
    var sh = SHEET_NAME ? ss.getSheetByName(SHEET_NAME) : ss.getSheets()[0];
    if (!sh) return _json({ ok: false, error: 'Hoja no encontrada' });

    var data = sh.getDataRange().getValues();
    var headers = data[0].map(function(h){ return String(h).toUpperCase().trim(); });

    // Misma lógica de detección de columnas que el dashboard
    var col = {
      id:    _find(headers, ['FASE','ID','CODIGO','CÓDIGO']),
      name:  _find(headers, ['NOMBRE','ACTIVIDAD']),
      group: _find(headers, ['GRUPO']),
      start: _find(headers, ['INICIO','START']),
      end:   _find(headers, ['FIN','END','TERMINA']),
      pct:   _find(headers, ['AVANCE','%','PROGRESO']),
      owner: _find(headers, ['RESPONSABLE','OWNER']),
      crit:  _find(headers, ['CRITICA','CRÍTICA']),
      pred:  _find(headers, ['PREDECESOR','PRED','DEPENDS'])
    };
    if (col.id < 0) return _json({ ok: false, error: 'No encuentro la columna de código de fase' });

    // Índice fila por id de fase
    var rowOf = {};
    for (var r = 1; r < data.length; r++) {
      var v = String(data[r][col.id] || '').trim().toUpperCase();
      if (v) rowOf[v] = r + 1; // 1-based
    }

    var applied = 0, errors = [];
    (body.updates || []).forEach(function(u) {
      var id = String(u.id || '').trim().toUpperCase();
      if (!id) return;
      var row = rowOf[id];

      if (u.deleted) {
        if (row) { sh.deleteRow(row); delete rowOf[id]; _reindex(rowOf, row); applied++; }
        return;
      }
      if (!row) {
        if (!u.isNew) { errors.push(id + ': fila no encontrada'); return; }
        row = sh.getLastRow() + 1;
        sh.getRange(row, col.id + 1).setValue(u.id);
        rowOf[id] = row;
      }
      _set(sh, row, col.name,  u.name);
      _set(sh, row, col.group, u.group);
      _set(sh, row, col.start, u.start);
      _set(sh, row, col.end,   u.end);
      _set(sh, row, col.owner, u.owner);
      _set(sh, row, col.pred,  u.predecessors);
      if (u.progress !== undefined && col.pct >= 0)
        sh.getRange(row, col.pct + 1).setValue(Number(u.progress));
      if (u.critical !== undefined && col.crit >= 0)
        sh.getRange(row, col.crit + 1).setValue(u.critical ? 'SI' : 'NO');
      applied++;
    });

    return _json({ ok: true, applied: applied, errors: errors });
  } catch (err) {
    return _json({ ok: false, error: String(err) });
  }
}

// GET de prueba: abre la URL /exec en el navegador y debes ver {"ok":true,...}
function doGet() {
  return _json({ ok: true, service: 'TSI write-back', version: 1 });
}

function _find(headers, keys) {
  for (var i = 0; i < headers.length; i++)
    for (var k = 0; k < keys.length; k++)
      if (headers[i].indexOf(keys[k]) !== -1) return i;
  return -1;
}
function _set(sh, row, colIdx, val) {
  if (val !== undefined && val !== null && colIdx >= 0)
    sh.getRange(row, colIdx + 1).setValue(val);
}
function _reindex(rowOf, deletedRow) {
  for (var k in rowOf) if (rowOf[k] > deletedRow) rowOf[k]--;
}
function _json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
