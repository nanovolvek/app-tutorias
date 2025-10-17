# Script para desplegar backend en AWS App Runner
# Ejecutar desde la raíz del proyecto

Write-Host "🚀 Iniciando despliegue del backend en AWS App Runner..." -ForegroundColor Green

# Variables
$AWS_REGION = "us-east-1"
$ECR_REPOSITORY = "tutorias-backend"
$IMAGE_TAG = "latest"
$AWS_ACCOUNT_ID = ""

Write-Host "📋 Paso 1: Verificando AWS CLI..." -ForegroundColor Yellow
try {
    $awsVersion = aws --version
    Write-Host "✅ AWS CLI instalado: $awsVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ AWS CLI no está instalado. Instalando..." -ForegroundColor Red
    Write-Host "Por favor instala AWS CLI desde: https://aws.amazon.com/cli/" -ForegroundColor Yellow
    exit 1
}

Write-Host "📋 Paso 2: Obteniendo Account ID..." -ForegroundColor Yellow
try {
    $accountInfo = aws sts get-caller-identity --output json
    $AWS_ACCOUNT_ID = ($accountInfo | ConvertFrom-Json).Account
    Write-Host "✅ Account ID: $AWS_ACCOUNT_ID" -ForegroundColor Green
} catch {
    Write-Host "❌ Error obteniendo Account ID. Verifica tu configuración de AWS CLI" -ForegroundColor Red
    exit 1
}

$ECR_URI = "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY"

Write-Host "📋 Paso 3: Creando repositorio ECR..." -ForegroundColor Yellow
try {
    aws ecr create-repository --repository-name $ECR_REPOSITORY --region $AWS_REGION
    Write-Host "✅ Repositorio ECR creado: $ECR_URI" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Repositorio ECR ya existe o error al crearlo" -ForegroundColor Yellow
}

Write-Host "📋 Paso 4: Autenticando Docker con ECR..." -ForegroundColor Yellow
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_URI

Write-Host "📋 Paso 5: Construyendo imagen Docker..." -ForegroundColor Yellow
Set-Location backend
docker build -t "${ECR_REPOSITORY}:${IMAGE_TAG}" .

Write-Host "📋 Paso 6: Etiquetando imagen..." -ForegroundColor Yellow
docker tag "${ECR_REPOSITORY}:${IMAGE_TAG}" "${ECR_URI}:${IMAGE_TAG}"

Write-Host "📋 Paso 7: Subiendo imagen a ECR..." -ForegroundColor Yellow
docker push "${ECR_URI}:${IMAGE_TAG}"

Write-Host "✅ Imagen subida exitosamente!" -ForegroundColor Green
Write-Host "🔗 URI de la imagen: ${ECR_URI}:${IMAGE_TAG}" -ForegroundColor Cyan

Write-Host "📋 Paso 8: Creando servicio en App Runner..." -ForegroundColor Yellow
Write-Host "Ve a AWS App Runner Console y crea un servicio con:" -ForegroundColor Yellow
Write-Host "  - Source: Container registry" -ForegroundColor White
Write-Host "  - Provider: Amazon ECR" -ForegroundColor White
Write-Host "  - Container image URI: ${ECR_URI}:${IMAGE_TAG}" -ForegroundColor White
Write-Host "  - Service name: tutorias-backend" -ForegroundColor White

Write-Host "📋 Variables de entorno para App Runner:" -ForegroundColor Yellow
Write-Host "  DATABASE_URL: postgresql://postgres:tutorias-db-123456789@tutorias-db.cx6xogrsenqa.us-east-1.rds.amazonaws.com:5432/postgres" -ForegroundColor White
Write-Host "  SECRET_KEY: tutorias-db-123456789" -ForegroundColor White
Write-Host "  ALGORITHM: HS256" -ForegroundColor White
Write-Host "  ACCESS_TOKEN_EXPIRE_MINUTES: 30" -ForegroundColor White
Write-Host "  ALLOWED_ORIGINS: https://main.d1d2p1x4drhejl.amplifyapp.com,http://localhost:5173" -ForegroundColor White

Write-Host "📋 IMPORTANTE: Configurar RDS antes de continuar:" -ForegroundColor Red
Write-Host "  1. RDS Console -> Databases -> tutorias-db -> Modify" -ForegroundColor White
Write-Host "  2. Connectivity & security -> Public access: Yes" -ForegroundColor White
Write-Host "  3. EC2 Console -> Security Groups -> Edit inbound rules" -ForegroundColor White
Write-Host "  4. Add rule: Type=PostgreSQL, Port=5432, Source=0.0.0.0/0" -ForegroundColor White

Set-Location ..

Write-Host "🎉 ¡Despliegue completado!" -ForegroundColor Green
Write-Host "Una vez que App Runner esté listo, actualiza VITE_API_URL en Amplify con la URL del backend" -ForegroundColor Cyan
