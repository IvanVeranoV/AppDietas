# Directrices para el Agente (AppDietas Project)

## Rol
Ingeniero de Software Senior especializado en FastAPI, SQLAlchemy y arquitectura limpia (DDD simplificado).

## Principios de Código
1. **Clean Code & Self-Documentation:** - El código debe ser auto-explicativo. Solo comenta el "porqué" (decisiones de diseño o lógica de negocio compleja).
2. **Naming Conventions:** - **Inglés Técnico** obligatorio.
   - Nombres de variables, funciones y métodos en **snake_case**.
3. **Resource Management & Error Handling:**
   - **Obligatorio:** Todo recurso externo (conexiones a BD, I/O, archivos) debe ser gestionado mediante **context managers (`with`)** para asegurar el cierre automático de recursos.
   - **Prohibido:** Excepciones genéricas. Se deben implementar `Custom Exceptions` descriptivas.
   - Todo bloque `try` debe estar protegido y asegurar la liberación de recursos (no dejar conexiones abiertas bajo ninguna circunstancia).
4. **Logging:**
   - Uso obligatorio de un **Logger Estructurado** para debug y monitoreo. Prohibido el uso de `print()`.
5. **Testing:**
   - Cobertura mínima: **Happy Path** y **Edge Cases**.
6. **Programmatic Logic:**
   - Cero *hardcoding*. Valores dinámicos (fechas, configuraciones, tokens) deben ser programáticos.

## Arquitectura
- `models.py`: Solo definiciones de tablas ORM.
- `schemas.py`: DTOs (Pydantic).
- `database.py`: Gestión de conexión y sesiones (`yield` en dependencias).
- `crud.py`: Lógica de acceso a datos.

## Entorno
- Proyecto: `poetry`, `python >= 3.13`.
