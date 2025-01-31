TELEGRAM ADLİ ANALİZ ARACI

1. GİRİŞ
Bu çalışmada geliştirilen program, Telegram mesajlaşma uygulamasından dışa aktarılan JSON formatındaki verileri analiz eden kapsamlı bir adli analiz aracıdır. Program, modern bir grafik kullanıcı arayüzü (GUI) kullanarak, dijital adli analiz uzmanlarına ve araştırmacılara detaylı veri analizi imkanı sunmaktadır.

2. PROGRAMIN TEMEL ÖZELLİKLERİ

2.1. Genel İstatistikler Modülü
•  Toplam mesaj, kullanıcı ve medya sayılarının istatistiksel analizi
•  En sık kullanılan kelimelerin interaktif kelime bulutu ile görselleştirilmesi
•  Kullanıcı aktivitelerinin pasta grafikleri ile sunumu

2.2. Medya Analizi Modülü
•  Profil fotoğrafları ve hikayelerin kronolojik sıralama ile görüntülenmesi
•  Her medya öğesi için tarih ve süre bilgilerinin detaylı gösterimi
•  Medya türlerinin dağılımının grafiksel analizi

2.3. Mesaj Analizi Modülü
•  Kronolojik sırayla mesaj içeriklerinin listelenmesi
•  Mesaj sahipleri ve gönderim tarihlerinin detaylı gösterimi
•  Mesaj istatistiklerinin çeşitli grafiklerle görselleştirilmesi

2.4. Kişi Analizi Modülü
•  Kullanıcıların mesaj aktivitelerinin detaylı analizi
•  En aktif kullanıcıların grafiksel gösterimi
•  Kullanıcı bazlı iletişim örüntülerinin analizi

2.5. Zaman Analizi Modülü
•  Mesajların zaman içindeki dağılımının grafiksel gösterimi
•  Günlük, haftalık ve aylık mesaj yoğunluğunun analizi
•  İletişim örüntülerinin zamansal analizi

3. TEKNİK ALTYAPI
Program, Python programlama dili kullanılarak geliştirilmiş olup, aşağıdaki kütüphanelerden yararlanmaktadır:
•  Tkinter: Grafik kullanıcı arayüzü için
•  Matplotlib: Veri görselleştirme ve grafik oluşturma için
•  PIL (Python Imaging Library): Görüntü işleme için
•  Wordcloud: Kelime bulutu oluşturma için


4. KULLANIM ALANLARI
Program özellikle şu alanlarda etkin kullanım sağlamaktadır:
•  Dijital adli bilişim incelemeleri
•  Dijital delillerin analizi ve raporlanması
•  İletişim örüntülerinin tespiti
•  Kullanıcı davranışlarının analizi

5. SONUÇ
Geliştirilen bu analiz aracı, kullanıcı dostu arayüzü sayesinde teknik olmayan kullanıcıların da kolayca analiz yapabilmesine olanak sağlamaktadır. Özellikle adli bilişim incelemelerinde, dijital delillerin analizi ve raporlanması süreçlerinde etkili bir araç olarak kullanılabilmektedir.

JSON Dosyasına Nasıl ulaşabilirim
> Masaüstü telegram uygulumasına giriş yaptıktan sonra sol taraftaki üç çizgiye bastıktan sonra -> Ayarlar -> Gelişmiş -> Telegram Verilerimi Dışa Aktar
> Burada indireceğimiz dizini ve hangi formatlarda çıktı alacağımızı (JSON VEYA HTML VEYA HER İKİSİ DE ) ve istediğimiz seçenekleri işaretleyip dışa aktar seçeneğine basıyoruz.
