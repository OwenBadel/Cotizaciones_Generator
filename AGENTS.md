# 🤖 Directiva Agéntica: Cotizaciones & Cuentas de Cobro TI

---
project_id: "PROJ_013"
project_name: "Cotizaciones_Generator"
absolute_disk_path: "d:/Proyectos/LemonFabrica/Fabrica_Software/projects/Cotizaciones Generator"
okf_project_node: "[[Proyectos/PROJ_013_Cotizaciones_Generator|PROJ-013: Cotizaciones Generator]]"
architecture_node: "[[Decisiones de Arquitectura/ARQ_clean_architecture_hexagonal_architecture|ARQ Clean Architecture]]"
mcp_server_entrypoint: "d:/Proyectos/LemonFabrica/Fabrica_Software/mcp/server.py"
status: "active"
created_at: "2026-09-27T17:40:00-05:00"
github_repo: "https://github.com/OwenBadel/Cotizaciones_Generator.git"
---

## 🎯 1. Identidad y Autoría
Este proyecto es diseñado y desarrollado bajo la titularidad y dirección de **Owen Badel Hooker** (Ingeniero de Sistemas / Software Architect).
Directorio local en disco duro:
`d:/Proyectos/LemonFabrica/Fabrica_Software/projects/Cotizaciones Generator`

### Roles Operativos en este Proyecto:
1. **Orquestador (ROL-001):** Supervisa la estructura modular y desacoplada de la aplicación.
2. **Desarrollador (ROL-004):** Garantiza 0 código espagueti y separación estricta entre GUI, modelos, plantillas y servicios.
3. **Evaluador / QA (ROL-005):** Audita estándares, robustez de cálculos monetarios y cobertura de pruebas.
4. **Documentador (ROL-006):** Mantiene la bitácora (`README.md`), docstrings y notas OKF en español.
5. **Tester (ROL-007):** Ejecuta la suite de pruebas unitarias (`tests/`).

---

## 🧭 2. Enrutamiento Determinista al Cerebro OKF (Cero Reinvención)
Antes de proponer o codificar, el agente debe consultar el árbol de conocimiento:

| Si necesitas... | Acude al Árbol de Conocimiento | Acción Obligatoria |
| :--- | :--- | :--- |
| **Modelos de Diseño y Arquitectura** | `vault/Decisiones de Arquitectura/` | Aplicar Clean Architecture y desacoplamiento. |
| **Generación de Reportes y Documentos** | `vault/Técnicas/` | ReportLab, QtWebEngine, HTML a PDF. |
| **Manipulación de Hojas de Cálculo** | `vault/Python/` | OpenPyXL para exportación estilizada a Excel. |
| **Resolución de Errores y Bugs** | `vault/Errores y Soluciones/` | Documentar soluciones en `ERR_XXX.md`. |

---

## 🏛️ 3. Marco Arquitectónico y Estándares
Este proyecto implementa:
* **Arquitectura:** Clean Architecture modular desacoplada:
  - `core/`: Modelos fuertemente tipados (`ItemCotizacion`, `DatosCotizacion`, `DatosCuentaCobro`), conversión de números a letras en pesos colombianos y persistencia atómica.
  - `templates/`: Plantillas HTML/CSS puras para Cotizaciones y Cuentas de Cobro.
  - `services/`: Renderizado vectorial a PDF con `QWebEngineView` y exportación a Excel con `openpyxl`.
  - `ui/`: Interfaz moderna PyQt5 con paleta oscura/azul corporativa y hojas de estilo QSS.
  - `tests/`: Suite unitaria automatizada.
* **Estándar de Memoria:** [[Plantillas/ESPECIFICACION_OKF|Estándar OKF v1.0.0]]

---

## 📦 4. Dependencias Autorizadas
- **PyQt5 & PyQtWebEngine:** Runtime gráfico y motor de renderizado PDF.
- **openpyxl:** Generación de libros de cálculo `.xlsx`.
- **unittest:** Validación de cobertura y cálculos.

---

## 🚦 5. Protocolo de Ejecución y Calidad
1. **Bloqueo Inmediato:** Prohibido realizar commits si la suite de pruebas unitarias (`python -m unittest discover -s tests`) falla.
2. **Cero Código Espagueti:** Prohibido mezclar maquetación HTML o lógica de cálculo dentro de los controladores de eventos de la GUI.
3. **Persistencia Segura:** Escritura atómica de `config.json` para evitar corrupción de datos.

---

## 🚀 6. Repositorio Git Individual y Commits Autónomos a GitHub
* **Aislamiento Total:** Este proyecto posee su propio repositorio Git con remoto `https://github.com/OwenBadel/Cotizaciones_Generator.git`.
* **Creación Desatendida con `gh` CLI:** `gh repo create Cotizaciones_Generator --public --source=. --push`.
* **Commits en Español:** Commits semánticos en español (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`).
