# Movie HTML Pages (DEPRECATED)

❗️ Endi alohida kino HTML fayllar (masalan, `9-jumboq.html`, `jin-tilak-tila.html`) ishlatilmaydi. Routing va SEO dinamik ravishda `index.html` ichida hash (`#slug.html`) orqali yuklanadi.

## Xususiyatlar

Oldingi xususiyatlar (statik fayllar):
- Har bir kino uchun alohida SEO-optimized HTML
- Open Graph / Twitter Card meta taglari
- Structured Data (Schema.org)
- Redirect orqali SPA ga kirish

Hozirgi yechim (dinamik):
- Bitta `index.html` ichida hash orqali `#slug.html` formatida deep link
- Slug / ID dan kino topiladi va SEO meta teglari dinamik yangilanadi (`updateMovieSEO()` funksiyasi)
- Spinner → avtomatik rerender film Firestore kelganda

## Nima o'zgardi?
Statik kino sahifalari olib tashlandi. Endi foydalanuvchi:
`https://www.soundora-music.com/#jin-tilak-tila.html` yoki `#9-jumboq.html` ga kirsa, sahifa `parseAppHash()` orqali filmni aniqlaydi va `renderMovieDetailsPage()` uni ko'rsatadi.

## Installation

### (ESKI) Usul 1: Oddiy Python Script

```bash
python generate_movie_pages.py
```

Bu avval test uchun ishlatilgan. Endi kerak emas.

### (ESKI) Usul 2: Firebase bilan barcha kinolar

1. Firebase service account key yuklab oling:
   - Firebase Console > Project Settings > Service Accounts
   - "Generate New Private Key" bosing
   - `serviceAccountKey.json` nomi bilan saqlang

2. Firebase Admin SDK o'rnating:
```bash
pip install firebase-admin
```

3. Scriptni ishga tushiring:
```bash
python firebase_movie_generator.py
```

Endi tavsiya etilmaydi. Film ma'lumotlari real-time snapshot orqali yuklanadi.

## Joriy Fayl Tuzilishi
```
app/src/main/assets/
   └── index.html   # Barcha routing va SEO shu yerda
```

## URL Structure

URL Formatlari:
- Hash slug: `https://www.soundora-music.com/#jin-tilak-tila.html`
- Hash id (fallback): `https://www.soundora-music.com/#123.html`
Frontend avtomatik ravishda slugni ID ga mapping qiladi.

## SEO Holati
`updateMovieSEO(movie)` funksiyasi sahifa yuklanganda:
- `<title>` va meta description yangilaydi
- Open Graph / Twitter / canonical URL ni sozlaydi
- JSON-LD (Movie schema) yaratadi
Chiqayotgan botlar hash URL larni to'liq indekslash uchun server-side prerender kerak bo'lishi mumkin (keyingi bosqich).

## Keyingi Qadamlar (Opsional)
1. Server-side prerender (Cloudflare Workers / Rendertron) → hash deep linklarni SEO uchun kuchaytirish
2. 404 / unknown slug handling: noma'lum slug bo'lsa `navigate({page:'main'})` + `showToast('Topilmadi')`
3. Sitemap yangilash: sluglar asosida dinamik sitemap generatsiya
4. Social share snapshot (og:image) generatsiya (Lambda / Cloud Function)

## Development

### Test (Dinamik)

Test uchun individual kino sahifasini yaratish:

```python
from generate_movie_pages import generate_movie_page

movie = {
    'id': 'my-movie',
    'title': 'My Movie',
    'year': '2024',
    # ... boshqa ma'lumotlar
}

generate_movie_page(movie, 'app/src/main/assets')
```

### Build

HTML fayllar yaratilgandan keyin:

```bash
.\gradlew assembleDebug
```

## Qo'shimcha Izohlar
- Statik kino fayllar REPODAN O'CHIRILDI.
- Deep link ishlashi: hash parse → slug/ID → spinner → Firestore snapshot → kino render.
- Agar film juda sekin kelsa: `renderMovieDetailsPage` 500ms retry qiladi.

## Troubleshooting

**Agar Firebase error bersa:**
- `serviceAccountKey.json` to'g'ri joylashganini tekshiring
- Firebase Admin SDK o'rnatilganini tekshiring
- Project ID to'g'riligini tekshiring

**Hash deep link ishlamasa:**
- Console da `parseAppHash` chiqishini tekshiring
- Slug index (`rebuildMovieSlugIndex`) muvaffaqiyatli ekanini tekshiring
- `movies` snapshot kelganini loglarda ko'ring (`📽️ Movies loaded:`)

---
Deprecated bo'lim qoldirildi tarix uchun; yangi arxitektura SPA hash-based.
