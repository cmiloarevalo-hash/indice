# Jurisdiction Matrix — Chile / Estados Unidos / Unión Europea / México

Fecha de corte: 2026-10-08.

## 1. Uso de esta matriz

Esta matriz es un baseline operativo para decidir en qué mercados puede activarse una acción comercial. No sustituye revisión jurídica de un caso concreto.

La regla de monetización es territorial: la empresa, el hosting o la tributación no convierten una obra protegida en reutilizable. El Convenio de Berna establece trato nacional y protección independiente; la extensión de la protección y los remedios dependen del país donde se reclama protección.

Fuente WIPO:
https://www.wipo.int/en/web/treaties/ip/berne/summary_berne

## 2. Estados operativos

AllowedMarketStatus admite:

- ALLOWED: evidencia suficiente para la acción concreta.
- ALLOWED_WITH_CONDITIONS: permitido sujeto a obligaciones registradas.
- BLOCKED: copyright/licencia impide la acción o falta un permiso necesario.
- REVIEW_REQUIRED: evidencia insuficiente o regla territorial compleja.

GeoRestrictionRequired:

- false cuando todos los mercados objetivo permiten exactamente la misma acción y condiciones compatibles;
- true cuando algún mercado está BLOCKED o REVIEW_REQUIRED mientras otro permite la acción, o cuando las condiciones territoriales difieren materialmente.

## 3. Matriz inicial

| Mercado | Baseline de duración | Obras extranjeras / reglas relevantes | AllowedMarketStatus inicial |
|---|---|---|---|
| Chile | vida del autor + 70 años; reglas especiales para colaboración, anónimas/seudónimas y otros supuestos | extranjeros no domiciliados reciben protección reconocida por convenios internacionales ratificados por Chile; no aplicar antigüedad como único criterio | REVIEW_REQUIRED hasta confirmar obra + edición |
| Estados Unidos | para obras creadas desde 1978: vida + 70; joint work: 70 desde último autor; work made for hire/anónimas/seudónimas: 95 desde publicación o 120 desde creación, lo que venza primero; pre-1978 tiene reglas históricas | formalidades/renewal históricos; URAA pudo restaurar ciertos copyrights de obras extranjeras; país de origen y fechas importan | REVIEW_REQUIRED salvo evidencia clara |
| Unión Europea | baseline armonizado: vida + 70; reglas para coautoría, anónimas/seudónimas; existen derechos especiales para ciertas primeras publicaciones de obras inéditas y posibles ediciones críticas | para ciertas obras de origen en tercer país y autor no UE, art. 7 aplica comparación de plazo: no más tarde que expiración en país de origen y no exceder plazo UE, sujeto a obligaciones internacionales | REVIEW_REQUIRED hasta evaluar origen y miembro relevante |
| México | vida del autor + 100 años; coautoría desde muerte del último; art. 29 contempla también 100 años después de divulgadas en el supuesto de su fracción II | autores/titulares extranjeros gozan de los mismos derechos que nacionales conforme a LFDA y tratados internacionales suscritos/aprobados por México | REVIEW_REQUIRED hasta confirmar obra + edición |

## 4. Chile

### 4.1 Baseline legal

Ley 17.336, artículo 10:

- protección durante toda la vida del autor;
- 70 años adicionales desde su fallecimiento.

Artículo 12:

- en colaboración, el plazo corre desde la muerte del último coautor.

Artículo 13:

- obras anónimas/seudónimas tienen reglas especiales basadas en publicación/creación.

Artículo 11:

- las obras cuyo plazo expiró pasan al patrimonio cultural común;
- su uso debe respetar paternidad e integridad.

Fuente oficial:
https://www.bcn.cl/leychile/navegar?idNorma=28933

### 4.2 Obras extranjeras

Artículo 2 de Ley 17.336:

- protege autores chilenos y extranjeros domiciliados en Chile;
- autores extranjeros no domiciliados reciben la protección reconocida por convenciones internacionales suscritas y ratificadas por Chile.

Por tanto, una obra extranjera no se clasifica por una simple comparación de año de publicación.

### 4.3 Regla operativa Chile

ALLOWED sólo si:

1. la obra subyacente es reutilizable en Chile;
2. la edición/archivo concreto es reutilizable;
3. la acción comercial específica está permitida;
4. se cumplen derechos morales/atribución aplicables;
5. no existe otra restricción contractual o de terceros detectada.

## 5. Estados Unidos

### 5.1 Obras creadas desde 1978

La Circular 15A del U.S. Copyright Office indica:

- vida del autor + 70 años;
- joint work: 70 años después de la muerte del último autor superviviente;
- work made for hire y obras anónimas/seudónimas: 95 años desde publicación o 120 desde creación, lo que expire primero, con reglas adicionales si se revela identidad.

Fuente:
https://www.copyright.gov/circs/circ15a.pdf

### 5.2 Obras pre-1978

El régimen es más complejo:

- notice y renewal históricos pueden importar;
- el máximo general para muchas obras que ya tenían protección antes de 1978 llegó a 95 años;
- la Circular 15A, revisada en abril de 2026, indica que todas las obras publicadas en Estados Unidos antes del 1 de enero de 1931 están en dominio público.

Ese dato cambia con el paso del tiempo y no debe codificarse como una regla estática sin fecha de corte.

### 5.3 Obras extranjeras y URAA

La Circular 38B explica que la URAA restauró copyright estadounidense de ciertas obras extranjeras que estaban en dominio público en EE. UU. pero seguían protegidas en su país de origen, cuando se cumplían los requisitos legales.

Consecuencia: “era dominio público por falta de formalidades estadounidenses” no es suficiente para una obra extranjera.

Fuente:
https://www.copyright.gov/circs/circ38b.pdf

Relaciones internacionales:
https://www.copyright.gov/circs/circ38a.pdf

### 5.4 Regla operativa EE. UU.

No usar una regla de año única.

Para cada edición:

1. fecha de creación;
2. fecha y lugar de primera publicación;
3. tipo de autoría;
4. formalidades/renewal si aplica;
5. posible URAA;
6. derechos de edición/derivados;
7. acción comercial.

Si alguno es incierto: REVIEW_REQUIRED.

## 6. Unión Europea

### 6.1 Baseline armonizado

Directiva 2006/116/CE, artículo 1:

- vida del autor + 70 años;
- en coautoría, desde muerte del último autor superviviente;
- anónimas/seudónimas: reglas específicas desde puesta lícita a disposición.

Artículo 8:

- los plazos se calculan desde el 1 de enero del año siguiente al hecho que los origina.

Fuente:
https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32006L0116

### 6.2 Terceros países

Artículo 7:

Para ciertas obras cuyo país de origen según Berna es un tercer país y cuyo autor no es nacional comunitario, el plazo concedido por los Estados miembros expira como máximo al expirar la protección en el país de origen y no puede superar el plazo del artículo 1, sin perjuicio de obligaciones internacionales y reglas transitorias.

### 6.3 Derechos especiales sobre publicaciones/ediciones

La Directiva contempla:

- artículo 4: hasta 25 años para primera publicación/comunicación lícita de una obra previamente inédita después de expirar copyright;
- artículo 5: los Estados miembros pueden proteger ediciones críticas/científicas de dominio público hasta 30 años.

Consecuencia: texto antiguo no implica automáticamente edición moderna libre.

### 6.4 Regla operativa UE

El status UE es baseline, no sustituto de revisar la legislación del Estado miembro cuando:

- exista derecho especial nacional;
- haya derechos morales relevantes;
- se use una edición crítica/científica;
- la transposición o reglas transitorias sean materialmente relevantes.

En esos casos usar REVIEW_REQUIRED por Estado miembro.

## 7. México

### 7.1 Baseline legal

Ley Federal del Derecho de Autor vigente, artículo 29:

- vida del autor + 100 años;
- para varios coautores, desde muerte del último;
- fracción II: 100 años después de divulgadas;
- después de los términos, la obra pasa al dominio público.

La versión oficial consultada indica última reforma DOF 14-05-2026.

Fuente:
https://www.diputados.gob.mx/LeyesBiblio/pdf/LFDA.pdf

### 7.2 Obras extranjeras

Artículo 7:

- autores/titulares extranjeros y causahabientes gozan de los mismos derechos que nacionales conforme a la ley y tratados internacionales de copyright suscritos y aprobados por México.

### 7.3 Derechos y contratos

Artículo 27 enumera derechos patrimoniales que incluyen reproducción, comunicación pública, distribución, importación y divulgación de obras derivadas.

Artículo 28 indica que esas facultades y modalidades de explotación son independientes.

Artículo 30 establece que los titulares pueden transferir derechos u otorgar licencias exclusivas o no exclusivas y exige forma escrita para actos de transmisión/licencias señalados allí.

Consecuencia operativa: una licencia para un canal no se presume aplicable a todos los demás.

### 7.4 Regla operativa México

ALLOWED sólo con:

- estatus temporal resuelto;
- obra/edición despejadas;
- acción concreta cubierta;
- tratados/estatus extranjero considerados;
- contrato/licencia suficiente cuando aplique.

## 8. Berna y country of origin

No confundir:

- país de origen de la obra;
- residencia del usuario;
- país del servidor;
- país de constitución;
- país donde se vende;
- país donde se reclama protección.

La regla operacional de Biblioteca Desktop debe modelar mercado de explotación, no sólo residencia societaria.

Fuente:
https://www.wipo.int/en/web/treaties/ip/berne/summary_berne

## 9. Algoritmo de decisión por mercado

Para cada Market:

1. identificar RightsClass global de evidencia;
2. identificar país de origen y fechas;
3. aplicar baseline de plazo del mercado;
4. aplicar regla de obra extranjera;
5. revisar edición/archivo;
6. revisar licencia contractual/abierta;
7. revisar acción concreta;
8. generar AllowedMarketStatus;
9. registrar EvidenceURLs y rationale;
10. si los mercados difieren, GeoRestrictionRequired = true.

## 10. Ejemplo sintético de georestricción

Edición X:

| Mercado | Resultado |
|---|---|
| Chile | ALLOWED |
| EE. UU. | REVIEW_REQUIRED por URAA |
| UE | ALLOWED_WITH_CONDITIONS |
| México | BLOCKED |

Resultado global:

- GeoRestrictionRequired = true;
- no ofrecer distribución global;
- habilitar sólo mercados con status permitido;
- EE. UU. permanece desactivado hasta resolver revisión;
- México permanece bloqueado.

## 11. Revalidación

Revalidar cuando:

- cambia una ley;
- se actualiza una interpretación material;
- aparece nueva evidencia;
- cambia una licencia;
- expira un contrato;
- se añade un nuevo mercado;
- se modifica la acción comercial;
- se recibe una reclamación.

La matriz debe guardar LegalBasisVersion y ReviewedAt.

## 12. Fuentes primarias/autoritativas

Berna/WIPO:
- https://www.wipo.int/en/web/treaties/ip/berne/index
- https://www.wipo.int/en/web/treaties/ip/berne/summary_berne

Chile:
- https://www.bcn.cl/leychile/navegar?idNorma=28933

Estados Unidos:
- https://www.copyright.gov/circs/circ15a.pdf
- https://www.copyright.gov/circs/circ38a.pdf
- https://www.copyright.gov/circs/circ38b.pdf
- https://www.copyright.gov/title17/

Unión Europea:
- https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32006L0116

México:
- https://www.diputados.gob.mx/LeyesBiblio/pdf/LFDA.pdf

## 13. Limitación

Esta matriz identifica controles y baselines. No declara el estatus de ninguna obra real de la colección. Esa decisión requiere evidencia por edición y mercado.
