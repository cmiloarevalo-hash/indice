# Biblioteca Desktop — Requisitos V1

## 1. Propósito y alcance

Biblioteca Desktop V1 será una aplicación local de escritorio para Windows destinada a navegar y buscar el catálogo de una biblioteca documental sin modificar el corpus original.

El corpus objetivo de referencia es:

`D:\Camilo\1. Respaldo\libroesoterico.com`

El repositorio de código y el corpus son recursos separados. V1 debe tratar el corpus como **READ-ONLY**.

## 2. Fuente de datos inicial

V1 reutilizará el índice ya aceptado en:

`D:\Camilo\1. Respaldo\_library_directory_index_v1`

El índice disponible contiene, entre otros, estos campos por documento:

- `Name`
- `Extension`
- `SizeBytes`
- `RelativePath`
- `DirectoryRelativePath`

La aplicación no requiere OCR, extracción de texto, análisis semántico ni lectura completa de los documentos para construir la experiencia V1.

## 3. Requisitos funcionales

### RF-01 — Aplicación de escritorio Windows

La aplicación debe ejecutarse como aplicación local de escritorio en Windows.

### RF-02 — Operación offline

Las funciones nucleares de navegación, búsqueda, filtrado y apertura deben funcionar sin conexión a Internet.

### RF-03 — Distribución portable futura

La aplicación debe poder publicarse en una fase posterior como aplicación portable/autoejecutable para Windows, sin exigir un instalador como condición para su uso.

### RF-04 — Ubicación futura junto al corpus

La distribución futura debe admitir un modo en que la aplicación se encuentre junto al corpus documental o en un directorio padre/sibling predecible, conservando la resolución portable de rutas.

Este requisito no autoriza copiar ni publicar la aplicación en el corpus durante este Work Item.

### RF-05 — Navegación del catálogo

La aplicación debe permitir recorrer el catálogo por directorio lógico usando los datos del índice, sin reordenar físicamente archivos o carpetas.

### RF-06 — Búsqueda

La aplicación debe permitir búsqueda textual al menos sobre:

- nombre del documento;
- ruta relativa;
- directorio relativo.

La búsqueda V1 es sobre metadatos del catálogo, no sobre el contenido de los documentos.

### RF-07 — Filtros iniciales

La aplicación debe permitir filtros basados únicamente en datos ya presentes en el índice. Como mínimo:

- extensión;
- directorio;
- tamaño del archivo.

Los filtros deben poder combinarse con la búsqueda textual.

### RF-08 — Abrir documento

Desde un registro del catálogo, el usuario debe poder abrir el documento seleccionado mediante la aplicación asociada por Windows para esa extensión.

Antes de abrir, la aplicación debe comprobar que la ruta resuelta existe y corresponde a un archivo.

### RF-09 — Abrir directorio original

Desde un registro del catálogo, el usuario debe poder abrir en el Explorador de Windows el directorio original que contiene el documento.

### RF-10 — Rutas relativas

El catálogo debe conservar rutas relativas cuando sea aplicable. La aplicación debe resolverlas en tiempo de ejecución contra una raíz de corpus determinada por configuración o por el layout portable.

No se deben convertir los registros del catálogo a rutas absolutas dependientes de una sola máquina como representación canónica.

### RF-11 — Corpus READ-ONLY

La aplicación no debe escribir en los documentos ni en sus directorios como parte de las funciones V1.

Las operaciones permitidas sobre el corpus son de lectura de metadatos necesarios para localizar/verificar archivos y la invocación de Windows para abrirlos.

### RF-12 — Sin reorganización física

V1 no debe mover, renombrar, eliminar ni reordenar físicamente documentos o directorios del corpus.

La organización que presente la UI es lógica y deriva del catálogo.

### RF-13 — Archivo faltante o ruta obsoleta

Si un documento indexado no existe en la ruta resuelta:

- la aplicación no debe buscarlo ni moverlo automáticamente;
- debe informar que el elemento no está disponible en la ubicación indexada;
- debe impedir la apertura de una ruta inexistente;
- puede mantener el registro visible para que la discrepancia sea observable.

Una actualización/reindexación del catálogo será una operación explícita de un Work Item posterior.

## 4. Requisitos no funcionales

### RNF-01 — Portabilidad

La solución debe minimizar dependencias externas en la máquina destino y permitir una publicación autocontenida para Windows.

### RNF-02 — Simplicidad operativa

V1 debe funcionar con el catálogo local y el sistema de archivos local sin servidores, servicios de red o servicios de pago.

### RNF-03 — Rendimiento objetivo

El diseño debe soportar cómodamente el índice aceptado actual, que contiene 28.781 documentos, sin requerir un motor de búsqueda externo.

La búsqueda y los filtros deben responder de forma interactiva sobre el catálogo cargado localmente.

### RNF-04 — Determinismo de rutas

La misma combinación de raíz de corpus y `RelativePath` debe resolver siempre a la misma ruta normalizada.

Las rutas resueltas deben validarse para impedir que un registro escape de la raíz de corpus mediante segmentos relativos inesperados.

### RNF-05 — Tolerancia a inconsistencias

Un archivo faltante, inaccesible o movido no debe provocar el cierre de la aplicación completa. El error debe quedar limitado al registro/operación afectado.

### RNF-06 — Frontera de escritura

El proceso normal de navegación y búsqueda no debe escribir dentro de la raíz del corpus.

Si V1 necesita preferencias de usuario o estado efímero, dichos datos deben almacenarse fuera del corpus, en un directorio de datos de aplicación del usuario definido por la arquitectura.

### RNF-07 — Privacidad y offline

La aplicación no debe enviar nombres de archivos, rutas o datos del catálogo a servicios externos para las funciones V1.

## 5. Fuera de alcance de V1

Quedan fuera de alcance salvo autorización posterior explícita:

- OCR;
- indexación de texto completo;
- búsqueda semántica;
- análisis del contenido de libros;
- edición de metadatos dentro del corpus;
- mover, renombrar o eliminar documentos;
- sincronización cloud;
- cuentas de usuario;
- servidor web;
- servicios remotos;
- instalador;
- auto-update;
- publicación o release;
- CI;
- base de datos obligatoria;
- clasificación automática del contenido.

## 6. Criterios de aceptación del producto V1

La futura implementación V1 se considerará funcionalmente verificable cuando, usando un catálogo de prueba o el índice autorizado en modo read-only, se pueda demostrar que:

1. inicia sin Internet;
2. carga el catálogo local;
3. navega por directorios lógicos;
4. busca por nombre/ruta;
5. filtra por extensión, directorio y tamaño;
6. resuelve rutas relativas contra una raíz configurada;
7. abre un archivo existente mediante la asociación de Windows;
8. abre su directorio contenedor;
9. informa correctamente un archivo faltante;
10. no modifica el corpus durante esas operaciones.
