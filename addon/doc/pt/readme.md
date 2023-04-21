# Complemento Wake Speaker para NVDA  #

Este complemento emite ruído branco em volume baixo para manter os alto-falantes acordados. Isso é útil se você tiver Alto-falantes que entram no modo de suspensão quando param de receber um fluxo de áudio, geralmente com o objetivo de economizar energia.

Copyright (C) 2023 David CM <dhf360@gmail.com>

Este complemento é distribuído sob os termos da GNU General Public License, Versão 2 ou posterior.

## Como esse complemento difere dos existentes?

Este complemento surge após a necessidade de alguns fones de ouvido bluetooth, que exigem que o fluxo de áudio seja pausado a cada certo tempo para poder manter a modalidade de baixa latência. Caso contrário, a latência aumenta ou o áudio é interrompido às vezes.

Se você não tem essa necessidade, você pode usar o complemento com sua funcionalidade básica. Se você precisar desse recurso adicional, verifique as configurações para adaptá-lo às suas necessidades.


## Download.

A versão mais recente deste complemento pode ser [baixado neste link.](https://davidacm.github.io/getlatest/gh/davidacm/WakeSpeaker)

## Uso e configuração.

Quando você instala este complemento, ele permanece ativo por padrão. Se você quiser modificar algum comportamento, vá para as opções do NVDA, categoria Wake Speaker, e ajuste qualquer uma das seguintes opções:

* Ativar o Wake Speaker: alterna a funcionalidade do complemento.
* Suspender após (segundos): a quantidade de tempo antes de suspender o fluxo de ruído usado para manter a saída de áudio acordada. O tempo começa a partir da última vez que o NVDA produziu voz ou tons. Padrão 60 segundos.
* Volume de ruído: o volume de ruído branco, por padrão, é 0. Aumente se o Nível 0 não for suficiente para o seu dispositivo.
* Tentar uma pausa após (Segundos): tenta produzir uma pausa de áudio após n segundos, o complemento tentará até que nenhum outro fluxo de áudio do NVDA exista durante a pausa. mantenha esse parâmetro em 0 se você não precisar desse recurso. Se você tiver um fluxo de áudio externo para o NVDA, como ao ouvir música, a pausa não terá efeito.
* Duração da pausa (MS): o tempo que a pausa dura em milissegundos, este parâmetro só tem efeito se o anterior estiver ativo.

## Requisitos
  
    Você precisa do NVDA 2019.3 ou posterior.

## contribuições, relatórios e doações

Se você gosta do meu projeto ou este software é útil para você em sua vida diária e gostaria de contribuir de alguma forma, você pode doar através dos seguintes métodos:

* [PayPal.](https://paypal.me/davicm)
* [Ko-fi.](https://ko-fi.com/davidacm)
* [Criptomoedas e outros métodos.](https://davidacm.github.io/donations/)

Se você quiser fazer correções, relatar problemas ou novas funcionalidades, entre em contato comigo em: <dhf360@gmail.com>.

  Ou no repositório github deste projeto:
  [Projeto do Wake Speaker no GitHub](https://github.com/davidacm/WakeSpeaker)

    Você pode obter a versão mais recente deste complemento nesse repositório.
