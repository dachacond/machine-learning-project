const form = document.getElementById('score-form');
const input = document.getElementById('input-data');
const output = document.getElementById('output');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  output.textContent = 'Enviando...';

  const text = input.value.trim();
  if (!text) {
    output.textContent = 'Introduce datos en el textarea.';
    return;
  }

  // Convertir la línea CSV en array. Permitimos varias filas separadas por nueva línea.
  const rows = text.split('\n').map(r => r.trim()).filter(Boolean).map(r => r.split(',').map(s => {
    const t = s.trim();
    // intentar parsear número, si no es número dejar como string
    const n = Number(t);
    return isNaN(n) ? t : n;
  }));

  try {
    const res = await fetch('/score_proba', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ data: rows })
    });

    const json = await res.json();
    console.log('response from /score_proba', res, json);
    if (!res.ok) {
      output.textContent = `Error ${res.status}: ${json.detail || JSON.stringify(json)}`;
      return;
    }

    // Construir salida legible usando la predicción que entrega el backend
    const lines = [];
    const probs = json.probabilities || [];
    const preds = json.predictions || [];
    for (let i = 0; i < rows.length; i++) {
      const p = probs[i] !== undefined ? probs[i] : null;
      const pred = preds[i] !== undefined ? preds[i] : (p !== null ? (p >= 0.5 ? 1 : 0) : null);
      lines.push(`Fila ${i+1}: entrada=${JSON.stringify(rows[i])}`);
      lines.push(`  Predicción (backend) = ${pred}`);
      lines.push(`  Probabilidad P(y=1) = ${p === null ? 'N/A' : p.toFixed(4)}`);
      lines.push('');
    }
    output.textContent = lines.join('\n');

  // Mostrar JSON crudo si el usuario lo desea
  const showRaw = document.getElementById('show-raw').checked;
    if (showRaw) {
      const rawEl = document.createElement('pre');
      rawEl.style.background = '#f6f6f6';
      rawEl.style.padding = '8px';
      rawEl.style.marginTop = '12px';
      rawEl.textContent = JSON.stringify(json, null, 2);
      output.appendChild(rawEl);
    }
  } catch (err) {
    output.textContent = 'Error de conexión: ' + err.message;
  }
});
