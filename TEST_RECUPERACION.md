# Guía de Prueba - Recuperación de Contraseña

## Pasos para Probar

### 1. Verificar que el servicio esté funcionando
- Ve a: https://app-tutorias.onrender.com
- Debería cargar la página de login

### 2. Probar Recuperación de Contraseña

#### Paso 1: Solicitar recuperación
1. En la página de login, click en **"¿Olvidaste tu contraseña?"**
2. Ingresa el email: `juanfernandomir@gmail.com`
3. Click en **"Enviar"**
4. Deberías ver el mensaje: *"Si el email existe, se enviará un enlace de recuperación"*

#### Paso 2: Verificar el email
1. Revisa la bandeja de entrada de `juanfernandomir@gmail.com`
2. Busca un email con asunto: **"Recuperación de Contraseña - Plataforma Tutorías"**
3. Si no está en la bandeja principal, revisa **Spam/Correo no deseado**

#### Paso 3: Usar el enlace
1. Abre el email
2. Click en el enlace que contiene: `https://app-tutorias.onrender.com/reset-password?token=XXXXX`
3. Deberías ver la página de "Restablecer Contraseña"

#### Paso 4: Cambiar contraseña
1. Ingresa una nueva contraseña (mínimo 6 caracteres)
2. Confirma la contraseña
3. Click en **"Restablecer Contraseña"**
4. Deberías ver: **"✅ Contraseña Restablecida"**
5. Serás redirigido al login automáticamente

#### Paso 5: Probar login con nueva contraseña
1. En el login, ingresa:
   - Email: `juanfernandomir@gmail.com`
   - Contraseña: [la nueva que acabas de poner]
2. Click en **"Iniciar Sesión"**
3. Deberías poder entrar al sistema

## Verificar Logs en Render

Si el email no llega, verifica los logs:

1. Ve a Render Dashboard → Tu servicio
2. Click en **"Logs"**
3. Busca mensajes como:
   - `✅ Email de recuperación enviado a juanfernandomir@gmail.com`
   - `❌ Error de autenticación SMTP`
   - `⚠️ SMTP no configurado`

## Posibles Problemas

### Email no llega
- **Verifica variables SMTP**: Asegúrate que todas las variables estén correctas
- **Revisa Spam**: El email puede estar en correo no deseado
- **Verifica logs**: Revisa los logs de Render para ver errores
- **Prueba puerto**: Si usas puerto 587 y no funciona, prueba 465

### Error 500 al solicitar recuperación
- Verifica que las variables SMTP estén configuradas
- Revisa los logs del servicio en Render

### Token inválido o expirado
- Los tokens expiran en 1 hora
- Solo se puede usar una vez
- Si expiró, solicita uno nuevo

## Comandos para Probar desde Terminal

### Probar endpoint directamente (opcional)
```bash
curl -X POST https://app-tutorias.onrender.com/auth/request-password-reset \
  -H "Content-Type: application/json" \
  -d '{"email": "juanfernandomir@gmail.com"}'
```

Debería retornar:
```json
{
  "message": "Si el email existe, se enviará un enlace de recuperación"
}
```

