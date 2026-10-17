# Biblioteca Desktop — Estrategia de monetización responsable

Fecha de corte jurídico de este marco: 2026-10-08.

## 1. Propósito y regla de decisión

Este documento define una estrategia para maximizar el valor económico de la biblioteca sin asumir derechos inexistentes. Es un marco comercial y operativo. No autoriza venta, publicación, redistribución, contacto con titulares, pago de licencias, constitución de sociedad ni despliegue comercial.

La unidad de decisión es siempre:

obra subyacente + edición/archivo concreto + mercado + acción comercial.

Una obra subyacente en dominio público no vuelve automáticamente reutilizable una traducción, prólogo, notas, ilustraciones, portada, maquetación o edición digital moderna.

La clasificación de Work Item #10 es el contrato de entrada:

- A_COMMERCIAL_REUSE_CONFIRMED: obra y edición/archivo concreto permiten reutilización comercial con evidencia suficiente.
- B_COMMERCIAL_WITH_CONDITIONS: reutilización comercial permitida, pero con condiciones.
- C_NONCOMMERCIAL_ONLY: existe licencia o permiso que excluye uso comercial.
- D_RIGHTS_RESERVED_OR_PERMISSION_REQUIRED: se necesita autorización o licencia comercial.
- E_UNCERTAIN_MANUAL_REVIEW: evidencia insuficiente, contradictoria o ambigua.

Regla maestra: ausencia de evidencia no equivale a permiso.

## 2. Principios jurídicos y operativos

### 2.1 Protección territorial

El Convenio de Berna se apoya en trato nacional, protección automática e independencia de protección. La extensión de la protección y los remedios dependen del país donde se reclama protección. Por tanto, país de constitución, facturación, hosting o tributación no sustituye el análisis por mercado.

Consecuencia operativa: cada edición debe tener AllowedMarketStatus separado para Chile, Estados Unidos, Unión Europea y México, y GeoRestrictionRequired cuando los resultados no sean equivalentes.

Fuente primaria/autoritativa:
- WIPO, Convenio de Berna y resumen oficial: https://www.wipo.int/en/web/treaties/ip/berne/summary_berne
- WIPO, Convenio de Berna: https://www.wipo.int/en/web/treaties/ip/berne/index

### 2.2 Derechos de obra y derechos de edición

La monetización directa sólo puede habilitarse cuando estén resueltos ambos niveles:

1. obra subyacente;
2. edición/archivo concreto.

Debe revisarse, cuando aplique, traducción, adaptación, prólogo, notas, ilustraciones, fotografías, portada, selección/compilación, diseño y otros aportes protegibles.

### 2.3 Fallar cerrado

Cualquier explotación directa se bloquea cuando:

- falta evidencia suficiente;
- la licencia expira;
- aparece evidencia contradictoria;
- el mercado no está evaluado;
- se recibe un takedown o disputa material;
- no se puede cumplir una obligación de atribución, ShareAlike o NoDerivatives;
- no está claro que el licenciante controle el derecho concreto solicitado.

## 3. Dos carriles de negocio

### Carril 1 — explotación directa de A/B

Aplica sólo a A y B, y sólo en mercados habilitados.

Productos potenciales:

- descarga o venta de una edición válida;
- membresía con acceso a archivos válidamente licenciados;
- colecciones temáticas;
- bundles;
- impresión bajo demanda cuando la edición concreta y el acuerdo aplicable lo permitan;
- ediciones propias construidas desde material libre sin copiar aportes protegidos de una edición ajena;
- investigación, análisis computacional o IA sólo si licencia, derechos del material y mercado permiten el uso concreto.

La clasificación A/B no debe traducirse como “libre de derechos”. Debe traducirse como acciones concretas permitidas y obligaciones concretas.

### Carril 2 — valor sin redistribución + adquisición selectiva de derechos

Aplica principalmente a C, D y E.

Modelos permitidos como estrategia futura:

- catálogo y metadata propios;
- descubrimiento y curación;
- bibliografías y colecciones temáticas sin adjuntar copias restringidas;
- membresía Pro del software;
- software que opera sobre colecciones locales del usuario;
- research-as-a-service sin entregar copias restringidas;
- enlaces a titular, editorial o distribuidor autorizado;
- afiliación cuando exista un programa válido;
- generación de señal de demanda;
- solicitud futura de licencia comercial;
- partnership y revenue share;
- incorporación prioritaria de obras de dominio público o licencias comerciales verificadas.

## 4. Estrategia por RightsClass

| Clase | Redistribución comercial del archivo | Estrategia principal | Estado por defecto |
|---|---|---|---|
| A | Sí, sólo en mercados verificados | venta, membresía, bundles, POD si procede | habilitable |
| B | Sí, cumpliendo condiciones | mismos modelos que A con controles de licencia | habilitable con condiciones |
| C | No bajo licencia NC | software, catálogo, discovery, enlaces, afiliación válida, re-licencia | bloqueado para archivo |
| D | No hasta licencia | clearance, licencia no exclusiva, royalty, revenue share | bloqueado |
| E | No | investigación y resolución de evidencia | bloqueado |

### 4.1 Clase A

Secuencia recomendada:

1. confirmar evidencia de obra y edición;
2. confirmar mercado;
3. definir CommercialActionsAllowed;
4. verificar derechos adicionales relevantes;
5. calcular valor esperado;
6. lanzar primero productos reversibles y de baja complejidad;
7. medir demanda antes de ampliar formatos.

### 4.2 Clase B y Creative Commons

Baseline operacional para licencias CC 4.0:

| Licencia | Comercial | Adaptación distribuible | Operación |
|---|---:|---:|---|
| CC BY | Sí | Sí | atribución, enlace a licencia, indicar cambios |
| CC BY-SA | Sí | Sí | BY + ShareAlike para adaptación |
| CC BY-ND | Sí | No | distribuir sólo material no adaptado; atribuir |
| CC BY-NC | No | Sí, sólo no comercial | excluir de explotación comercial salvo permiso separado |
| CC BY-NC-SA | No | Sí, sólo no comercial | NC + SA |
| CC BY-NC-ND | No | No | NC + ND |

Fuentes oficiales:
- CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
- CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/
- CC BY-ND 4.0: https://creativecommons.org/licenses/by-nd/4.0/
- CC BY-NC 4.0: https://creativecommons.org/licenses/by-nc/4.0/
- licencias CC: https://creativecommons.org/share-your-work/use-remix/cc-licenses/

La licencia exacta, su versión y la evidencia de que cubre la edición concreta deben quedar registradas. Las licencias CC no resuelven por sí solas derechos de terceros no controlados por el licenciante.

### 4.3 Clase C

No vender ni redistribuir comercialmente el archivo bajo una licencia NC.

Alternativas legítimas de monetización:

- catálogo/metadata propios;
- software Pro;
- discovery y curación;
- bibliografías;
- enlaces autorizados;
- afiliación válida;
- servicio sobre archivos que el usuario ya posee;
- medición agregada de demanda;
- solicitud de licencia comercial independiente.

### 4.4 Clase D

Tratar D como pipeline de adquisición, no como inventario vendible.

Priorizar cuando coincidan:

- demanda alta;
- titular identificable;
- derechos solicitados claros;
- coste de negociación razonable;
- cobertura territorial atractiva;
- posibilidad de agrupar títulos;
- margen suficiente después de royalty/licencia.

### 4.5 Clase E

Cola de investigación estricta. No habilitar descarga, venta, membresía sobre el archivo, POD ni derivados comerciales.

Orden de investigación:

1. identidad de obra y edición;
2. autor/coautores;
3. fecha y país de publicación;
4. traductor/editor/ilustrador/prologuista;
5. aviso de copyright o licencia;
6. país de origen;
7. titular y cadena de título;
8. estatus por mercado;
9. reclasificación sólo con evidencia.

## 5. Cuatro modelos de negocio

### Modelo 1 — Biblioteca Desktop Pro

Propuesta de valor: búsqueda, filtros, listas, organización y descubrimiento sobre colecciones locales del usuario.

Clientes: coleccionistas, investigadores, lectores especializados, archivos personales.

Derechos requeridos: software y assets propios; metadata propia o autorizada. No depende de redistribuir libros del usuario.

Ingresos: licencia de software, suscripción Pro, upgrades o soporte premium.

Costes: desarrollo, soporte, pagos, marketing y distribución.

Riesgo jurídico: bajo a medio si se evita redistribuir archivos, portadas o extractos restringidos.

Complejidad: baja a media.

Dependencia del corpus: baja.

### Modelo 2 — Colecciones digitales rights-cleared

Propuesta de valor: bundles temáticos con procedencia, licencia y atribución transparentes.

Clientes: lectores especializados e investigadores.

Derechos requeridos: A/B habilitados en cada mercado.

Ingresos: venta unitaria, bundles, membresía.

Costes: rights QA, metadata, atribución, hosting, pagos y soporte.

Riesgo jurídico: medio.

Complejidad: media.

Dependencia del corpus: media/alta sobre el subconjunto A/B.

### Modelo 3 — Partnerships con titulares

Propuesta de valor: transformar D de alta demanda en ediciones autorizadas mediante distribución, discovery y analytics agregados.

Clientes: lectores; titular/editor como socio.

Derechos requeridos: licencia expresa para los derechos y territorios concretos.

Ingresos: venta, suscripción atribuible, revenue share.

Costes: negociación, mínimo garantizado si existe, royalty, reporting y compliance.

Riesgo jurídico: medio si la cadena de título es sólida; alto si no lo es.

Complejidad: alta.

Dependencia del corpus: selectiva.

### Modelo 4 — Research y bibliografías sin copias

Propuesta de valor: investigación bibliográfica, mapas de autores/temas y dossiers sin entregar copias restringidas.

Clientes: investigadores, editoriales, creadores y lectores avanzados.

Derechos requeridos: derechos sobre entregables propios y permisos/excepciones aplicables a cualquier material de terceros realmente incorporado.

Ingresos: informes, suscripción o encargos.

Costes: investigación, QA y soporte.

Riesgo jurídico: bajo a medio según contenido del entregable.

Complejidad: media.

Dependencia del corpus: media para discovery, baja para distribución.

## 6. Maximización de cobertura

Orden recomendado:

1. monetizar primero software/discovery, que no requiere redistribuir todo el corpus;
2. habilitar A/B por mercado;
3. usar demanda observada para ordenar D;
4. negociar grupos de títulos por titular;
5. incorporar nuevas fuentes de dominio público y licencias comerciales;
6. ampliar jurisdicciones sólo cuando exista matriz de derechos y georestricción operativa.

KPIs futuros:

- ARPU de software;
- porcentaje del catálogo con evidencia suficiente;
- porcentaje A/B por mercado;
- coste medio de clearance;
- conversión D → licenciado;
- margen por título/licencia;
- tiempo de respuesta a takedown;
- número de títulos bloqueados por evidencia expirada.

## 7. Controles antes de monetizar un archivo

Ningún archivo se habilita sin:

- RightsClass;
- evidencia de obra subyacente;
- evidencia de edición/archivo;
- AllowedMarketStatus;
- CommercialActionsAllowed;
- RequiredAttribution;
- RequiredLicense cuando aplique;
- versión/fecha de evidencia;
- GeoRestrictionRequired;
- ausencia de hold o takedown.

La metadata completa y los resultados de derechos deben seguir la arquitectura privada de Work Item #10. El repositorio público de la aplicación no debe convertirse en depósito de libros ni del catálogo completo.

## 8. Qué no hacer

- vender PDFs sólo porque están disponibles en Internet;
- tratar Internet Archive, Google Books, Scribd, PDFDrive o mirrors como prueba de licencia comercial;
- asumir que dominio público del texto libera una traducción o edición moderna;
- usar una licencia NC para explotar comercialmente el material licenciado;
- distribuir una adaptación de material ND sin permiso separado;
- aplicar una sola regla de plazo a todos los países;
- ignorar reglas históricas o restauración de copyright de obras extranjeras en EE. UU.;
- asumir que una sociedad de gestión colectiva controla un derecho digital sin verificar repertorio y mandato;
- constituir o facturar desde otro país como supuesto bypass de copyright;
- habilitar A/B en mercados no evaluados;
- dejar una obra activa cuando expira la licencia o desaparece la evidencia.

## 9. Hechos legales vs hipótesis comerciales

Hechos jurídicos soportados por fuentes primarias/autoritativas:

- territorialidad y trato nacional de Berna;
- duración y reglas especiales por jurisdicción;
- tratamiento oficial de las licencias Creative Commons;
- necesidad de autorización para derechos exclusivos salvo licencia, dominio público o excepción aplicable.

Hipótesis comerciales a validar posteriormente:

- precios;
- conversión;
- demanda;
- CAC/LTV;
- coste de clearance;
- royalty óptimo;
- revenue share;
- tamaño de bundles;
- ranking económico de títulos.

## 10. Fuentes jurídicas principales

- WIPO — Convenio de Berna: https://www.wipo.int/en/web/treaties/ip/berne/index
- WIPO — resumen oficial de Berna: https://www.wipo.int/en/web/treaties/ip/berne/summary_berne
- Chile — Ley 17.336: https://www.bcn.cl/leychile/navegar?idNorma=28933
- U.S. Copyright Office — Circular 15A: https://www.copyright.gov/circs/circ15a.pdf
- U.S. Copyright Office — Circular 38A: https://www.copyright.gov/circs/circ38a.pdf
- U.S. Copyright Office — Circular 38B: https://www.copyright.gov/circs/circ38b.pdf
- UE — Directiva 2006/116/CE: https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32006L0116
- México — Ley Federal del Derecho de Autor: https://www.diputados.gob.mx/LeyesBiblio/pdf/LFDA.pdf
- Creative Commons — licencias: https://creativecommons.org/licenses/

## 11. Limitación

Este marco no sustituye revisión jurídica de una explotación concreta. Antes de activar un mercado deben verificarse edición, país de origen, titularidad, plazo, licencias, derechos derivados, derechos morales y reglas transitorias o contractuales aplicables.
