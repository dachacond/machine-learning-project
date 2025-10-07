# Hipótesis de negocio y ejemplo — Proyecto de Scoring

Este proyecto contiene un modelo que predice la probabilidad de un evento binario (0/1). El código y las métricas usan la convención estándar:

- Predicción (0 o 1): la decisión automática que toma el modelo usando su umbral interno (por defecto 0.5).  
- Probabilidad P(y=1): la confianza continua del modelo de que la observación pertenece a la clase 1 (es decir, P(clase=1)).

Importante: el repositorio no impone una interpretación de negocio para `0` o `1` —esa decisión es del negocio. Si tu evento de interés es la clase `0` (no la `1`), entonces calcula P(y=0) como 1 - P(y=1) y aplica las reglas sobre P(y=0).

Objetivo de negocio (resumen):

Usar el modelo para priorizar casos/usuarios/objetos que tienen mayor probabilidad de generar un comportamiento deseado o no deseado (por ejemplo: compra, churn, fraude, respuesta a campaña). Con una probabilidad podemos ordenar los casos y aplicar acciones distintas según el riesgo o la oportunidad.

Hipótesis concreta (expresada sobre P(y=1)):

1. Si la probabilidad P(y=1) es alta, entonces merece una acción inmediata (p. ej. ofrecer una promoción, asignar revisión manual, bloqueo temporal).  
2. Si la probabilidad P(y=1) es baja, no es necesario invertir recursos y se puede seguir con el flujo estándar.

Si prefieres trabajar sobre el evento `y=0`, sustituye P(y=1) por P(y=0)=1-P(y=1) en las reglas anteriores.

Reglas de ejemplo (ejecutable por negocio; expresadas sobre P(y=1)):

- P(y=1) >= 0.8 → Acción A (prioridad alta: contactación inmediata / revisión manual).  
- 0.5 <= P(y=1) < 0.8 → Acción B (monitorización o campaña complementaria).  
- P(y=1) < 0.5 → Acción C (sin acción adicional automática).

Si el evento de interés es `y=0`, usa las mismas reglas aplicadas a P(y=0)=1-P(y=1). Por ejemplo, P(y=0) >= 0.8 significa P(y=1) <= 0.2.

Ejemplo práctico (fila del archivo `data/score.csv` — línea 19):

Entrada (columnas):

- x1 = 6.769261  
- x2 = 20.316831  
- x3 = Thur (jueves)  
- x4 = 1.333796  
- x5 = 106.440653  
- x6 = Nebraska  
- x7 = ford


Salida del modelo (ejemplo real observado):

- Predicción (modelo): 1  
- Probabilidad P(y=1): ~0.52 (52%)

Interpretación simple para negocio:

1) Si el evento de interés es la clase `1`: este caso tiene una probabilidad ligeramente por encima del 50% de pertenecer a la clase positiva. No es una señal fuerte, pero es suficiente para tratarlo como candidato a una acción de seguimiento moderada (Acción B).

2) Si el evento de interés es la clase `0`: la probabilidad de `y=0` es P(y=0)=1-0.52 = 0.48 (48%). En este caso la observación no alcanza el umbral habitual del 50% para la clase `0`, por lo que no sería prioritaria (Acción C) —o dicho de otra forma, el modelo predice `1`, que indica que el caso no pertenece a la clase `0`.

Recomendación práctica:

1. No asignar recursos de alta prioridad (no aplicar Acción A).  
2. Incluir este caso en una lista de seguimiento o en una campaña complementaria (Acción B).  
3. Si el negocio necesita reducir falsos positivos, considerar elevar el umbral de decisión (por ejemplo usar 0.6 o 0.7) o exigir una segunda verificación manual antes de aplicar acciones costosas.

Notas y buenas prácticas:

- La probabilidad es continua: usarla para ordenar y segmentar (priorización).  
- Validar reglas con métricas reales (precisión, recall, AUC) en datos históricos y monitorear la performance en producción.  
- Revisar características y datos faltantes: si muchas filas tienen valores faltantes, la confianza del modelo puede bajar.

¿Qué sigue?

- Si quieren, podemos añadir al proyecto un README corto para negocio que incluya estas reglas y cómo interpretar las probabilidades, o un endpoint que devuelva explicaciones locales (p. ej. con SHAP) para cada predicción.
