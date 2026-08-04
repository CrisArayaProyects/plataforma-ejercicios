import subprocess
import sys
import tempfile
import os


def ejecutar_codigo(codigo_alumno, entrada, timeout_segundos=5):
    """
    Ejecuta el código del alumno en un proceso separado, le pasa 'entrada'
    como si el alumno escribiera eso en el input(), y devuelve lo que
    el programa imprimió (o un mensaje de error si falló).
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as archivo_temp:
        archivo_temp.write(codigo_alumno)
        ruta_temp = archivo_temp.name

    try:
        resultado = subprocess.run(
            [sys.executable, ruta_temp],
            input=entrada,
            capture_output=True,
            text=True,
            timeout=timeout_segundos
        )
        if resultado.returncode != 0:
            return None, resultado.stderr.strip()
        return resultado.stdout.strip(), None

    except subprocess.TimeoutExpired:
        return None, f"El programa tardó más de {timeout_segundos} segundos (¿ciclo infinito?)"

    finally:
        os.remove(ruta_temp)


def coincide(salida_real, esperado):
    """
    Compara la salida real contra la esperada, tolerando texto de prompts
    (como 'Ingresar n1: ') que el alumno haya puesto dentro de sus input().
    """
    salida_real = salida_real.strip()
    esperado = esperado.strip()

    if salida_real == esperado:
        return True

    if salida_real.endswith(esperado):
        indice_previo = len(salida_real) - len(esperado) - 1
        if indice_previo < 0:
            return True
        caracter_previo = salida_real[indice_previo]
        # Si el caracter justo antes no es letra/número, es un límite válido
        if not caracter_previo.isalnum():
            return True

    return False


def corregir_ejercicio(codigo_alumno, casos):
    """
    Corre el código del alumno contra cada caso de prueba y devuelve
    una lista de resultados (uno por caso) más el conteo de aciertos.
    """
    resultados = []
    aciertos = 0

    for i, caso in enumerate(casos, start=1):
        entrada = caso["input"]
        esperado = caso["output_esperado"].strip()

        salida, error = ejecutar_codigo(codigo_alumno, entrada)

        if error:
            resultados.append({
                "caso": i,
                "paso": False,
                "detalle": f"Error al ejecutar: {error}"
            })
        elif coincide(salida, esperado):
            resultados.append({"caso": i, "paso": True, "detalle": "Correcto"})
            aciertos += 1
        else:
            resultados.append({
                "caso": i,
                "paso": False,
                "detalle": f"Se esperaba '{esperado}' pero se obtuvo '{salida}'"
            })

    return resultados, aciertos, len(casos)