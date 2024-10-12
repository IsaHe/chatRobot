# RoboChat Automation Script

Este proyecto automatiza la interacción con chatbots como ChatGPT y Copilot utilizando Selenium y el framework de Robocorp. El script `tasks.py` permite abrir un navegador, enviar un prompt a un chatbot y guardar la respuesta en un archivo PDF.

## Requisitos

- Python 3.x
- Google Chrome
- ChromeDriver
- Robocorp
- Selenium
- RPA Framework

## Instalación

1. **Clonar el repositorio:**

    ```sh
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2. **Instalar las dependencias:**

    - VS code las instalara por ti usando `conda.yaml`

3. **Configurar el entorno:**

    Asegúrate de que `CHROME_PATH` y `CHROME_DRIVER_PATH` en `tasks.py` apuntan a las ubicaciones correctas de Google Chrome y ChromeDriver en tu sistema.

## Uso

1. **Configurar el archivo de entrada:**

    Coloca el archivo que deseas adjuntar en la carpeta `output` y asegúrate de que `PATH_TO_ATATCHMENT_FILE` en `tasks.py` apunta a este archivo.

2. **Ejecutar el script:**

    - En VS code con el teclado abrir la paleta de comandos (macOS: Shift-Command-P, Windows / Linux: Ctrl+Shift+P)
    - Escribe `run robot` y selecciona `Robocorp: Create Task Package (Robot)`

3. **Seleccionar el chatbot:**

    El script está configurado para usar ChatGPT por defecto. Si deseas usar Copilot, cambia la variable `chatbot` a `"copilot"` en `tasks.py`.

4. **Ver la respuesta:**

    La respuesta del chatbot se guardará en un archivo PDF en la carpeta `output` con el nombre `Respuesta.pdf`.

## Funciones Principales

### `openChat()`

Esta función principal configura el navegador, prepara el prompt y envía el prompt al chatbot seleccionado. Luego guarda la respuesta en un archivo PDF.

### `preparePromt(prompt)`

Prepara el prompt añadiendo el contenido del archivo adjunto si existe.

### `copilot(prompt)`

Envía el prompt a Copilot y devuelve la respuesta.

### `chatgpt(prompt)`

Envía el prompt a ChatGPT utilizando un navegador Chrome en modo depuración.

### `abrirChrome(url, prompt)`

Abre Chrome en modo depuración, envía el prompt y obtiene la respuesta.

### `inicializarWebDriver(puerto)`

Inicializa el WebDriver de Chrome.

### `obtenerCookie(driver)`

Obtiene la cookie de sesión de autenticación.

### `enviarPrompt(driver, prompt)`

Envía el prompt al chatbot.

### `esperarQueRespuestaTermine(driver)`

Espera a que el chatbot termine de generar la respuesta.

### `obtenerRespuesta(driver)`

Obtiene la respuesta del chatbot.

## Notas

- **Soporte para Windows:** Actualmente, el soporte para Windows no está implementado.
- **Framework:** Utiliza el framework de Robocorp para comunicarse con el chatbot.

## Licencia

Este proyecto está licenciado bajo los términos de la licencia Apache-2.0. Consulta el archivo [LICENSE](LICENSE) para más detalles.