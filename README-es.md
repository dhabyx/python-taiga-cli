# Taiga CLI

`taiga-cli` es una herramienta de línea de comandos (CLI) diseñada para interactuar con una instancia de **Taiga**, una plataforma de gestión de proyectos ágil. Esta CLI permite a los usuarios gestionar configuraciones, proyectos, sprints e historias de usuario de manera eficiente y rápida desde la terminal.

---

## **Instalación**

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/dhabyx/python-taiga-cli.git
   cd taiga-cli
   ```

2. **Instalar la herramienta**:
   Usa `pip` para instalar el proyecto como una aplicación CLI global:
   ```bash
   pip install .
   ```

   Esto instalará la herramienta y configurará el comando `taiga` para ejecutarse desde cualquier ubicación en tu terminal.

3. **Verifica la instalación**:
   ```bash
   taiga --help
   ```

   Si ves el menú de ayuda, ¡todo está listo!

4. **Actualizar la herramienta**:
   Si realizas cambios locales o deseas actualizar desde el repositorio, puedes reinstalar:
   ```bash
   pip install --upgrade .
   ```

5. **Desinstalar la herramienta**:
   Si necesitas eliminar la CLI, usa:
   ```bash
   pip uninstall taiga-cli
   ```
---

## **Comandos**

### **1. Configuración (`config`)**
Configura el servidor y las credenciales del usuario.

```bash
taiga config
```

Sigue las instrucciones interactivas para configurar el servidor Taiga y las credenciales de usuario.

---

### **2. Iniciar sesión (`login`)**
Autentícate en tu instancia de Taiga.

```bash
taiga login
```

---

### **3. Gestión de Proyectos (`project`)**

- **Listar proyectos propios**:
  ```bash
  taiga project ls
  ```

- **Listar todos los proyectos**:
  ```bash
  taiga project ls --all
  ```

- **Mostrar proyecto por defecto**:
  ```bash
  taiga project default
  ```

- **Configurar un proyecto como predeterminado**:
  ```bash
  taiga project set-default <project-slug>
  ```

---

### **4. Gestión de Sprints (`sprint`)**

- **Listar sprints del proyecto por defecto**:
  ```bash
  taiga sprint ls
  ```

- **Listar sprints de un proyecto específico**:
  ```bash
  taiga sprint ls --project=<project-slug>
  ```

- **Ver estadísticas del usuario en un sprint**:
  ```bash
  taiga sprint user-stats
  ```

- **Ver estadísticas de un usuario específico**:
  ```bash
  taiga sprint user-stats --user=<username>
  ```

- **Ver estadísticas de todos los usuarios**:
  ```bash
  taiga sprint user-stats --all-users
  ```

- **Ver estadísticas de un proyecto específico**:
  ```bash
  taiga sprint user-stats --project=<project-slug>
  ```

- **Ver estadísticas de un sprint específico**:
  ```bash
  taiga sprint user-stats --sprint=<sprint-slug>
  ```

- **Listar historias de usuario de un sprint**:
  ```bash
  taiga sprint user-stories
  ```

- **Listar historias de un usuario específico**:
  ```bash
  taiga sprint user-stories --user=<username>
  ```

- **Listar historias de todos los usuarios**:
  ```bash
  taiga sprint user-stories --all-users
  ```

---

### **5. Gestión de Historias de Usuario (`stories`)**

- **Listar historias propias**:
  ```bash
  taiga stories ls
  ```

- **Listar historias de todos los sprints**:
  ```bash
  taiga stories ls --all-sprints
  ```

- **Filtrar historias por usuario**:
  ```bash
  taiga stories ls --user=<username>
  ```

- **Filtrar historias por estado**:
  ```bash
  taiga stories ls --status=open
  taiga stories ls --status=closed
  ```

- **Filtrar historias por sprint**:
  ```bash
  taiga stories ls --sprint=<sprint-slug>
  ```

- **Filtrar historias de un proyecto específico**:
  ```bash
  taiga sprint user-stats --project=<project-slug>
  ``` 
  
### **6. Gestión de Configuración**

`taiga-cli` almacena su configuración en un archivo en el sistema del usuario. Esta configuración incluye detalles 
como el servidor Taiga, las credenciales de usuario y los valores predeterminados para proyectos y sprints.

---

#### **Ubicación del Archivo de Configuración**
El archivo de configuración se encuentra en la siguiente ubicación, dependiendo del sistema operativo:

- **Linux**:
  ```bash
  ~/.config/taiga-cli/config.json
  ```

- **macOS**:
  ```bash
  ~/Library/Application Support/taiga-cli/config.json
  ```

- **Windows**:
  (No se ha diseñado explícitamente para Windows, pero podrías adaptarlo).

---

#### **Limpiar la Configuración**
Si deseas borrar toda la configuración almacenada y reiniciar la herramienta:

1. **Eliminar el archivo de configuración**:
   - En Linux:
     ```bash
     rm ~/.config/taiga-cli/config.json
     ```
   - En macOS:
     ```bash
     rm ~/Library/Application\\ Support/taiga-cli/config.json
     ```

2. **Crear nuevamente la configuración**:
   Después de eliminar el archivo, al ejecutar `taiga config`, se te pedirá ingresar los detalles nuevamente:
   ```bash
   taiga config
   ```

---

#### **Precaución**
Eliminar este archivo de configuración:
- Restablecerá el servidor, las credenciales y cualquier valor predeterminado configurado.
- No afecta los datos almacenados en la instancia de Taiga que estás utilizando.

---

## **Ayuda**
Para ver todas las opciones y comandos disponibles:
```bash
taiga --help
```

Para un comando específico:
```bash
taiga <command> --help
```

---

## **Contribuciones**
1. **Bifurca (Fork) este repositorio.**
2. **Crea una nueva rama:**
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```

3. **Realiza cambios y haz un commit:**
   ```bash
   git commit -m "Añadir nueva funcionalidad"
   ```

4. **Haz un push y abre un Pull Request.**

---

## **Licencia**
`taiga-cli` está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más información.
