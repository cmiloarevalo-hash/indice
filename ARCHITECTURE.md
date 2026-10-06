# Biblioteca Desktop — Arquitectura V1

## 1. Objetivo de arquitectura

La arquitectura V1 prioriza:

- aplicación Windows local y offline;
- superficie técnica pequeña;
- reutilización del índice existente;
- resolución portable de rutas;
- acceso estrictamente read-only al corpus;
- posibilidad de publicación futura como ejecutable autocontenido.

No se implementa código, base de datos, empaquetado ni UI en este Work Item.

## 2. Runtime y toolkit seleccionados

### Selección

- Lenguaje: **C#**
- Runtime: **.NET 10 LTS**
- UI desktop: **Windows Forms (WinForms)**
- Destino inicial de publicación futura: **Windows x64**
- Modelo de publicación previsto: **self-contained, single-file**

### Justificación

.NET 10 es la versión LTS activa y ofrece soporte prolongado. WinForms es una tecnología .NET específica para aplicaciones de escritorio Windows y proporciona controles suficientes para una interfaz de catálogo basada en búsqueda, filtros y una grilla/listado.

La publicación single-file de .NET permite empaquetar una aplicación autocontenida para un runtime objetivo de Windows, reduciendo la dependencia de un runtime previamente instalado.

### Alternativas consideradas

**WPF** también es una opción .NET adecuada para escritorio Windows, pero introduce una capa de UI más amplia de la necesaria para el primer prototipo. V1 requiere principalmente búsqueda, filtros, navegación y listado tabular, por lo que WinForms mantiene menor complejidad inicial.

**Tauri/Electron** no se seleccionan para V1 porque añadirían toolchains y/o runtimes web adicionales para una aplicación exclusivamente Windows y offline. No existe un requisito actual que justifique esa complejidad.

La selección podrá revisarse mediante un Work Item posterior si una necesidad concreta de UI o distribución lo exige.

## 3. Componentes lógicos

La implementación futura se dividirá en tres fronteras principales.

### 3.1 UI

Responsabilidades:

- presentar búsqueda y filtros;
- mostrar resultados y navegación por directorios;
- mostrar estado de disponibilidad de cada registro;
- disparar las acciones «Abrir documento» y «Abrir directorio»;
- mostrar errores recuperables al usuario.

La UI no accede directamente al corpus mediante lógica ad hoc; consume servicios de catálogo y resolución de rutas.

### 3.2 Catálogo e indexación

Responsabilidades:

- cargar el snapshot local del catálogo;
- parsear y validar registros;
- ofrecer búsqueda, filtros, ordenamiento y agrupación;
- mantener los datos del catálogo separados de la UI;
- exponer el registro seleccionado y sus rutas relativas.

V1 no necesita generar OCR ni leer el contenido de los documentos.

La actualización/reindexación del catálogo no forma parte de la primera implementación funcional salvo Work Item posterior que la autorice.

### 3.3 Acceso read-only al corpus

Responsabilidades:

- resolver una ruta relativa contra la raíz de corpus;
- normalizar y validar que la ruta resultante permanezca dentro de la raíz;
- comprobar existencia y tipo de archivo/directorio;
- solicitar a Windows la apertura del archivo con su aplicación asociada;
- solicitar a Windows la apertura del directorio correspondiente.

Esta capa no expone operaciones de escritura, borrado, renombre o movimiento.

## 4. Estrategia de almacenamiento local del catálogo

### 4.1 Fuente inicial

El índice aceptado existente contiene:

- `books_index.csv`
- `directories_index.csv`
- `extension_totals.csv`

Para V1, esos CSV constituyen la fuente de importación inicial. El archivo principal por documento dispone de:

- `Name`
- `Extension`
- `SizeBytes`
- `RelativePath`
- `DirectoryRelativePath`

El índice aceptado contiene actualmente 28.781 registros de libros/documentos. Ese volumen permite cargar el catálogo en memoria sin introducir una base de datos obligatoria.

### 4.2 Representación V1

La estrategia V1 es:

1. mantener un snapshot CSV local del catálogo como artefacto de datos de la aplicación;
2. abrirlo en modo lectura al iniciar;
3. parsearlo a objetos en memoria;
4. ejecutar búsqueda, filtros y ordenamiento sobre esa colección;
5. no modificar el CSV como consecuencia de navegar o abrir documentos.

No se adopta SQLite en V1 porque el volumen y las consultas requeridas no justifican todavía una dependencia y una capa de persistencia adicionales. Si futuras mediciones muestran una necesidad real de indexación avanzada o actualizaciones transaccionales, esa decisión se revisará explícitamente.

## 5. Layout portable y resolución de rutas

### 5.1 Regla canónica

`RelativePath` se interpreta siempre como ruta relativa a la **raíz del corpus**, no al directorio del proceso ni al working directory actual.

Conceptualmente:

`absoluteDocumentPath = Normalize(corpusRoot + RelativePath)`

`absoluteDirectoryPath = Normalize(corpusRoot + DirectoryRelativePath)`

### 5.2 Determinación de la raíz

La implementación futura debe soportar dos modos:

1. **Modo portable colocated:** detectar una raíz de corpus en una ubicación conocida relativa a `AppContext.BaseDirectory`.
2. **Modo configurado:** permitir seleccionar explícitamente la raíz del corpus cuando no se encuentre en el layout esperado.

La selección persistida, si existe, debe guardarse fuera del corpus en datos de usuario.

### 5.3 Validación de seguridad e integridad

Antes de acceder a una ruta:

1. combinar raíz + ruta relativa;
2. obtener la ruta absoluta normalizada;
3. comprobar que permanezca bajo la raíz normalizada del corpus;
4. rechazar registros que escapen de la raíz;
5. comprobar existencia antes de abrir.

No se seguirá una ruta arbitraria fuera del corpus debido a segmentos `..` u otras formas de traversal presentes en datos corruptos.

## 6. Apertura de documentos y directorios

### Documento

La capa de acceso solicitará a Windows abrir la ruta del documento utilizando la asociación registrada del sistema operativo.

Si el archivo no existe, la acción se cancela y la UI informa el estado.

### Directorio

La capa de acceso abrirá el directorio resuelto en el Explorador de Windows.

No es necesario que la aplicación modifique atributos, permisos o contenido para realizar estas acciones.

## 7. Archivo faltante o cambio de ruta

Cuando un registro del catálogo apunte a una ruta inexistente:

- el registro permanece visible;
- se marca o reporta como no disponible;
- «Abrir documento» no intenta una búsqueda global ni una reparación automática;
- la aplicación no mueve ni renombra nada;
- el usuario puede seguir navegando el resto del catálogo.

Un archivo movido se considera «ruta indexada obsoleta». La corrección del catálogo se realizará mediante un proceso explícito de refresh/reindex autorizado en un Work Item posterior.

Opcionalmente, una verificación futura podrá comparar `SizeBytes` contra el tamaño actual como señal de cambio, pero V1 no debe leer el contenido completo para detectar modificaciones.

## 8. Fronteras de escritura

### Dentro del corpus

**Prohibido escribir** como parte de V1.

La aplicación no debe:

- editar documentos;
- crear sidecars dentro de carpetas del corpus;
- renombrar;
- mover;
- eliminar;
- reordenar;
- escribir cachés o logs allí.

### Fuera del corpus

Si se requiere persistencia de preferencias, la ubicación prevista es:

`%LOCALAPPDATA%\BibliotecaDesktop\`

Ejemplos permitidos para una implementación posterior:

- preferencia de raíz de corpus;
- tamaño/posición de ventana;
- filtros recientes;
- logs diagnósticos limitados.

El snapshot de catálogo distribuido con la aplicación se trata como read-only durante navegación normal.

## 9. Reutilización del índice existente

La aplicación no volverá a analizar el contenido de los documentos para arrancar V1.

El pipeline previsto es:

1. recibir/copiar como artefacto de aplicación un snapshot derivado del índice aceptado;
2. validar encabezados y tipos esperados;
3. cargar `books_index.csv`;
4. usar `directories_index.csv` y `extension_totals.csv` cuando aporten navegación o conteos sin recalcularlos;
5. resolver las rutas relativas sólo al momento de verificar/abrir.

La procedencia del catálogo debe poder trazarse al índice aceptado, pero el ejecutable no necesita acceso permanente al directorio de trabajo del inventario original.

## 10. Estrategia de empaquetado

La publicación futura prevista será:

- Release;
- runtime target `win-x64`;
- self-contained;
- single-file;
- sin instalador obligatorio.

La salida de publicación será un artefacto de build, no un archivo versionado en el repositorio.

La configuración exacta de publish se definirá y verificará en el Work Item de implementación/empaquetado correspondiente.

## 11. Estrategia mínima de pruebas

### 11.1 Pruebas unitarias

Como mínimo:

- parseo de filas válidas e inválidas del catálogo;
- búsqueda textual;
- filtros por extensión/directorio/tamaño;
- combinación de filtros;
- normalización de rutas;
- rechazo de traversal fuera de la raíz;
- comportamiento con ruta faltante.

### 11.2 Pruebas de integración

Usar un árbol temporal de archivos de prueba, no el corpus real, para validar:

- resolución de rutas relativas;
- detección de archivo/directorio existente;
- detección de faltantes;
- frontera read-only.

### 11.3 Verificación manual

Sobre una fuente autorizada read-only:

- arranque offline;
- carga del catálogo;
- navegación;
- búsqueda;
- filtros;
- apertura de archivo mediante asociación del sistema;
- apertura de directorio;
- mensaje de faltante;
- confirmación de que el corpus no cambia.

### 11.4 Verificación de artefacto portable

En el Work Item de empaquetado:

- ejecutar el artefacto publicado en una máquina/entorno Windows compatible sin depender de un runtime .NET previamente instalado;
- confirmar que el catálogo y las rutas relativas funcionen con el layout previsto;
- confirmar que no escriba en el corpus durante uso normal.

## 12. Dependencias y servicios

V1 no requiere:

- servidor;
- servicio cloud;
- cuenta;
- navegador embebido;
- motor de búsqueda externo;
- base de datos obligatoria;
- OCR;
- IA;
- acceso a Internet durante uso normal.

Cualquier dependencia futura debe responder a una necesidad demostrada y estar autorizada por un Work Item específico.

## 13. Fuentes técnicas de la decisión

Documentación oficial consultada para fijar la arquitectura:

- .NET support policy: https://dotnet.microsoft.com/en-us/platform/support/policy
- Windows Forms documentation: https://learn.microsoft.com/dotnet/desktop/winforms/
- .NET single-file deployment: https://learn.microsoft.com/dotnet/core/deploying/single-file/overview
- .NET application publishing overview: https://learn.microsoft.com/dotnet/core/deploying/

Estas referencias sustentan la selección del runtime/UI y la viabilidad del modelo self-contained single-file. No forman parte de una dependencia online en tiempo de ejecución.
