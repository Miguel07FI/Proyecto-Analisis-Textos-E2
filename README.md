# Sistema Inteligente de Auditoría de Odio Web (SADOW)

Este proyecto implementa una arquitectura híbrida basada en Aprendizaje Profundo (*Deep Learning*) para la detección semántica de discurso de odio y hostilidad dirigida dentro de tablones de comentarios en plataformas web. El sistema integra el procesamiento de texto mediante una Red Neuronal Convolucional Unidimensional (CNN 1D) con la cuantificación matemática de la densidad de un léxico peyorativo especializado, permitiendo la generación automatizada de informes ejecutivos en formato PDF con métricas analíticas y representaciones gráficas en tiempo real.

---

## 👥 Integrantes del Equipo de Desarrollo

* **Miguel Ángel Hernandez Ramirez**
* miguelhernandez0532@gmail.com
* **Pérez Del Angel Joaquín Eduardo**
* eduardodelangel17@outlook.com
* **[Nombre Tercer Integrante] [Apellido]** 

---

## 🛠️ Requisitos del Entorno

Asegúrese de contar con los siguientes componentes de infraestructura antes de iniciar el despliegue:

* **Python**: Versión 3.11.x (Obligatorio)
* **Sistema Operativo**: Windows 10/11, macOS o Linux.
* **Administrador de Paquetes**: `pip` actualizado.

---

## 🚀 Guía de Despliegue Secuencial

Siga estrictamente los siguientes pasos desde su terminal para inicializar el sistema en su máquina local.

### 1. Clonar el Repositorio y Acceder al Directorio

```bash
git clone https://github.com/TuUsuario/Proyecto-Analisis-Textos-E2.git
cd Proyecto-Analisis-Textos-E2
```

### 2. Configurar el Soporte de Rutas Largas (Solo Windows)

Si implementa el sistema en un entorno Windows, debe remover el límite histórico de 260 caracteres para evitar fallos en el enlazado binario de las librerías nativas de TensorFlow:

1. Haga clic en el menú de inicio de Windows o use el buscador de la barra de tareas.
2. Escriba **PowerShell** en el cuadro de búsqueda.
3. Localice el acceso directo de **Windows PowerShell**, haga clic derecho sobre él y seleccione **Ejecutar como Administrador**.
4. Copie y pegue el siguiente comando algebraico de registro dentro de la consola:

```powershell
New-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

5. Presione **Enter** para aplicar los cambios en el sistema operativo.
6. Reinicie su entorno de desarrollo, como VS Code o la terminal activa, para asegurar que la nueva directiva de rutas sea asimilada.

### 3. Instalar las Dependencias del Sistema

Instale los paquetes y módulos de control especificados en el manifiesto del proyecto:

```bash
pip install -r requirements.txt
```

---

## 🔑 Configuración de las Credenciales de Google Cloud (API Key)

Para habilitar el consumo y la extracción de flujos de datos en vivo desde la plataforma de YouTube, es obligatorio parametrizar una clave de acceso API válida:

1. Ingrese a la consola de desarrolladores de Google: [Google Cloud Console](https://console.cloud.google.com/).
2. Instancie un nuevo proyecto de software y diríjase a la sección **API y Servicios > Biblioteca**.
3. Busque y habilite el servicio denominado **YouTube Data API v3**.
4. Acceda a la pestaña **Credenciales**, seleccione **Crear credenciales** y elija la opción **Clave de API (API Key)**.
5. Abra el archivo interno `config.py` en su editor de texto y actualice la constante global con el string alfanumérico generado:

```python
YOUTUBE_API_KEY = "SU_CLAVE_ALFANUMÉRICA_REAL_AQUÍ"
```

---

## 🎮 Flujo de Ejecución del Software

El pipeline de procesamiento se ejecuta de manera secuencial a través de la interfaz de comandos (CLI).

### Paso A: Inicialización del Dataset Sintético

Genere el corpus balanceado de 12,000 instancias binarias con inyección de ruido estructural:

```bash
python descargar_data.py
```

### Paso B: Ajuste Jerárquico del Modelo (Entrenamiento)

Ejecute la optimización del gradiente para calibrar los pesos de los *Word Embeddings* y los filtros convolucionales 1D. Este proceso generará de forma automática el archivo nativo de Keras en la carpeta `models/`:

```bash
python train_nn.py
```

### Paso C: Extracción de Métricas de Control

Evalúe la capacidad de generalización de la arquitectura sobre el conjunto de validación ciego del 20%. Este paso exportará los diagramas estáticos de matriz de confusión y curva de pérdida a la carpeta `outputs/`:

```bash
python evaluar_modelo.py
```

### Paso D: Ejecución y Orquestación Central

Inicie el panel interactivo del sistema para evaluar registros sintéticos locales o auditar un enlace web en vivo consumiendo el flujo distribuido de YouTube:

```bash
python main.py
```
## 🖥️ Operación de la Interfaz Gráfica (Dashboard SADOW)

Al ejecutar el orquestador principal del sistema (`python main.py`), se desplegará una interfaz gráfica de usuario (GUI) automatizada de alta fidelidad, diseñada bajo los estándares estéticos institucionales de la UNAM. 

Para activar el motor de inferencia profunda, siga las instrucciones de uso:

1. **Inserción del Recurso Web (Input):** Localice el campo de texto superior titulado *"Inserte la URL del video de YouTube a auditar"*. Copie la dirección web completa de cualquier video desde la barra de su navegador (por ejemplo: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`) y péguela en el contenedor.
2. **Procesamiento de Flujos Disgregados:** Haga clic en el botón **"INICIAR AUDITORÍA E INFERENCIA"**. 
3. **Mapeo y Ejecución Asíncrona:** * El sistema aislará de forma sintáctica el identificador único del video (`video_id`) y se conectará de manera directa al protocolo API de Google para realizar la extracción de datos en vivo.
   * La interfaz iniciará una barra de progreso indeterminada. Gracias a la concurrencia multihilo del sistema (`threading`), la ventana permanecerá completamente reactiva y fluida mientras la **Red Neuronal Convolucional (CNN 1D)** procesa los comentarios en segundo plano.
4. **Resultados e Indicadores de Control:** Al finalizar la tokenización y la evaluación de tensores, la GUI actualizará de forma dinámica su cuadro de mando (KPIs cuantitativos) y emitirá un veredicto visual inmediato (Verde para entornos seguros o Rojo para ataques de odio coordinados), compilando en simultáneo el reporte formal de auditoría en la carpeta de salidas\
5. Al final, si todo es correcto el sistema imprimira un mensaje de proceso exitoso y se generaran las graficas y reporte de analsis final en la carprta de outputs del poryecto
