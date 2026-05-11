# ebd-datafile-analysis

Herramienta mínima para analizar archivos CSV exportados desde eBird.

## Uso

```bash
python /home/runner/work/ebd-datafile-analysis/ebd-datafile-analysis/analyze_ebird_datafile.py /ruta/al/archivo.csv
```

## Salida

El script muestra un resumen con:

- Total de observaciones (filas)
- Total de especies únicas
- Total de individuos (solo conteos numéricos)
- Registros con conteo no numérico (por ejemplo `X`)
- Total de listas (si existe `Submission ID` o `Checklist ID`)
- Top 10 especies más reportadas
