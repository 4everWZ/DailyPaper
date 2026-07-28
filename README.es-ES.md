# DailyPaper - Herramienta de Resumen Automático de Literatura

![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

¡Resume automáticamente los últimos artículos de los campos de AI/ML/CV/NLP cada día, ahorrando tu tiempo de búsqueda!

## 🎯 Características

- ✨ **Actualización Automática**: Extrae automáticamente los artículos más recientes a diario.
- 📚 **Agregación Multi-fuente**: Soporta múltiples fuentes de datos como ArXiv, conferencias principales, revistas, etc.
- 🔍 **Clasificación Inteligente**: Clasificación automática por campo (CV, NLP, ML, etc.).
- 🎨 **Presentación Estética**: Diseño web responsivo con soporte para búsqueda y filtrado.
- 🔗 **Acceso Rápido**: Enlaces directos al texto original de los artículos.

## 📖 Fuentes de Datos Soportadas

- **ArXiv**: Categorías como cs.AI, cs.CV, cs.CL, cs.LG, entre otras.
- **Conferencias**: NeurIPS, ICML, CVPR, ICCV, ECCV, ACL, EMNLP, etc.
- **Revistas**: Nature, Science, PAMI, JMLR, etc.

## 🚀 Inicio Rápido

### Ejecución Local

```bash
# Clonar el proyecto
git clone https://github.com/4everWZ/DailyPaper.git
cd DailyPaper

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el crawler
python scripts/fetch_papers.py

# Generar página web
python scripts/generate_html.py
```

### Despliegue en GitHub Pages

**Despliegue Rápido (Recomendado):**
```powershell
# Ejecutar script de despliegue en un clic
.\deploy.ps1
```

**Despliegue Manual:**
1. Crear un nuevo repositorio en GitHub (llamado `DailyPaper`, Público).
2. Empujar el código a GitHub.
3. En Settings > Pages, configurar: Source = rama `gh-pages`.
4. En Settings > Actions > General, configurar permisos: Read and write.
5. Ejecutar manualmente "Update Papers Daily" en Actions.
6. Acceder a `https://4everWZ.github.io/DailyPaper/`.

**Para pasos detallados, consulta: [DEPLOYMENT.md](DEPLOYMENT.md)**

## 📁 Estructura del Proyecto

```
DailyPaper/
├── .github/
│   └── workflows/
│       └── update-papers.yml    # Script de automatización de GitHub Actions
├── scripts/
│   ├── fetch_papers.py          # Script de extracción de artículos
│   ├── generate_html.py         # Generador de página estática
│   └── utils.py                 # Funciones de utilidad
├── data/
│   └── papers.json              # Almacenamiento de datos de artículos
├── docs/                        # Archivos fuente de GitHub Pages
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── requirements.txt
└── README.md
```

## ⚙️ Configuración

Edita el archivo `config.yaml` para personalizar:

```yaml
# Configuración de extracción
sources:
  arxiv:
    enabled: true
    categories: ['cs.AI', 'cs.CV', 'cs.CL', 'cs.LG']
    max_results: 50
  
# Frecuencia de actualización
schedule: "0 0 * * *"  # Diariamente a las 0:00 UTC

# Palabras clave por dominio
keywords:
  CV: ['computer vision', 'image', 'video', 'detection', 'segmentation']
  NLP: ['natural language', 'language model', 'transformer', 'nlp']
  ML: ['machine learning', 'deep learning', 'neural network']
```

## 📊 Origen de los Datos

- [ArXiv](https://arxiv.org/) - Repositorio de preprints de acceso abierto.

## 🤝 Contribuciones

¡Las Issues y Pull Requests son bienvenidas!

## 📄 Licencia

Licencia MIT

## 🙏 Agradecimientos

¡Gracias a todos los proveedores de datos abiertos y contribuyentes!

## ⭐ Star History

Si este proyecto te ha sido útil, por favor danos una estrella ⭐️
