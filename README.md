# MeteoCórdoba: Proyecto Intermodular

## Integrante(s)
* **Rafael Ruiz Álvarez**

---

## Descripción del problema
La agricultura moderna en la provincia de Córdoba se enfrenta al gran desafío de optimizar los recursos hídricos ante condiciones de sequía y variabilidad climática extrema. Para afrontar esto, se despliegan redes de sensores en el suelo (nodos IoT) encargados de medir variables críticas del ecosistema. 

Sin embargo, estos dispositivos sufren problemas reales en el entorno de campo: fallos de alimentación por falta de insolación, degradación de la batería, pérdidas de conectividad o descalibración de lecturas. El problema radica en la necesidad de transformar un conjunto masivo de datos crudos e imperfectos en un sistema analítico robusto que automatice las alertas críticas de mantenimiento y emplee algoritmos predictivos para anticipar los niveles de humedad hídrica, asegurando la continuidad operativa del hardware y la salud del cultivo.

---

## Variables analizadas
A lo largo de la práctica se aíslan y tratan de forma estadística las siguientes variables clave:
* **Fecha / Hora:** Eje temporal transformado al formato nativo `datetime` para organizar cronológicamente la serie.
* **Humedad media global (`humedad_media_global`):** Variable crítica que representa el porcentaje de agua presente en el suelo del cultivo.
* **Temperatura promedio global (`temperatura_promedio_global`):** Medición térmica del suelo (°C) indispensable para evaluar la evapotranspiración.
* **Batería (`bateria_v`):** Voltaje residual de la batería de litio del dispositivo (V), monitorizada para prevenir el cese de lecturas.
* **Panel solar (`panel_solar_v`):** Voltaje fotovoltaico generado (V), clave para evaluar si el panel recibe suficiente luz solar diurna.
* **Predicciones de alertas de la IA:** Campos generados mediante el modelo predictivo que anticipan el estado hídrico y energético en el horizonte futuro ($t+1$).

---

## Instrucciones para ejecutar el análisis
1. **Clonar o descargar** los archivos del proyecto en una carpeta local que contenga el dataset original y el archivo del cuaderno `practica_intermodular.ipynb`.
2. **Instalar los requisitos de analítica:** En este caso, la manera más accesible es instalando el entorno de Python Anaconda, el cúal contiene todo tipo de librerías relacionadas con el análisis de datos.
3. **Ejecutar el Notebook:** Inicia Jupyter Lab, abre `practica_intermodular.ipynb` y ejecuta las celdas de forma secuencial (Run All Cells). Esto mostrará el fragmento crudo, cargará el csv con los nombres corregidos y filtrará los datos, generará los gráficos y finalmente generará los CSV finales con sus respectivas alertas y predicciones calculadas.

---

## URL del hosteo
https://rafarual04.pythonanywhere.com/

---

## URL del Github del proyecto
https://github.com/rafarual04/MeteoCordoba

---

## Enlace al vídeo
https://youtu.be/bt4_CgTHPGs

---

## Usuario de prueba
Usuario: admin

Contraseña: admin

Este usuario te dará privilegios de admin (panel adminitrativo de Djando y el CRUD de los registros). Si quieres uno normal, puedes probar a *registrarte*.

---

## Principales conclusiones
Una iniciativa así puede ser muy útil en el día a día de los agricultores de Córdoba, ya que saber con antelación las condiciones climáticas aproximadas te da un margen muy valioso a la hora de planificar las siguientes cosechas.

No solo eso, sino que en una situación real, todos salen ganando porque los agricultores reciben datos mientras que los programadores son empleados en el proyecto.

---

## Limitaciones
La única limitación que he notado ha sido el tiempo (en mi caso, es que soy una sola persona) y que solo nos dieron los datos desde 2024 hasta abril de este año. Estoy seguro que con más datos nos podría haber salido un modelo aún más completo.

---

## Mejoras futuras
- **Mejorar la responsividad de la página web**: está bastante bien, pero por ejemplo la tabla no se ve del todo bien en dispositivos móviles.
- **Añadir la opcion de importar tus propios CSV**: Esto fue algo que pregunté en clase y me dejaron hacerlo precargando los datos, pero es cierto que pudiendo cargar datos desde la propia web el proceso de añadirlos sería menos manual.
- **Mejorar CSS de la página**: Aunque es verdad que la estética minimalista no está mal (encima con un logo que yo mismo he diseñado), es cierto que todavía tengo margen para darle una identidad visual más única y no tan "del montón"
