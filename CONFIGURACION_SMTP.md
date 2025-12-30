# Configuración SMTP en Render

## Paso 1: Ir a Render Dashboard
1. Ve a: https://dashboard.render.com
2. Selecciona tu servicio (app-tutorias)
3. Click en **Settings** (Configuración)
4. Scroll hasta **Environment Variables** (Variables de Entorno)

## Paso 2: Agregar Variables SMTP

Click en **Add Environment Variable** y agrega estas 5 variables:

### Variable 1:
- **Key**: `SMTP_SERVER`
- **Value**: `smtp.ensenachile.cl`

### Variable 2:
- **Key**: `SMTP_PORT`
- **Value**: `587` (o `465` si usa SSL)

### Variable 3:
- **Key**: `SMTP_USER`
- **Value**: `tutorias@ensenachile.cl`

### Variable 4:
- **Key**: `SMTP_PASSWORD`
- **Value**: `[tu contraseña de correo]`

### Variable 5:
- **Key**: `FRONTEND_URL`
- **Value**: `https://app-tutorias.onrender.com`

## Paso 3: Reiniciar Servicio
1. Ve a **Manual Deploy**
2. Click en **Clear build cache & deploy**

## Nota sobre SMTP_PORT:
- **587**: Puerto estándar con STARTTLS (recomendado)
- **465**: Puerto SSL directo
- Si no funciona 587, prueba 465

