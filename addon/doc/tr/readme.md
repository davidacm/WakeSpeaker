# Hoparlörü Uyanık Tut NVDA Eklentisi #

Bu eklenti, hoparlörleri uyanık tutmak için çok düşük bir ses seviyesinde duyulmayan gürültü yayar. Bu, genellikle güç tasarrufu yapmak için bir ses akışı almayı bıraktıklarında uykuya geçen hoparlörleriniz varsa kullanışlıdır.  

Telif Hakkı (C) 2023 David CM <dhf360@gmail.com>  

Bu paket, GNU Genel Kamu Lisansı, sürüm 2 veya sonraki sürümler altında dağıtılmaktadır.  

## Bu eklentinin mevcut olanlardan farkı nedir?

Bu fikir, düşük gecikme modunu korumak için ses akışının zaman zaman duraklatılmasını gerektiren bazı bluetooth kulaklıklara duyulan ihtiyaçtan sonra ortaya çıktı. Aksi takdirde, gecikme artar veya ses zaman zaman kesilir.  

Böyle bir ihtiyacınız yoksa, eklentiyi temel işlevselliği ile kullanabilirsiniz. Bu ek özelliğe ihtiyacınız varsa, ihtiyaçlarınıza göre uyarlamak için ayarları kontrol edin.  

## İndirme:
 [En son sürüm bu bağlantıdan indirilebilir.](https://davidacm.github.io/getlatest/gh/davidacm/WakeSpeaker)

## Kullanım ve ayarlar:

Bu eklenti yüklendiğinde, varsayılan olarak etkin olacaktır.  

Eklentiyi etkinleştirmek veya devre dışı bırakmak için bir kısa yol bulunmaktadır.  
Lakin, varsayılan olarak bir hareket tanımlanmamıştır.  
Her zamanki gibi:  
NVDA Menüsü>Tercihler>Girdi Hareketleri iletişim kutusunda, Hoparlörü Uyanık Tut dalı altından istenen hareket tanımlanabilir.  

Aşağıda bulunan seçenekleri yapılandırmak için, NVDA Menüsü>Tercihler>Ayarlar iletişim kutusunda, Hoparlörü Uyanık Tut dalına gitmek yeterli olacaktır.  

* Hoparlör Uyandırmayı Etkinleştir: İşaretliyse, etkin, değilse eklenti devre dışı olur.
* Şu kadar süre sonra ses çalmayı durdur (Saniye olarak): Ses çıkışını uyanık tutmak için kullanılan gürültü akışını askıya almadan önce geçen süre. Süre, NVDA'nın ses veya tonlar ürettiği son andan itibaren başlar. Varsayılan olarak 60 saniye.
* Gürültü ses düzeyi: beyaz gürültünün ses seviyesi varsayılan olarak 0'dır. Çıkış cihazınız için 0 seviyesi yeterli değilse yükseltin.
* Gürültüyü şu kadar süre sonra duraklatmayı dene (saniye olarak): bu, sesi belirtilen saniyeden sonra duraklatmaya çalışır, eklenti duraklama sırasında başka bir NVDA ses akışı kalmayana kadar dener. Bu özelliğe ihtiyacınız yoksa bu parametreyi 0'da tutun. NVDA dışında bir ses akışınız varsa, örneğin müzik dinlerken, akışı duraklatmanın hiçbir etkisi olmaz.
* Duraklama süresi (Milisaniye olarak): duraklamanın milisaniye cinsinden süresini belirler, bu parametre yalnızca bir önceki seçenek etkinse etkilidir.

## Gereksinimler:
  NVDA 2019.3 veya sonrası sürümler gereklidir.

## katkılar, raporlar ve bağışlar:

Projemi beğendiyseniz, bu yazılım günlük hayatınızda işinize yararsa ve bir şekilde katkıda bulunmak isterseniz aşağıdaki yöntemlerle bağışta bulunabilirsiniz:  

* [PayPal.](https://paypal.me/davicm)
* [Ko-fi.](https://ko-fi.com/davidacm)
* [kripto para birimleri ve diğer yöntemler.](https://davidacm.github.io/donations/)

Hataları düzeltmek, sorunları bildirmek veya yeni özellik isteğinde bulunmak için benimle <dhf360@gmail.com> adresinden iletişime geçebilirsiniz.  

  Veya bu projenin github deposunda:  
  [GitHub'da Hoparlörü Uyanık Tut](https://github.com/davidacm/WakeSpeaker)  

    Eklentinin en son sürümünü bu depodan edinebilirsiniz.
