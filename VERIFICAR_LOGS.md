# Cómo Verificar los Logs de SMTP en Render

## Pasos para Ver los Logs

### 1. Acceder a los Logs
1. Ve a: https://dashboard.render.com
2. Selecciona tu servicio (app-tutorias o tutorias-app)
3. Click en **"Logs"** en el menú lateral

### 2. Buscar Errores de SMTP

En los logs, busca estos mensajes:

#### ✅ Si funciona:
```
[EMAIL] Intentando conectar a smtp.ensenachile.cl:587...
[EMAIL] Conexión establecida, iniciando STARTTLS...
[EMAIL] Autenticando con usuario: tutorias@ensenachile.cl...
[EMAIL] Enviando email a juanfernandomir@gmail.com...
✅ Email de recuperación enviado a juanfernandomir@gmail.com
```

#### ❌ Si hay errores:

**Error de conexión:**
```
❌ Error de conexión SMTP: No se pudo conectar a smtp.ensenachile.cl:587
```
→ **Solución**: Verifica SMTP_SERVER y SMTP_PORT. Prueba puerto 465.

**Error de autenticación:**
```
❌ Error de autenticación SMTP: (535, '5.7.8 Username and Password not accepted')
```
→ **Solución**: Verifica SMTP_USER y SMTP_PASSWORD. Asegúrate de usar la contraseña correcta.

**SMTP no configurado:**
```
⚠️  SMTP no configurado. Variables SMTP_USER y SMTP_PASSWORD requeridas.
```
→ **Solución**: Verifica que el Environment Group esté vinculado al servicio.

### 3. Filtrar Logs

En la barra de búsqueda de logs, busca:
- `EMAIL` - Para ver todos los mensajes de email
- `SMTP` - Para ver errores SMTP
- `Error` - Para ver todos los errores

### 4. Probar de Nuevo

Después de corregir las variables:
1. Ve a **Manual Deploy**
2. Click en **"Clear build cache & deploy"**
3. Espera a que termine el deploy
4. Prueba la recuperación de contraseña de nuevo
5. Revisa los logs nuevamente

## Problemas Comunes

### Variables no se aplican
- Verifica que el Environment Group esté vinculado al servicio
- Reinicia el servicio después de agregar variables

### Puerto incorrecto
- Prueba primero con `587`
- Si no funciona, prueba con `465` (SSL directo)
- Algunos servidores usan `25` (no recomendado)

### Servidor SMTP bloquea conexiones
- Algunos servidores solo permiten conexiones desde IPs específicas
- Contacta al administrador de correo de ensenachile.cl

