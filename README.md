<div align="center">
  <h1>🔐 SIGAL - Sistema de Gestión de Acceso a Laboratorios 🔐</h1>
  <p>Aplicación para gestionar y registrar el acceso de estudiantes y personal a laboratorios universitarios, desarrollada con <strong>Python</strong>, <strong>Tkinter</strong> y <strong>MongoDB Atlas</strong>.</p>

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-3776AB)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white)

</div>

## 🌟 **Bienvenido**

**SIGAL** permite registrar entradas y salidas en laboratorios universitarios mediante una interfaz gráfica. Administra roles, permisos y horarios de acceso, garantizando seguridad y trazabilidad del uso de los espacios.

## 📂 **Módulos Principales**

| Módulo                      | Descripción                                                       |
| --------------------------- | ----------------------------------------------------------------- |
| **Inicio de sesión**        | Inicio de sesión y autenticación por roles.                       |
| **Registro de Acceso**      | Permite registrar entradas y salidas de usuarios autorizados.     |
| **Gestión de Usuarios**     | Alta, baja y modificación de usuarios con asignación de permisos. |
| **Gestión de Laboratorios** | Administración de laboratorios y horarios permitidos.             |
| **Historial de Accesos**    | Consulta de entradas/salidas por usuario, fecha y laboratorio.    |

## 🚀 **Instalación y Configuración**

### 🛠️ **Requisitos Previos**

- **Python 3.11** – Descargar e instalar desde: [Python](https://www.python.org/downloads/).
- **MongoDB Atlas** – Crear cuenta gratuita desde: [mongodb.com/cloud](https://www.mongodb.com/cloud/atlas).

### 📥 **Instalación**

1. **Clonar el repositorio:**

```bash
  git clone https://github.com/Eddys912/sigal.git
```

2. **Acceder al proyecto:**

```bash
  cd sigal
```

3. **Crear y activar un entorno virtual:**

```bash
  python -m venv venv
  source venv/bin/activate   # En Windows
```

4. **Instalar dependecias:**

```bash
  pip install -r requirements.txt
```

5. **Configurar variables de entorno:**
   - Renombra el archivo `.env.example` a `.env` y configurar.
6. **Ejecutar la aplicación:**

```bash
  python main.py
```

## 🚀 Cómo Contribuir?

1. **Realizar un Fork** del proyecto haciendo clic en el botón `Fork`.
2. **Realizar los pasos de instalación.**
3. **Realiza tus cambios**:
   - Guarda los archivos.
   - Crea un commit con una descripción clara:
     ```bash
     git add .
     git commit -m "Descripción de los cambios realizados"
     ```
4. **Envíar los cambios** a tu repositorio fork:
   ```bash
   git push origin mi-nueva-funcionalidad
   ```
5. **Abre un Pull Request** 🚀:
   - Dirígete al repositorio original y crea un **Pull Request**.
   - Describe los cambios realizados.
