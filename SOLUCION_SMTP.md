# Solución: Error DNS con smtp.ensenachile.cl

## Problema
El servidor `smtp.ensenachile.cl` no existe o no se puede resolver por DNS.

## Soluciones

### Opción 1: Usar Gmail (Recomendado - Más Fácil)

1. Crea una cuenta Gmail para la aplicación (ej: `tutorias.ensenachile@gmail.com`)
2. Activa verificación en 2 pasos
3. Genera App Password
4. Configura en Render:

```
SMTP_SERVER = smtp.gmail.com
SMTP_PORT = 587
SMTP_USER = tutorias.ensenachile@gmail.com
SMTP_PASSWORD = [App Password de Gmail]
FRONTEND_URL = https://app-tutorias.onrender.com
```

### Opción 2: Usar Outlook/Hotmail

1. Crea cuenta Outlook
2. Configura en Render:

```
SMTP_SERVER = smtp-mail.outlook.com
SMTP_PORT = 587
SMTP_USER = tutorias@outlook.com
SMTP_PASSWORD = [tu contraseña]
FRONTEND_URL = https://app-tutorias.onrender.com
```

### Opción 3: Preguntar al Administrador de ensenachile.cl

Si necesitas usar el correo de ensenachile.cl, pregunta al administrador:

1. **¿Cuál es el servidor SMTP?**
   - Puede ser: `mail.ensenachile.cl`, `smtp.ensenachile.cl`, o otro
   - O puede usar Gmail/Outlook empresarial

2. **¿Qué puerto usa?**
   - Generalmente 587 (STARTTLS) o 465 (SSL)

3. **¿Necesita autenticación especial?**
   - Algunos servidores requieren configuración adicional

## Configuración Rápida con Gmail

### Paso 1: Crear cuenta Gmail
1. Ve a: https://accounts.google.com/signup
2. Crea: `tutorias.ensenachile@gmail.com` (o el nombre que prefieras)

### Paso 2: Activar App Password
1. Ve a: https://myaccount.google.com/security
2. Activa "Verificación en 2 pasos"
3. Ve a "Contraseñas de aplicaciones"
4. Genera nueva contraseña para "Correo"
5. Copia la contraseña de 16 caracteres

### Paso 3: Configurar en Render
En Environment Variables del Environment Group:

```
SMTP_SERVER = smtp.gmail.com
SMTP_PORT = 587
SMTP_USER = tutorias.ensenachile@gmail.com
SMTP_PASSWORD = abcd efgh ijkl mnop
FRONTEND_URL = https://app-tutorias.onrender.com
```

### Paso 4: Reiniciar Servicio
1. Ve a tu servicio en Render
2. Manual Deploy → "Clear build cache & deploy"

## Verificar que Funciona

Después de configurar, prueba la recuperación de contraseña y revisa los logs. Deberías ver:

```
[EMAIL] Intentando conectar a smtp.gmail.com:587...
[EMAIL] Conexión establecida, iniciando STARTTLS...
[EMAIL] Autenticando con usuario: tutorias.ensenachile@gmail.com...
[EMAIL] Autenticación exitosa, enviando email...
✅ Email de recuperación enviado a juanfernandomir@gmail.com
```

