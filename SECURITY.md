# Security

## Uso autorizado / Authorized use

PhiStack es un gestor de herramientas, muchas de ellas de ciberseguridad
ofensiva (phishing, explotación, fuerza bruta). El uso de cualquier herramienta
debe limitarse a sistemas que **posees** o para los que tienes **permiso
explícito por escrito**. El autor no se responsabiliza del mal uso.

## Reportar vulnerabilidades

Si encuentras un problema de seguridad en PhiStack (no en las herramientas que
instala), abre un issue privado o contacta con el autor. Incluye:

- Descripción del fallo.
- Pasos para reproducirlo.
- Impacto potencial.

## Supply-chain

- Los `download` directos del catálogo permiten fijar `sha256`.
- No se usa `curl | bash` para instalar dependencias del catálogo.
- Las herramientas de terceros se clonan de repositorios públicos; revisa
  siempre el script antes de ejecutar una instalación desconocida.
- Ejecuta `phi doctor` para validar el entorno antes de instalar.
