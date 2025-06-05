# 📁 `/pages` – Módulos funcionales del sistema de Firma Digital

Esta carpeta contiene las interfaces específicas de cada rol dentro del sistema de firma digital del DIF. Cada archivo representa una vista distinta accesible desde la interfaz principal (`main.py`) de la aplicación.

---

## 📄 Archivos en `/pages`

### 🔐 `dif_admin.py` – Administrador del DIF
- **Función:** Permite al administrador generar claves RSA (256 bits) para los funcionarios autorizados del DIF.
- **Entradas:**
  - Nombre del funcionario.
- **Salidas:**
  - Clave pública y módulo guardados en `users_keys.csv`.
  - Clave privada mostrada al administrador para ser compartida de forma segura.
- **Uso esperado:** Solo el administrador del DIF debe acceder a esta vista.

---

### ✍️ `dif.py` – Firma de documentos (Funcionario del DIF)
- **Función:** Permite firmar digitalmente un archivo PDF.
- **Entradas:**
  - PDF a firmar.
  - Clave privada del funcionario.
- **Proceso:**
  1. Se extrae el texto del PDF.
  2. Se genera un hash SHA-256 del contenido.
  3. Se firma el hash utilizando RSA con la clave privada (`firma = hash^d mod N`).
- **Salidas:**
  - Archivo `.sig` con la firma digital.

---

### 🧾 `rc.py` – Verificación de firma (Registro Civil)
- **Función:** Valida si un PDF fue firmado por un funcionario autorizado.
- **Entradas:**
  - Archivo PDF.
  - Archivo `.sig`.
  - Nombre del firmante.
- **Proceso:**
  1. Busca la clave pública correspondiente en `users_keys.csv`.
  2. Genera el hash del PDF.
  3. Verifica si `firma^e mod N == hash`.
- **Resultado:**
  - Muestra si la firma es válida o no.

---

## 📌 Nota

Estas interfaces se integran automáticamente con Streamlit a través del sistema de multipágina. No requieren ejecución directa, solo deben estar dentro de esta carpeta y ser importadas mediante `streamlit run main.py`.

---
