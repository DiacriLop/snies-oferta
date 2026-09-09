# FLUJO DE CONSULTA — MÓDULO OFERTA ACADÉMICA

## 1. ¿Qué es el Módulo de Oferta Académica?

El **Módulo de Oferta Académica** permitirá consultar y analizar la información de los programas académicos registrados en el SNIES.

El usuario podrá realizar búsquedas utilizando diferentes criterios como:

- Nombre del programa.
- Departamento y municipio.
- Clasificación CINE F 2013 AC.
- Nivel de formación.
- Nivel académico.
- Sector de la institución.
- Modalidad del programa.
- Institución.

A partir de los criterios seleccionados, el sistema mostrará la información que coincida con la consulta y generará diferentes tablas para facilitar el análisis de la oferta académica.

---

# 2. ¿Cómo funcionará la consulta?

El proceso para realizar una consulta será:

```text
                 INICIO
                    │
                    ▼
          Ingresar al módulo
          Oferta Académica
                    │
                    ▼
          Seleccionar criterios
              de búsqueda
                    │
                    ▼
            Realizar consulta
                    │
                    ▼
       El sistema busca programas
       que cumplan los criterios
                    │
                    ▼
             ¿Hay resultados?
              /           \
            NO             SÍ
            │               │
            ▼               ▼
     Mostrar mensaje     Mostrar
     sin resultados      resultados
                            │
                            ▼
                     Consultar tablas
                            │
                            ▼
                     Exportar información
```

---

# 3. Paso 1 — Realizar una búsqueda

El usuario podrá buscar programas académicos mediante palabras clave.

La búsqueda se realizará sobre el **nombre del programa**.

Por ejemplo:

```text
Ingeniería Ambiental
```

También podrá utilizar operadores para realizar búsquedas más específicas:

```text
Ingeniería AND Ambiental
```

```text
Ingeniería OR Ambiental
```

```text
(Ingeniería OR Ambiental) AND Sostenibilidad
```

Esto permitirá realizar búsquedas sencillas o combinadas dependiendo de la necesidad del usuario.

---

# 4. Paso 2 — Filtrar por ubicación

El usuario podrá limitar la búsqueda a una ubicación determinada.

### Departamento

Podrá seleccionar un departamento, por ejemplo:

```text
Valle del Cauca
```

### Municipio

Después podrá seleccionar un municipio asociado al departamento.

Por ejemplo:

```text
Departamento: Valle del Cauca
Municipio: Tuluá
```

Si el usuario no desea limitar la búsqueda por ubicación, podrá dejar la opción:

```text
Todos
```

---

# 5. Paso 3 — Filtrar por clasificación CINE

El sistema permitirá consultar los programas utilizando la clasificación **CINE F 2013 AC**.

La clasificación estará organizada jerárquicamente:

```text
Campo amplio
      ↓
Campo específico
      ↓
Campo detallado
```

Esto permitirá comenzar con una categoría general y, si se desea, ir aumentando el nivel de detalle.

Por ejemplo:

```text
Campo amplio
      ↓
Campo específico
      ↓
Campo detallado
```

El usuario podrá utilizar solamente el campo amplio o profundizar hasta el campo detallado.

---

# 6. Paso 4 — Filtrar por clasificación académica

El usuario podrá seleccionar:

### Nivel de formación

Por ejemplo:

```text
Pregrado
Especialización
Maestría
Doctorado
```

### Nivel académico

Este filtro permitirá complementar la búsqueda utilizando la clasificación académica disponible en los datos.

Ambos criterios podrán utilizarse individualmente o combinados.

---

# 7. Paso 5 — Filtrar por características de la oferta

El usuario podrá especificar características particulares de los programas.

### Sector

```text
Oficial
Privado
```

### Modalidad

Por ejemplo:

```text
Presencial
Presencial Virtual
Virtual
A Distancia Virtual
```

### Institución

Podrá seleccionar una institución específica para consultar únicamente sus programas.

---

# 8. Paso 6 — Combinar criterios

Los diferentes criterios podrán utilizarse simultáneamente.

Por ejemplo, el usuario podría realizar una consulta como:

```text
Búsqueda:
Ingeniería AND Ambiental

Departamento:
Valle del Cauca

Nivel de formación:
Maestría

Sector:
Oficial

Modalidad:
Presencial
```

El sistema mostrará únicamente los programas que cumplan con los criterios seleccionados.

Esto permitirá pasar de una búsqueda general a una consulta mucho más específica.

---

# 9. Paso 7 — Consultar los resultados

Después de realizar la consulta, el sistema mostrará los resultados encontrados.

Si existen registros que coincidan con los criterios, el usuario podrá consultar diferentes formas de presentar la información.

El módulo contará con tres resultados principales:

```text
┌───────────────────────────────────────┐
│ T01 — Tabla General de Oferta         │
├───────────────────────────────────────┤
│ T02 — Clasificación de las Maestrías  │
├───────────────────────────────────────┤
│ T03 — Oferta específica del Valle     │
│      del Cauca                        │
└───────────────────────────────────────┘
```

---

# 10. T01 — Tabla General de Oferta

Esta tabla permitirá obtener una **visión general de la oferta académica**.

La información se organizará teniendo en cuenta:

- Nivel de formación.
- Sector.
- Modalidad.

Además, permitirá conocer:

- Cantidad de programas.
- Cantidad de instituciones.
- Cantidad de municipios.
- Cantidad de departamentos.

Por ejemplo, el usuario podrá identificar cómo se distribuyen las maestrías y doctorados entre instituciones oficiales y privadas y según la modalidad de estudio.

---

# 11. T02 — Clasificación de las Maestrías

Esta tabla permitirá analizar específicamente las **maestrías**.

El sistema identificará la clasificación disponible en los datos:

```text
Maestría de investigación
Maestría de profundización
```

También permitirá analizar su distribución según:

- Sector.
- Modalidad.
- Cantidad de programas.
- Instituciones.
- Municipios.
- Departamentos.

Los registros de maestrías que no tengan información de clasificación serán tratados como **sin clasificación**, sin asignarles una categoría que no esté registrada en los datos.

---

# 12. T03 — Oferta específica del Valle del Cauca

Esta tabla permitirá consultar de manera detallada los programas ofrecidos en:

```text
Valle del Cauca
```

A diferencia de las tablas anteriores, esta será una vista **detallada de los programas**.

El usuario podrá consultar información como:

- Sector.
- Institución.
- Código SNIES del programa.
- Nombre del programa.
- Modalidad.
- Municipio.
- Reconocimiento del Ministerio.
- Fecha de resolución.
- Número de periodos de duración.
- Periodicidad.
- Número de créditos.

Esto permitirá revisar individualmente los programas que conforman la oferta académica del departamento.

---

# 13. ¿Qué ocurre si no se encuentran resultados?

Si los criterios seleccionados no coinciden con ningún programa, el sistema informará al usuario.

Por ejemplo:

```text
No se encontraron programas que coincidan
con los criterios de búsqueda seleccionados.
```

El usuario podrá modificar los filtros y realizar una nueva consulta.

---

# 14. Limpiar la consulta

El usuario contará con una opción:

```text
LIMPIAR
```

Esta opción permitirá eliminar los criterios seleccionados y regresar la consulta a su estado inicial.

De esta manera, el usuario podrá comenzar una nueva búsqueda sin tener que modificar cada filtro manualmente.

---

# 15. Exportar resultados

Una vez realizada la consulta, el usuario podrá exportar la información para utilizarla posteriormente.

La aplicación permitirá generar un archivo Excel con los resultados obtenidos.

El archivo podrá contener:

```text
Resultados de la consulta
Tabla General de Oferta
Clasificación de las Maestrías
Oferta del Valle del Cauca
```

Esto permitirá continuar el análisis de la información fuera de la aplicación.

---

# 16. Condición de información mostrada

Para garantizar que la consulta utilice información vigente dentro del conjunto de datos proporcionado, el sistema mostrará únicamente:

```text
Instituciones ACTIVAS
        +
Programas ACTIVOS
```

Esta condición será aplicada automáticamente y no necesitará ser configurada por el usuario.

---

# 17. Ejemplo de uso completo

Un usuario necesita encontrar las maestrías presenciales del sector oficial relacionadas con ingeniería ambiental en el Valle del Cauca.

Realizaría:

### 1. Búsqueda

```text
Ingeniería AND Ambiental
```

### 2. Ubicación

```text
Departamento: Valle del Cauca
```

### 3. Nivel de formación

```text
Maestría
```

### 4. Sector

```text
Oficial
```

### 5. Modalidad

```text
Presencial
```

### 6. Buscar

El sistema procesa los criterios y muestra los programas que coinciden.

### 7. Analizar

El usuario puede consultar:

```text
T01 → Resumen general
T02 → Clasificación de las maestrías
T03 → Detalle de la oferta del Valle del Cauca
```

### 8. Exportar

Finalmente puede generar un archivo Excel con la información obtenida.

---

# 18. Resumen del funcionamiento

En términos simples, el usuario podrá:

```text
       BUSCAR
          │
          ▼
   ELEGIR FILTROS
          │
          ▼
       CONSULTAR
          │
          ▼
   VER RESULTADOS
          │
     ┌────┼────┐
     ▼    ▼    ▼
    T01  T02  T03
     │    │    │
     └────┼────┘
          ▼
       ANALIZAR
          │
          ▼
       EXPORTAR
```

El propósito del módulo es facilitar la **consulta, exploración y análisis de la oferta académica**, permitiendo al usuario pasar de una búsqueda general a resultados específicos mediante la combinación de diferentes criterios.