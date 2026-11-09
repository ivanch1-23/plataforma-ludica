# ADR 0001: Implementación del Motor de Racha Diaria

**Fecha:** 9 de noviembre de 2026

## Contexto
La plataforma de inglés requiere aplicar la mecánica de **Racha Diaria** asignada a Ivan Andres Diaz Lizcano. Se debe registrar la frecuencia diaria con la que los niños practican, premiar la constancia y reiniciar el conteo ante omisiones de un día completo.

## Alternativas

1. **Cálculo en cliente (LocalStorage / JavaScript):**
   - *Ventajas:* No requiere consultas a base de datos para mostrar el contador.
   - *Desventajas:* Fácilmente manipulable por el usuario o al cambiar de dispositivo; no permite que el docente consulte las métricas centralizadas.
2. **Cálculo reactivo en backend basado en fecha calendario:**
   - *Ventajas:* Seguro, auditable, almacena historial y permite al docente ver el avance en tiempo real.
   - *Desventajas:* Requiere manejo preciso de zonas horarias en el servidor.
3. **Cron job diario que reinicie rachas a medianoche:**
   - *Ventajas:* Proceso por lotes automatizado.
   - *Desventajas:* Complejidad innecesaria de infraestructura en el plan gratuito de Render; difícil manejo de usuarios inactivos.

## Decisión
Se adopta la **Alternativa 2 (Cálculo reactivo en backend en `app/servicios/racha.py`)**:
Cada vez que un estudiante completa una sesión de práctica, el backend compara la fecha actual con su `ultima_fecha_jugada`:
- Si la diferencia es de 1 día calendario: `racha_actual += 1`.
- Si la fecha es el mismo día: se mantienen los puntos pero la racha no aumenta nuevamente.
- Si la diferencia es > 1 día: `racha_actual = 1`.

## Consecuencias
- La lógica de negocio queda completamente aislada en la capa de servicios, con alta facilidad para ser testeada unitariamente con `pytest`.
- El modelo `Racha` almacenará el récord histórico (`mejor_racha`) y la última fecha de actividad.
