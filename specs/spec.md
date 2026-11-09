# Especificación: Plataforma Lúdica de Inglés con Racha Diaria

## Contexto
- **Cliente:** Un instituto de inglés para niños.
- **Público objetivo:** Colegios de primaria que no cuentan con docentes especializados en inglés (los mismos docentes de aula dictan todas las materias y no dominan el idioma).
- **Problema que resuelve:** Permite a los niños aprender y practicar vocabulario en inglés mediante imágenes y audios interactivos alineados con los estándares del MEN, liberando al docente de preparar material complejo y facilitando el seguimiento del avance sin requerir que el docente domine el idioma.
- **Mecánica lúdica (Racha diaria):** Incentiva el hábito de práctica diaria mediante bonificaciones acumulativas de puntos por días consecutivos jugados, reiniciándose a 1 si se omite un día.
- **Acceso:** Dos roles bien diferenciados:
  - **Docente:** Administra clases, asigna temas de vocabulario y visualiza métricas de progreso y rachas.
  - **Niño:** Ingreso simplificado y seguro con **código de clase + avatar seleccionado** (sin contraseñas complejas ni correos electrónicos).

---

## Historias de usuario

### H1. Acceso del niño a su clase
Como **niño**,  
quiero **ingresar usando solo el código de mi clase y tocando mi avatar**,  
para **empezar a practicar mis actividades de inglés sin necesidad de recordar un correo o contraseña**.

**Criterios de aceptación:**
- Dado un código de clase válido, cuando el niño lo ingresa, entonces el sistema muestra la cuadrícula con los avatares de los niños inscritos en esa clase.
- Dado un avatar seleccionado, cuando el niño confirma su selección, entonces ingresa directamente a su panel de actividades y ve su racha actual.

### H2. Práctica de vocabulario con imagen y audio
Como **niño**,  
quiero **ver imágenes, escuchar la pronunciación en audio y asociar la palabra correspondiente**,  
para **aprender nuevo vocabulario de inglés de manera divertida**.

**Criterios de aceptación:**
- Dada una actividad de vocabulario (ej. animales o colores), cuando el niño escucha un audio o ve una tarjeta, entonces puede seleccionar la opción correcta entre varias alternativas visuales/texto.
- Dado que el niño responde, cuando envía la respuesta, entonces el sistema le muestra retroalimentación inmediata (acierto/error) con sonido o animación.

### H3. Registro y cálculo de la Racha Diaria
Como **niño**,  
quiero **ver mi contador de días seguidos jugando y ganar puntos extra**,  
para **motivarme a practicar todos los días y no perder mi racha**.

**Criterios de aceptación:**
- Dado un niño que ya practicó ayer, cuando completa al menos una actividad hoy, entonces su racha se incrementa en +1 y recibe puntos de bonificación por racha.
- Dado un niño que no ingresó el día anterior, cuando ingresa hoy, entonces su contador de racha se reinicia a 1 día.

### H4. Panel del docente para seguimiento de progreso
Como **docente**,  
quiero **ver el tiempo de práctica, palabras aprendidas y la racha de cada estudiante**,  
para **saber qué niños están cumpliendo sus metas de estudio y quiénes necesitan motivación**.

**Criterios de aceptación:**
- Dado un docente autenticado, cuando entra al panel de su clase, entonces visualiza una tabla con cada estudiante, su racha actual, racha máxima histórica y palabras dominadas.

---

## Requisitos funcionales

| Código | Requisito | Historia |
|---|---|---|
| **RF1** | El sistema debe permitir la creación de clases con código único alfanumérico por parte del docente. | H4 |
| **RF2** | El sistema debe permitir el acceso del estudiante mediante código de clase y selección de avatar. | H1 |
| **RF3** | El sistema debe presentar actividades interactivas de vocabulario (imagen + audio + opciones). | H2 |
| **RF4** | El sistema debe calcular y actualizar automáticamente la racha diaria y los puntos acumulados por estudiante al completar la primera sesión del día. | H3 |
| **RF5** | El sistema debe reiniciar la racha a 1 si ha pasado más de 1 día calendario desde la última práctica registrada. | H3 |
| **RF6** | El sistema debe listar al docente las métricas por estudiante (racha actual, mejor racha, palabras aprendidas). | H4 |

---

## Requisitos no funcionales

| Código | Requisito | Cómo se verifica |
|---|---|---|
| **RNF1** | Rendimiento y ligereza: la carga de actividades debe ser rápida en redes lentas de salón escolar. | Pruebas de carga y peso de recursos estáticos optimizados. |
| **RNF2** | Interfaz intuitiva para niños: uso predominante de iconos, colores legibles y tipografías grandes. | Inspección visual en dispositivos móviles y de escritorio. |
| **RNF3** | Privacidad de menores: no solicitar nombres completos, correos ni datos personales del niño. | Revisión del esquema de base de datos y endpoints de registro. |
| **RNF4** | Cobertura de pruebas: las reglas de cálculo de racha y avance deben estar probadas al 100%. | Pruebas unitarias con `pytest`. |

---

## Casos límite

1. **Juego en cambio de día:** Si el niño inicia una práctica antes de medianoche y termina después, el cómputo debe basarse en la fecha local del inicio de sesión.
2. **Múltiples sesiones en el mismo día:** Jugar más veces el mismo día suma puntos ordinarios, pero el contador de racha solo se incrementa una vez cada día calendario.
3. **Pérdida momentánea de conexión:** El resultado debe poder sincronizarse al reanudar la conexión sin penalizar la racha.

---

## Fuera de alcance
- Pagos o suscripciones en línea.
- Micrófono con inteligencia artificial avanzada para reconocimiento fonético (el audio será para escucha y repetición del niño).
- Chat abierto o interacción directa entre estudiantes.
