# Diagramas del Sistema de Optimización de Tiempo

## 🎨 Diagrama de Flujo del Algoritmo Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                      INICIO: Usuario + Token                    │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Validar Token JWT   │
                    └──────────┬───────────┘
                               │
                               ▼
                         ┌─────────┐
                         │ ¿Valid? │───NO──► [Error 401]
                         └────┬────┘
                              │ YES
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FASE 1: RECOLECCIÓN DE DATOS                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐      ┌──────────────────┐               │
│  │  Obtener Profile │      │ Obtener Tareas   │               │
│  │  - work_schedule │      │ - Goal tasks     │               │
│  │  - hours_per_week│      │ - Mind tasks     │               │
│  │  - hours_used    │      │ - Body tasks     │               │
│  └────────┬─────────┘      └────────┬─────────┘               │
│           │                         │                          │
│           └────────┬────────────────┘                          │
│                    │                                            │
└────────────────────┼────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│              FASE 2: ANÁLISIS DE DISPONIBILIDAD                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Horas Totales (24h)                                           │
│       │                                                         │
│       ├─► Restar Sueño (8h)          ─┐                       │
│       ├─► Restar Trabajo (8h)         ├─► Total Fijo: 18h    │
│       └─► Restar Cuidado Personal(2h)─┘                       │
│                                                                 │
│  Horas Libres = 24 - 18 = 6 horas disponibles                 │
│                                                                 │
│  División en Slots:                                            │
│  ┌────────────────┐              ┌────────────────┐           │
│  │ SLOT MATUTINO  │              │ SLOT VESPERTINO│           │
│  │ 06:00 - 09:00  │              │ 17:00 - 22:00  │           │
│  │ 2 horas (~120m)│              │ 5 horas (~300m)│           │
│  └────────────────┘              └────────────────┘           │
│                                                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│              FASE 3: CÁLCULO DE PRIORIDADES                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PARA CADA TAREA:                                              │
│                                                                 │
│  ┌──────────────────────────────────────────────────┐         │
│  │ 1. Base Score = type_weight × task_weight × 10  │         │
│  │    - Goals: 3.0 × weight × 10                   │         │
│  │    - Mind:  1.5 × weight × 10                   │         │
│  │    - Body:  1.5 × weight × 10                   │         │
│  └──────────────────────────────────────────────────┘         │
│                       │                                         │
│                       ▼                                         │
│  ┌──────────────────────────────────────────────────┐         │
│  │ 2. Urgency Multiplier (por deadline)            │         │
│  │    - Vence hoy/mañana:    × 3.0                 │         │
│  │    - Vence en 2-3 días:   × 2.5                 │         │
│  │    - Vence esta semana:   × 2.0                 │         │
│  │    - Vence en 2 semanas:  × 1.5                 │         │
│  │    - Sin deadline:        × 1.0                 │         │
│  └──────────────────────────────────────────────────┘         │
│                       │                                         │
│                       ▼                                         │
│  ┌──────────────────────────────────────────────────┐         │
│  │ 3. Duration Bonus                                │         │
│  │    - ≤ 30 min: +5 puntos                        │         │
│  │    - ≤ 60 min: +2 puntos                        │         │
│  │    - > 60 min: +0 puntos                        │         │
│  └──────────────────────────────────────────────────┘         │
│                       │                                         │
│                       ▼                                         │
│  ┌──────────────────────────────────────────────────┐         │
│  │ PRIORITY SCORE FINAL                             │         │
│  │ = (base × urgency) + duration_bonus              │         │
│  └──────────────────────────────────────────────────┘         │
│                                                                 │
│  Resultado: Lista de tareas ordenadas por score ↓              │
│                                                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│            FASE 4: ALGORITMO DE DISTRIBUCIÓN                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Tareas Ordenadas (por priority_score descendente)            │
│          │                                                      │
│          ▼                                                      │
│  ┌─────────────────┐                                          │
│  │ PARA CADA TAREA │◄────────────────┐                       │
│  └────────┬────────┘                 │                       │
│           │                          │                       │
│           ▼                          │                       │
│  ┌────────────────────────────┐     │                       │
│  │ Calcular duración+buffer   │     │                       │
│  │ = duration + 15 min        │     │                       │
│  └────────┬───────────────────┘     │                       │
│           │                          │                       │
│           ▼                          │                       │
│  ┌────────────────────────────┐     │                       │
│  │ Determinar slot preferido  │     │                       │
│  │ - Goals/Mind → Morning     │     │                       │
│  │ - Body → Evening           │     │                       │
│  └────────┬───────────────────┘     │                       │
│           │                          │                       │
│           ▼                          │                       │
│     ┌─────────────────┐             │                       │
│     │ ¿Cabe en slot   │             │                       │
│     │   preferido?    │             │                       │
│     └────┬───────┬────┘             │                       │
│          │YES    │NO                │                       │
│          │       │                  │                       │
│          │       ▼                  │                       │
│          │  ┌─────────────────┐    │                       │
│          │  │ ¿Cabe en slot   │    │                       │
│          │  │  alternativo?   │    │                       │
│          │  └────┬───────┬────┘    │                       │
│          │       │YES    │NO       │                       │
│          │       │       │         │                       │
│          ▼       ▼       ▼         │                       │
│     ┌──────┐ ┌──────┐ ┌──────┐   │                       │
│     │Asignar│ │Asignar│ │Saltar│   │                       │
│     │a Pref.│ │a Alt. │ │Tarea │   │                       │
│     └───┬───┘ └───┬───┘ └───┬──┘   │                       │
│         │         │         │       │                       │
│         └─────┬───┴─────────┘       │                       │
│               │                     │                       │
│               ▼                     │                       │
│     ┌────────────────────┐         │                       │
│     │ Restar tiempo del  │         │                       │
│     │ slot + calcular    │         │                       │
│     │ start_time y       │         │                       │
│     │ end_time           │         │                       │
│     └────────┬───────────┘         │                       │
│              │                     │                       │
│              └─────────────────────┘                       │
│              (siguiente tarea)                              │
│                                                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│              FASE 5: CÁLCULO DE MÉTRICAS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────┐                  │
│  │ Efficiency Score                        │                  │
│  │ = (tiempo_programado / tiempo_total)    │                  │
│  │   × 100                                 │                  │
│  │                                         │                  │
│  │ Ejemplo: 360min / 420min × 100 = 85.7% │                  │
│  └─────────────────────────────────────────┘                  │
│                                                                 │
│  ┌─────────────────────────────────────────┐                  │
│  │ Balance Score                           │                  │
│  │ = 100 - (Σ|actual% - ideal%| / 3)      │                  │
│  │                                         │                  │
│  │ Ideal: 60% goal, 20% mind, 20% body    │                  │
│  │ Actual: 63% goal, 18% mind, 19% body   │                  │
│  │ Score: 100 - ((3+2+1)/3) = 98%         │                  │
│  └─────────────────────────────────────────┘                  │
│                                                                 │
│  ┌─────────────────────────────────────────┐                  │
│  │ Productivity Score                      │                  │
│  │ = (efficiency × 0.6) +                  │                  │
│  │   (balance × 0.4)                       │                  │
│  │                                         │                  │
│  │ Ejemplo: (85.7×0.6)+(98×0.4) = 90.6%   │                  │
│  └─────────────────────────────────────────┘                  │
│                                                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                  RESULTADO FINAL (JSON)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  {                                                              │
│    "schedule": {                                               │
│      "morning": { "tasks": [...], "scheduled_minutes": 105 },  │
│      "evening": { "tasks": [...], "scheduled_minutes": 255 }   │
│    },                                                           │
│    "summary": {                                                │
│      "total_tasks_scheduled": 8,                              │
│      "efficiency_percentage": 85.7                            │
│    },                                                           │
│    "scores": {                                                 │
│      "productivity_score": 90.6                               │
│    }                                                            │
│  }                                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 Diagrama de Ejemplo de Ejecución

### Escenario: Usuario con 5 tareas pendientes

**Entrada:**
```
Usuario: Juan Pérez
Fecha: 2025-10-09
Hora actual: 06:00 AM

Profile:
- work_schedule: "9:00-17:00"
- hours_per_week: 40
- hours_used_this_week: 15

Tareas Pendientes:
1. [GOAL] "Completar proyecto final" - 90 min - deadline: mañana
2. [GOAL] "Estudiar capítulo 3" - 60 min - deadline: en 5 días
3. [MIND] "Meditación" - 30 min - sin deadline
4. [BODY] "Gym" - 60 min - sin deadline
5. [GOAL] "Revisar código" - 45 min - deadline: en 2 días
```

**Procesamiento:**

```
FASE 1: Cálculo de Tiempo Disponible
=====================================
- Slot Matutino: 06:00-09:00 = 180 min (3h)
  Descontando preparación: 120 min útiles

- Slot Vespertino: 17:00-22:00 = 300 min (5h)

Total disponible: 420 minutos (7h)


FASE 2: Cálculo de Prioridades
================================
Tarea 1: "Completar proyecto final"
  - Base: 3.0 (goal) × 1 (weight) × 10 = 30
  - Urgency: × 3.0 (deadline mañana)
  - Duration bonus: +0 (90min)
  - SCORE: 90.0

Tarea 5: "Revisar código"
  - Base: 3.0 × 1 × 10 = 30
  - Urgency: × 2.5 (deadline 2 días)
  - Duration bonus: +2 (45min)
  - SCORE: 77.0

Tarea 2: "Estudiar capítulo 3"
  - Base: 3.0 × 1 × 10 = 30
  - Urgency: × 2.0 (deadline 5 días)
  - Duration bonus: +2 (60min)
  - SCORE: 62.0

Tarea 3: "Meditación"
  - Base: 1.5 (mind) × 1 × 10 = 15
  - Urgency: × 1.0 (sin deadline)
  - Duration bonus: +5 (30min)
  - SCORE: 20.0

Tarea 4: "Gym"
  - Base: 1.5 (body) × 1 × 10 = 15
  - Urgency: × 1.0
  - Duration bonus: +2 (60min)
  - SCORE: 17.0

Lista ordenada:
1. Proyecto final (90.0)
2. Revisar código (77.0)
3. Estudiar cap.3 (62.0)
4. Meditación (20.0)
5. Gym (17.0)


FASE 3: Distribución en Slots
===============================

[Tarea 1: Proyecto final - 90min - GOAL]
  Prefer: Morning (alta prioridad)
  Duración+buffer: 90 + 15 = 105 min
  Morning disponible: 120 min
  ✓ Asignar a Morning: 06:00-07:30
  Morning restante: 15 min

[Tarea 2: Revisar código - 45min - GOAL]
  Prefer: Morning
  Duración+buffer: 45 + 15 = 60 min
  Morning disponible: 15 min (insuficiente)
  Evening disponible: 300 min
  ✓ Asignar a Evening: 17:00-17:45
  Evening restante: 240 min

[Tarea 3: Estudiar cap.3 - 60min - GOAL]
  Prefer: Morning
  Morning: 15 min (insuficiente)
  Duración+buffer: 60 + 15 = 75 min
  Evening disponible: 240 min
  ✓ Asignar a Evening: 18:00-19:00
  Evening restante: 165 min

[Tarea 4: Meditación - 30min - MIND]
  Prefer: Morning
  Morning: 15 min (insuficiente)
  Duración+buffer: 30 + 15 = 45 min
  Evening disponible: 165 min
  ✓ Asignar a Evening: 19:15-19:45
  Evening restante: 120 min

[Tarea 5: Gym - 60min - BODY]
  Prefer: Evening
  Duración+buffer: 60 + 15 = 75 min
  Evening disponible: 120 min
  ✓ Asignar a Evening: 20:00-21:00
  Evening restante: 45 min


FASE 4: Resultados
===================
Morning Schedule:
  06:00-07:30 | Proyecto final (90min) [GOAL]

Evening Schedule:
  17:00-17:45 | Revisar código (45min) [GOAL]
  18:00-19:00 | Estudiar cap.3 (60min) [GOAL]
  19:15-19:45 | Meditación (30min) [MIND]
  20:00-21:00 | Gym (60min) [BODY]

Tiempo total programado: 285 minutos (4.75 horas)
Tiempo total disponible: 420 minutos (7 horas)

Distribución por tipo:
  - Goals: 195 min (68.4%)
  - Mind:  30 min  (10.5%)
  - Body:  60 min  (21.1%)

Métricas:
  - Efficiency: 67.9%
  - Balance: 89.1%
  - Productivity: 76.4%
```

## 🎯 Diagrama de Priorización con Deadlines

```
                    URGENCIA DEL DEADLINE
                            ▲
                            │
                    × 3.0   │   ┌──────────────────┐
                            │   │ CRÍTICO          │
                            │   │ Vence hoy/mañana │
                    × 2.5   │   │ ┌──────────────┐ │
                            │   │ │ MUY URGENTE  │ │
                            │   │ │ Vence 2-3días│ │
                    × 2.0   │   │ │ ┌──────────┐ │ │
                            │   │ │ │ URGENTE  │ │ │
                            │   │ │ │ Esta sem.│ │ │
                    × 1.5   │   │ │ │ ┌──────┐ │ │ │
                            │   │ │ │ │NORMAL│ │ │ │
                            │   │ │ │ │2 sem.│ │ │ │
                    × 1.0   │   │ │ │ │      │ │ │ │
                            │   │ │ │ │      │ │ │ │
                            └───┴─┴─┴─┴──────┴─┴─┴─┴─►
                                GOAL    MIND    BODY
                                (3.0)   (1.5)   (1.5)
                                    TIPO DE TAREA
```

**Ejemplo de Scores:**
- Goal vence mañana: 3.0 × 3.0 × 10 = **90 puntos**
- Goal esta semana: 3.0 × 2.0 × 10 = **60 puntos**
- Mind sin deadline: 1.5 × 1.0 × 10 = **15 puntos**
- Body sin deadline: 1.5 × 1.0 × 10 = **15 puntos**

## ⏰ Timeline Visual de un Día Optimizado

```
00:00 ━━━━━━━━━━━━━━━━ SUEÑO (8h) ━━━━━━━━━━━━━━━━ 06:00
         😴 Dormir y recuperarse
                                                      
06:00 ─────────── SLOT MATUTINO (2h) ─────────── 09:00
         ⏰ Despertarse + Prepararse (1h)
         📚 GOAL: Proyecto final (90min)
         💡 Alta energía y concentración
         
09:00 ━━━━━━━━━━━━━ TRABAJO (8h) ━━━━━━━━━━━━━ 17:00
         💼 Horario laboral
         (No disponible para tareas personales)
         
17:00 ─────────── SLOT VESPERTINO (5h) ────────── 22:00
         📝 GOAL: Revisar código (45min)
         📖 GOAL: Estudiar capítulo 3 (60min)
         🧘 MIND: Meditación (30min)
         💪 BODY: Gimnasio (60min)
         🍽️  Cena + Relax (tiempo libre restante)
         
22:00 ━━━━━━━━━━━━━━━━ SUEÑO (8h) ━━━━━━━━━━━━━━━━ 00:00
         😴 Prepararse para dormir
```

## 🎨 Distribución Ideal vs Real

```
DISTRIBUCIÓN IDEAL (Objetivo del algoritmo)
═══════════════════════════════════════════

        GOALS (60%)      ████████████████████████
        MIND  (20%)      ████████
        BODY  (20%)      ████████
                         └────────────────────────┘
                         0%      50%      100%


EJEMPLO DE DISTRIBUCIÓN REAL
═══════════════════════════════════════════

Día normal:
        GOALS (68%)      ███████████████████████████
        MIND  (11%)      ████
        BODY  (21%)      ████████
                         
Desviación: +8%, -9%, +1%
Balance Score: 94/100 ✓


Día con deadline urgente:
        GOALS (85%)      ████████████████████████████████████
        MIND  (8%)       ███
        BODY  (7%)       ██
                         
Desviación: +25%, -12%, -13%
Balance Score: 67/100 ⚠️
(Justificado por urgencia)
```

## 📈 Evolución del Productivity Score

```
Productivity Score a lo largo del día:

100% │                                    ╱────
     │                              ╱────╱
 90% │                        ╱────╱
     │                  ╱────╱
 80% │            ╱────╱
     │      ╱────╱
 70% │╱────╱
     │
 60% └────┬────┬────┬────┬────┬────┬────┬────
        06:00 09:00 12:00 15:00 18:00 21:00
        
        Morning:  70% (1 tarea completada)
        Evening:  95% (todas tareas completadas)
```

## 🔄 Ciclo de Optimización Continua

```
┌────────────────────────────────────────┐
│     1. Usuario consulta horario        │
│        (optimize-day endpoint)         │
└──────────────┬─────────────────────────┘
               │
               ▼
┌────────────────────────────────────────┐
│  2. Sistema genera plan optimizado     │
│     - Calcula prioridades              │
│     - Distribuye tareas                │
│     - Muestra scores                   │
└──────────────┬─────────────────────────┘
               │
               ▼
┌────────────────────────────────────────┐
│  3. Usuario ejecuta tareas             │
│     - Consulta "tasks-now" durante día│
│     - Marca tareas como completadas    │
└──────────────┬─────────────────────────┘
               │
               ▼
┌────────────────────────────────────────┐
│  4. Sistema aprende (futuro)           │
│     - Tiempo real vs estimado          │
│     - Patrones de productividad        │
│     - Ajusta predicciones              │
└──────────────┬─────────────────────────┘
               │
               └─────► Mejora continua
```

---

**Estos diagramas complementan la documentación técnica y ayudan a visualizar el funcionamiento interno del algoritmo de optimización.**
