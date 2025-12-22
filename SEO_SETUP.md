# SEO Optimizatsiyalari - SND Streaming App

## Qanday ishlaydi?

Google'da kino nomini qidirsangiz, endi SND ilovasidagi kinolar to'g'ridan-to'g'ri Google qidiruv natijalarida ko'rinadi va bosilganda kino sahifasiga olib boradi.

## Qo'shilgan funksiyalar

### 1. **Dinamik Meta Teglar**
Har bir kino sahifasi uchun avtomatik ravishda yangilanadigan meta teglar:
- `<title>` - Kino nomi + yili
- `<meta description>` - Kino tavsifi
- `<meta keywords>` - Kino, janr, aktyorlar

### 2. **Open Graph Protokoli**
Ijtimoiy tarmoqlarda (Facebook, Telegram, WhatsApp) ulashganda chiroyli ko'rinadi:
- Kino afishasi rasmi
- Kino nomi va tavsifi
- URL manzili

### 3. **Twitter Card**
Twitter'da ulashganda katta rasm bilan ko'rinadi:
- Large Image card formati
- Kino rasmi, nomi, tavsifi

### 4. **Structured Data (JSON-LD)**
Google uchun boy natijalar (Rich Snippets):
- Kino nomi, janri, yili
- IMDB/SND reytingi
- Aktyorlar, rejissyor
- Studiya, davlat

### 5. **Canonical URL**
Dublikat sahifalarni oldini olish uchun

### 6. **Ulashish Tugmasi**
Har bir kino sahifasida yangi "Ulashish" tugmasi:
- Mobilda: Web Share API orqali ulashish
- Desktopda: URL ni clipboard'ga nusxalash

### 7. **Path-based URL qo'llab-quvvatlash**
Endi `/9-jumboq` kabi URL'lar avtomatik ravishda hash-based URL'ga yo'naltiriladi:
```
/9-jumboq → index.html#movie-details?movieId=9-jumboq
```

## Fayl tuzilishi

```
app/src/main/assets/
├── index.html          (asosiy ilova - SEO meta teglar qo'shilgan)
├── sitemap.xml         (Google uchun sahifalar ro'yxati)
├── robots.txt          (qidiruv robotlari uchun qoidalar)
└── .htaccess           (Apache server uchun URL qayta yo'naltirish)
```

## Qanday ishlatish?

### Kinoni ulashish
1. Kino sahifasini oching
2. Yashil "Ulashish" tugmasini bosing
3. Mobilda: Ulashish menusi ochiladi (WhatsApp, Telegram, va boshqalar)
4. Desktopda: URL avtomatik clipboard'ga nusxalanadi

### Google'da qidirish
Google serverda bo'lganida (production):
1. Google'ga kino nomini yozing, masalan: "Jumboq kino SND"
2. Google natijalarda SND saytidagi kino ko'rinadi
3. Bosinganda to'g'ridan-to'g'ri kino sahifasiga olib boradi

## Server sozlamalari

### Apache Server
`.htaccess` fayli allaqachon tayyor - `/9-jumboq` kabi URL'larni avtomatik qayta yo'naltiradi.

### Nginx Server
Nginx uchun quyidagi konfiguratsiyani qo'shing:

```nginx
location /app/src/main/assets/ {
    try_files $uri $uri/ /app/src/main/assets/index.html;
    
    # Handle clean movie URLs
    rewrite ^/app/src/main/assets/([a-zA-Z0-9\-]+)$ /app/src/main/assets/index.html#movie-details?movieId=$1 redirect;
}
```

### VS Code Live Server
Live Server avtomatik ishlaydi, lekin path-based URL'lar 404 qaytaradi.
To'g'ri URL format:
```
http://127.0.0.1:5500/app/src/main/assets/index.html#movie-details?movieId=9-jumboq
```

## URL formatlari

### Hash-based (hozirgi)
```
✅ http://yourdomain.com/app/src/main/assets/index.html#movie-details?movieId=9-jumboq
```

### Path-based (server konfiguratsiyasi kerak)
```
✅ http://yourdomain.com/app/src/main/assets/9-jumboq
   (avtomatik hash-based'ga yo'naltiriladi)
```

## Google Search Console'da indekslash

1. [Google Search Console](https://search.google.com/search-console)'ga kiring
2. Saytingizni qo'shing
3. Sitemap URL'ni qo'shing:
   ```
   https://yourdomain.com/app/src/main/assets/sitemap.xml
   ```
4. "URL Inspection" orqali har bir kino sahifasini tekshiring
5. "Request Indexing" tugmasini bosing

## Social Media Preview tekshirish

### Facebook/Meta
https://developers.facebook.com/tools/debug/

### Twitter
https://cards-dev.twitter.com/validator

### LinkedIn
https://www.linkedin.com/post-inspector/

## Maslahatlar

1. **Kino ma'lumotlarini to'ldiring**: Har bir kino uchun to'liq ma'lumot kiriting (tavsif, poster, aktyorlar)
2. **Sifatli rasmlar**: Posterlar kamida 1200x630 piksel bo'lishi kerak
3. **Unique tavsiflar**: Har bir kino uchun o'ziga xos tavsif yozing
4. **Schema Markup tekshirish**: https://search.google.com/test/rich-results
5. **Tezlikni oshirish**: Rasmlarni siqib, CDN ishlatish

## Monitoring

### Google Analytics
Qaysi kinolar ko'p qidirilayotganini kuzatish uchun Google Analytics qo'shing.

### Google Search Console
Qaysi kalit so'zlar orqali foydalanuvchilar kelayotganini ko'rish.

## Yordam

Muammolar bo'lsa:
1. Browser console'ni tekshiring (F12)
2. Meta teglar to'g'ri yuklanganini tasdiqlang
3. Structured data xatolarini tekshiring: https://validator.schema.org/

---

**Eslatma**: Bu optimizatsiyalar production serverda (jonli domenда) to'liq ishlaydi. Localhost'da faqat ulashish funksiyasi ishlaydi.
