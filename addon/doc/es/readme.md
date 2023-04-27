# Complemento Wake Speaker para NVDA  #

Este complemento emite un ruido blanco a bajo volumen para mantener los altavoces despiertos. Esto es útil si tienes altavoces que se ponen en modo suspención cuando dejan de recibir un flujo de audio, generalmente con el objetivo de ahorrar energía.

Copyright (C) 2023 David CM <dhf360@gmail.com>

Este complemento se distribuye bajo los términos de la Licencia Pública General GNU, versión 2 o posterior.

## ¿Cómo se diferencia este complemento de los existentes?

Este complemento surge tras una necesidad de algunos audífonos bluetooth, que requieren que el flujo de audio sea pausado cada cierto tiempo para poder mantener la modalidad de baja latencia. De no hacerlo, la latencia aumenta o el audio se ve interrumpido en ocasiones.

Si no tienes dicha necesidad, puedes usar el complemento con su funcionalidad básica. Si necesitas esta característica adicional, entonces verifica las configuraciones para adaptarlo a tus necesidades.


## Descarga.

La última versión de este complemento se puede [descargar en este enlace.](https://davidacm.github.io/getlatest/gh/davidacm/WakeSpeaker/?index=1)

## Uso y configuración.

Cuando instales este complemento, estará activo por defecto.

Este complemento tiene un script para alternar el estado del complemento (activado o desactivado) que no tiene gesto asignado. Puedes asignar gestos en el diálogo "Gestos de entrada".

Si deseas modificar algún comportamiento, ve a las opciones de NVDA, categoría Wake Speaker, y ajusta cualquiera de las siguientes opciones:

* Habilitar Wake Speaker: alterna la funcionalidad del complemento.
* Suspender después de  (segundos): la cantidad de tiempo antes de suspender el flujo de ruido utilizado para mantener despierta la salida de audio. El tiempo comienza desde la última vez que NVDA produjo voz o tonos. Por defecto 60 segundos.
* Volumen del ruido: el volumen del ruido blanco, por defecto es 0. Auméntalo si al nivel 0 no es suficiente para tu dispositivo.
* Intentar una pausa después de (Segundos): Intenta producir una pausa de audio después de n segundos, el complemento lo intentará hasta que durante la pausa no exista ningún otro flujo de audio de NVDA. mantén este parámetro en 0 si no necesitas esta característica. Si posees un flujo de audio externo a NVDA, como por ejemplo cuando escuchas música, la pausa no tendrá efecto.
* Duración de la pausa (MS): el tiempo que dura la pausa en milisegundos, este parámetro solo tiene efecto si el anterior está activo.

## Requisitos
  Necesitas NVDA 2019.3 o posterior.

## contribuciones, reportes y donaciones

Si te gusta mi proyecto o este software te es útil en tu vida diaria y te gustaría contribuir de alguna manera, puedes donar a través de los siguientes métodos:

* [PayPal.](https://paypal.me/davicm)
* [Ko-fi.](https://ko-fi.com/davidacm)
* [Criptomonedas y otros métodos.](https://davidacm.github.io/donations/)

Si deseas realizar correcciones, informar problemas o nuevas funcionalidades, puedes contactarme en: <dhf360@gmail.com>.

  O en el repositorio de github de este proyecto:
  [Wake Speaker en GitHub](https://github.com/davidacm/WakeSpeaker)

    Puedes obtener la última versión de este complemento en dicho repositorio.
