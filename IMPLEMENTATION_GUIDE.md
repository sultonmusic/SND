# Soundora Platform - Implementation Guide

This guide provides ready-to-use code snippets for implementing the recommended improvements to the Soundora streaming platform.

## Table of Contents
1. [Language Switcher](#language-switcher)
2. [Empty Content Sections](#empty-content-sections)
3. [Search UX Improvements](#search-ux-improvements)
4. [Login Prompts for Guests](#login-prompts-for-guests)
5. [Accessibility Enhancements](#accessibility-enhancements)
6. [Registration Form Fixes](#registration-form-fixes)

---

## 1. Language Switcher

### Add to Header (HTML)
```html
<!-- Insert in header navigation, after search icon -->
<div class="language-selector-container">
    <button id="language-button" class="language-button" aria-label="Select language">
        <i class="fas fa-globe"></i>
        <span id="current-language-code">EN</span>
    </button>
    
    <div id="language-dropdown" class="language-dropdown hidden">
        <button class="language-option" data-lang="en" aria-label="Switch to English">
            English
        </button>
        <button class="language-option" data-lang="ru" aria-label="Переключить на русский">
            Русский
        </button>
        <button class="language-option" data-lang="uz" aria-label="O'zbekchaga o'tish">
            O'zbekcha
        </button>
    </div>
</div>
```

### Styling (CSS)
```css
.language-selector-container {
    position: relative;
}

.language-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 0.5rem;
    color: white;
    cursor: pointer;
    transition: all 0.3s ease;
}

.language-button:hover {
    background: rgba(255, 255, 255, 0.15);
}

.language-dropdown {
    position: absolute;
    top: 100%;
    right: 0;
    margin-top: 0.5rem;
    background: #1F2937;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0.5rem;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
    min-width: 150px;
    z-index: 1000;
}

.language-dropdown.hidden {
    display: none;
}

.language-option {
    width: 100%;
    text-align: left;
    padding: 0.75rem 1rem;
    background: transparent;
    border: none;
    color: #D1D5DB;
    cursor: pointer;
    transition: background 0.2s ease;
}

.language-option:hover {
    background: rgba(59, 130, 246, 0.1);
    color: white;
}

.language-option.active {
    background: rgba(59, 130, 246, 0.2);
    color: #3B82F6;
}
```

### JavaScript Implementation
```javascript
// Initialize language switcher
function initLanguageSwitcher() {
    const languageButton = document.getElementById('language-button');
    const languageDropdown = document.getElementById('language-dropdown');
    const languageOptions = document.querySelectorAll('.language-option');
    const currentLangCode = document.getElementById('current-language-code');
    
    // Toggle dropdown
    languageButton.addEventListener('click', (e) => {
        e.stopPropagation();
        languageDropdown.classList.toggle('hidden');
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', () => {
        languageDropdown.classList.add('hidden');
    });
    
    // Handle language selection
    languageOptions.forEach(option => {
        option.addEventListener('click', (e) => {
            e.stopPropagation();
            const lang = option.dataset.lang;
            switchLanguage(lang);
            languageDropdown.classList.add('hidden');
        });
        
        // Mark current language as active
        if (option.dataset.lang === window.currentLanguage) {
            option.classList.add('active');
        }
    });
    
    // Update button text
    updateLanguageButton();
}

function switchLanguage(lang) {
    if (!window.translations[lang]) {
        console.error(`Language ${lang} not found`);
        return;
    }
    
    window.currentLanguage = lang;
    localStorage.setItem('preferredLanguage', lang);
    
    updateLanguageButton();
    updateAllTranslations();
    
    // Update active state
    document.querySelectorAll('.language-option').forEach(opt => {
        opt.classList.toggle('active', opt.dataset.lang === lang);
    });
}

function updateLanguageButton() {
    const currentLangCode = document.getElementById('current-language-code');
    const langMap = { en: 'EN', ru: 'RU', uz: 'UZ' };
    currentLangCode.textContent = langMap[window.currentLanguage] || 'EN';
}

function updateAllTranslations() {
    const currentLang = window.currentLanguage || 'en';
    const translations = window.translations[currentLang];
    
    // Update all elements with data-lang-key attribute
    document.querySelectorAll('[data-lang-key]').forEach(element => {
        const key = element.dataset.langKey;
        if (translations[key]) {
            element.textContent = translations[key];
        }
    });
    
    // Update placeholder attributes
    document.querySelectorAll('[data-lang-key-placeholder]').forEach(element => {
        const key = element.dataset.langKeyPlaceholder;
        if (translations[key]) {
            element.placeholder = translations[key];
        }
    });
    
    // Update aria-label attributes
    document.querySelectorAll('[data-lang-key-aria]').forEach(element => {
        const key = element.dataset.langKeyAria;
        if (translations[key]) {
            element.setAttribute('aria-label', translations[key]);
        }
    });
}

// Call on page load
document.addEventListener('DOMContentLoaded', initLanguageSwitcher);
```

---

## 2. Empty Content Sections

### Coming Soon Component
```javascript
function createComingSoonSection(config = {}) {
    return `
        <div class="coming-soon-section w-full min-h-[400px] flex items-center justify-center p-8">
            <div class="text-center max-w-md">
                <div class="mb-6">
                    <i class="${config.icon || 'fas fa-film'} fa-4x text-gray-600"></i>
                </div>
                <h2 class="text-3xl font-bold text-white mb-3" data-lang-key="comingSoonTitle">
                    Coming Soon
                </h2>
                <p class="text-gray-400 mb-6 leading-relaxed" data-lang-key="${config.messageKey || 'comingSoonMessage'}">
                    We're working hard to bring you amazing content. Stay tuned!
                </p>
                ${config.showNotifyButton ? `
                    <button onclick="subscribeToUpdates('${config.section}')" 
                            class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition inline-flex items-center gap-2">
                        <i class="fas fa-bell"></i>
                        <span data-lang-key="notifyMe">Notify Me</span>
                    </button>
                ` : ''}
            </div>
        </div>
    `;
}

// Usage for different sections
function loadMoviesSection() {
    const moviesContainer = document.getElementById('movies-grid');
    
    if (!moviesData || moviesData.length === 0) {
        moviesContainer.innerHTML = createComingSoonSection({
            icon: 'fas fa-film',
            messageKey: 'moviesComingSoon',
            section: 'movies',
            showNotifyButton: true
        });
    } else {
        // Render movies
    }
}

function loadSportsSection() {
    const sportsContainer = document.getElementById('sports-grid');
    
    if (!sportsData || sportsData.length === 0) {
        sportsContainer.innerHTML = createComingSoonSection({
            icon: 'fas fa-basketball-ball',
            messageKey: 'sportsComingSoon',
            section: 'sports',
            showNotifyButton: true
        });
    } else {
        // Render sports
    }
}

function loadChallengesSection() {
    const challengesContainer = document.getElementById('challenges-grid');
    
    if (!challengesData || challengesData.length === 0) {
        challengesContainer.innerHTML = createComingSoonSection({
            icon: 'fas fa-trophy',
            messageKey: 'challengesComingSoon',
            section: 'challenges',
            showNotifyButton: true
        });
    } else {
        // Render challenges
    }
}
```

### Add Translation Keys
```javascript
// Add to window.translations.en
comingSoonTitle: "Coming Soon",
comingSoonMessage: "We're working hard to bring you amazing content. Stay tuned!",
moviesComingSoon: "Exciting movies are on their way! Check back soon for our latest additions.",
sportsComingSoon: "Get ready for thrilling sports content! Coming soon to Soundora.",
challengesComingSoon: "Amazing challenges await! We're preparing something special for you.",
sndComingSoon: "Exclusive SND Originals are in production. Be the first to watch!",
notifyMe: "Notify Me When Available",

// Add to window.translations.ru
comingSoonTitle: "Скоро",
comingSoonMessage: "Мы работаем над добавлением отличного контента. Следите за обновлениями!",
moviesComingSoon: "Новые захватывающие фильмы уже в пути! Загляните позже.",
sportsComingSoon: "Готовьтесь к захватывающему спортивному контенту! Скоро на Soundora.",
challengesComingSoon: "Вас ждут потрясающие испытания! Мы готовим для вас нечто особенное.",
sndComingSoon: "Эксклюзивные SND Оригиналы в производстве. Будьте первыми зрителями!",
notifyMe: "Уведомить о появлении",

// Add to window.translations.uz
comingSoonTitle: "Tez orada",
comingSoonMessage: "Biz ajoyib kontent qo'shish ustida ishlayapmiz. Yangiliklar uchun kuzatib boring!",
moviesComingSoon: "Qiziqarli filmlar yo'lda! Tez orada qaytib keling.",
sportsComingSoon: "Hayajonli sport kontenti tayyorlanmoqda! Soundora'da tez orada.",
challengesComingSoon: "Ajoyib musobaqalar sizni kutmoqda! Siz uchun maxsus narsa tayyorlayapmiz.",
sndComingSoon: "Eksklyuziv SND Originallari ishlab chiqilmoqda. Birinchi tomoshabinlar bo'ling!",
notifyMe: "Chiqganda xabar bering",
```

---

## 3. Search UX Improvements

### Improved No Results State
```javascript
function displayNoResults(searchTerm) {
    const container = document.getElementById('search-results');
    
    // Remove any error styling from search input
    const searchInput = document.getElementById('search-input');
    searchInput.classList.remove('border-red-500', 'border-red-600');
    searchInput.classList.add('border-gray-600'); // Neutral border
    
    const html = `
        <div class="no-results-state col-span-full flex flex-col items-center justify-center py-16 px-4">
            <div class="mb-6">
                <i class="fas fa-search fa-4x text-gray-600"></i>
            </div>
            <h3 class="text-2xl font-bold text-white mb-2" data-lang-key="noResultsTitle">
                No results found
            </h3>
            <p class="text-gray-400 mb-4 text-center max-w-md" data-lang-key="noResultsMessage">
                We couldn't find any content matching "${escapeHtml(searchTerm)}"
            </p>
            <div class="text-gray-500 text-sm text-center max-w-md">
                <p data-lang-key="searchSuggestions">Try:</p>
                <ul class="list-disc list-inside mt-2 space-y-1">
                    <li data-lang-key="searchTip1">Using different keywords</li>
                    <li data-lang-key="searchTip2">Checking your spelling</li>
                    <li data-lang-key="searchTip3">Using more general terms</li>
                    <li data-lang-key="searchTip4">Browsing categories instead</li>
                </ul>
            </div>
            <button onclick="clearSearch()" 
                    class="mt-6 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition">
                <span data-lang-key="clearSearch">Clear Search</span>
            </button>
        </div>
    `;
    
    container.innerHTML = html;
    updateAllTranslations(); // Update new translation keys
}

function clearSearch() {
    const searchInput = document.getElementById('search-input');
    searchInput.value = '';
    searchInput.classList.remove('border-red-500');
    searchInput.focus();
    // Return to default view
    loadFeaturedContent();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
```

### Add Translation Keys
```javascript
// English
noResultsTitle: "No results found",
noResultsMessage: "We couldn't find any content matching your search",
searchSuggestions: "Try:",
searchTip1: "Using different keywords",
searchTip2: "Checking your spelling",
searchTip3: "Using more general terms",
searchTip4: "Browsing categories instead",
clearSearch: "Clear Search",

// Russian
noResultsTitle: "Ничего не найдено",
noResultsMessage: "Мы не смогли найти контент, соответствующий вашему запросу",
searchSuggestions: "Попробуйте:",
searchTip1: "Использовать другие ключевые слова",
searchTip2: "Проверить правописание",
searchTip3: "Использовать более общие термины",
searchTip4: "Просмотреть категории",
clearSearch: "Очистить поиск",

// Uzbek
noResultsTitle: "Natija topilmadi",
noResultsMessage: "Qidiruv bo'yicha hech narsa topilmadi",
searchSuggestions: "Sinab ko'ring:",
searchTip1: "Boshqa kalit so'zlardan foydalaning",
searchTip2: "Imloni tekshiring",
searchTip3: "Umumiy atamalardan foydalaning",
searchTip4: "Kategoriyalarni ko'rib chiqing",
clearSearch: "Qidiruvni tozalash",
```

---

## 4. Login Prompts for Guests

### Modal Component
```javascript
// Create modal overlay
function createLoginPromptModal(config) {
    const modalId = 'login-prompt-modal';
    
    // Remove existing modal if any
    const existing = document.getElementById(modalId);
    if (existing) existing.remove();
    
    const modal = document.createElement('div');
    modal.id = modalId;
    modal.className = 'fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-75 backdrop-blur-sm';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-labelledby', 'modal-title');
    
    modal.innerHTML = `
        <div class="bg-gray-900 rounded-xl shadow-2xl max-w-md w-full p-8 relative border border-gray-800 transform transition-all">
            <button onclick="closeLoginPrompt()" 
                    class="absolute top-4 right-4 text-gray-400 hover:text-white transition"
                    aria-label="Close dialog">
                <i class="fas fa-times text-xl"></i>
            </button>
            
            <div class="text-center">
                <div class="mb-6 inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-500 bg-opacity-20">
                    <i class="${config.icon || 'fas fa-lock'} fa-2x text-blue-500"></i>
                </div>
                
                <h2 id="modal-title" class="text-2xl font-bold text-white mb-3">
                    ${config.title || 'Login Required'}
                </h2>
                
                <p class="text-gray-400 mb-8 leading-relaxed">
                    ${config.message || 'Please log in to access this feature'}
                </p>
                
                <div class="flex flex-col gap-3">
                    <button onclick="navigateToLogin()" 
                            class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition flex items-center justify-center gap-2">
                        <i class="fas fa-sign-in-alt"></i>
                        <span data-lang-key="login">Log In</span>
                    </button>
                    
                    <button onclick="navigateToRegister()" 
                            class="w-full bg-gray-800 hover:bg-gray-700 border border-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition flex items-center justify-center gap-2">
                        <i class="fas fa-user-plus"></i>
                        <span data-lang-key="registerNow">Sign Up</span>
                    </button>
                    
                    <button onclick="closeLoginPrompt()" 
                            class="w-full text-gray-400 hover:text-white font-medium py-2 transition">
                        <span data-lang-key="continueBrowsing">Continue Browsing</span>
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Update translations for newly added elements
    updateAllTranslations();
    
    // Trap focus in modal
    trapFocus(modal);
    
    // Close on Escape key
    document.addEventListener('keydown', handleEscapeKey);
    
    return modal;
}

function closeLoginPrompt() {
    const modal = document.getElementById('login-prompt-modal');
    if (modal) {
        modal.remove();
        document.removeEventListener('keydown', handleEscapeKey);
    }
}

function handleEscapeKey(e) {
    if (e.key === 'Escape') {
        closeLoginPrompt();
    }
}

function trapFocus(element) {
    const focusableElements = element.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];
    
    element.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            if (e.shiftKey && document.activeElement === firstFocusable) {
                e.preventDefault();
                lastFocusable.focus();
            } else if (!e.shiftKey && document.activeElement === lastFocusable) {
                e.preventDefault();
                firstFocusable.focus();
            }
        }
    });
    
    firstFocusable.focus();
}

// Usage examples
function handleFavoritesClick() {
    if (!isUserLoggedIn()) {
        createLoginPromptModal({
            icon: 'fas fa-heart',
            title: translations[currentLanguage].favoritesTitle || 'My Favorites',
            message: translations[currentLanguage].favoritesRequireLogin || 'Please log in to view and manage your favorite content.'
        });
        return;
    }
    // Navigate to favorites
    showPage('favorites');
}

function handleProfileClick() {
    if (!isUserLoggedIn()) {
        createLoginPromptModal({
            icon: 'fas fa-user-circle',
            title: translations[currentLanguage].profileTitle || 'Your Profile',
            message: translations[currentLanguage].profileRequiresLogin || 'Log in to access your profile and personalized settings.'
        });
        return;
    }
    // Navigate to profile
    showPage('profile');
}

function handleSupportClick() {
    if (!isUserLoggedIn()) {
        createLoginPromptModal({
            icon: 'fas fa-headphones',
            title: translations[currentLanguage].supportTitle || 'Support Chat',
            message: translations[currentLanguage].supportRequiresLogin || 'Please log in to chat with our support team.'
        });
        return;
    }
    // Open support chat
    openSupportChat();
}

function handleNotificationClick() {
    if (!isUserLoggedIn()) {
        createLoginPromptModal({
            icon: 'fas fa-bell',
            title: translations[currentLanguage].notificationsTitle || 'Notifications',
            message: translations[currentLanguage].notificationsRequireLogin || 'Log in to view your notifications and updates.'
        });
        return;
    }
    // Show notifications
    openNotifications();
}
```

### Add Translation Keys
```javascript
// English
favoritesTitle: "My Favorites",
favoritesRequireLogin: "Please log in to view and manage your favorite content.",
profileTitle: "Your Profile",
profileRequiresLogin: "Log in to access your profile and personalized settings.",
supportTitle: "Support Chat",
supportRequiresLogin: "Please log in to chat with our support team.",
notificationsTitle: "Notifications",
notificationsRequireLogin: "Log in to view your notifications and updates.",
continueBrowsing: "Continue Browsing",

// Russian
favoritesTitle: "Мои избранные",
favoritesRequireLogin: "Войдите, чтобы просматривать и управлять избранным контентом.",
profileTitle: "Ваш профиль",
profileRequiresLogin: "Войдите, чтобы получить доступ к профилю и персональным настройкам.",
supportTitle: "Чат поддержки",
supportRequiresLogin: "Войдите, чтобы общаться с нашей службой поддержки.",
notificationsTitle: "Уведомления",
notificationsRequireLogin: "Войдите, чтобы просматривать уведомления и обновления.",
continueBrowsing: "Продолжить просмотр",

// Uzbek
favoritesTitle: "Mening sevimlilarim",
favoritesRequireLogin: "Sevimli kontentingizni ko'rish va boshqarish uchun tizimga kiring.",
profileTitle: "Sizning profilingiz",
profileRequiresLogin: "Profil va shaxsiy sozlamalarga kirish uchun tizimga kiring.",
supportTitle: "Qo'llab-quvvatlash chati",
supportRequiresLogin: "Qo'llab-quvvatlash xizmatimiz bilan suhbatlashish uchun tizimga kiring.",
notificationsTitle: "Bildirishnomalar",
notificationsRequireLogin: "Bildirishnomalar va yangiliklarni ko'rish uchun tizimga kiring.",
continueBrowsing: "Ko'rishda davom etish",
```

---

## 5. Accessibility Enhancements

### Focus Indicators (CSS)
```css
/* Global focus styles */
*:focus {
    outline: 2px solid #3B82F6;
    outline-offset: 2px;
}

/* Custom focus for buttons */
button:focus,
a:focus {
    outline: 2px solid #3B82F6;
    outline-offset: 2px;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
}

/* Focus for form inputs */
input:focus,
select:focus,
textarea:focus {
    outline: 2px solid #3B82F6;
    outline-offset: 0;
    border-color: #3B82F6;
}

/* Skip to main content link */
.skip-to-main {
    position: absolute;
    left: -9999px;
    z-index: 9999;
    padding: 1rem 2rem;
    background: #3B82F6;
    color: white;
    text-decoration: none;
    font-weight: 600;
    border-radius: 0.5rem;
}

.skip-to-main:focus {
    left: 50%;
    transform: translateX(-50%);
    top: 1rem;
}

/* Screen reader only content */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
}

.sr-only-focusable:focus {
    position: static;
    width: auto;
    height: auto;
    padding: inherit;
    margin: inherit;
    overflow: visible;
    clip: auto;
    white-space: normal;
}
```

### Enhanced HTML with ARIA Labels
```html
<!-- Skip to main content -->
<a href="#main-content" class="skip-to-main">Skip to main content</a>

<!-- Navigation with proper ARIA -->
<nav aria-label="Main navigation" role="navigation">
    <ul class="nav-list">
        <li>
            <a href="#home" 
               aria-current="page" 
               aria-label="Go to home page">
                <i class="fas fa-home" aria-hidden="true"></i>
                <span>Home</span>
            </a>
        </li>
        <li>
            <a href="#series" 
               aria-label="Browse series">
                <i class="fas fa-tv" aria-hidden="true"></i>
                <span>Series</span>
            </a>
        </li>
    </ul>
</nav>

<!-- Search button with label -->
<button class="search-button" 
        aria-label="Search for movies and series"
        onclick="handleSearchClick()">
    <i class="fas fa-search" aria-hidden="true"></i>
    <span class="sr-only">Search</span>
</button>

<!-- Notification button with count -->
<button class="notification-button" 
        aria-label="Notifications: 3 new"
        onclick="handleNotificationClick()">
    <i class="fas fa-bell" aria-hidden="true"></i>
    <span class="notification-badge" aria-hidden="true">3</span>
    <span class="sr-only">You have 3 new notifications</span>
</button>

<!-- Movie card with proper structure -->
<article class="movie-card" role="article" aria-labelledby="movie-title-123">
    <img src="poster.jpg" alt="Movie poster for Inception" loading="lazy">
    <div class="movie-info">
        <h3 id="movie-title-123">Inception</h3>
        <div class="movie-meta">
            <span class="rating" aria-label="Rating: 8.8 out of 10">
                <i class="fas fa-star" aria-hidden="true"></i>
                8.8
            </span>
            <span class="year">2010</span>
        </div>
        <button class="play-button" 
                aria-label="Play Inception"
                onclick="playMovie('123')">
            <i class="fas fa-play" aria-hidden="true"></i>
            <span data-lang-key="play">Play</span>
        </button>
    </div>
</article>

<!-- Form with proper labels -->
<form role="form" aria-labelledby="login-form-title">
    <h2 id="login-form-title">Login to Your Account</h2>
    
    <div class="form-group">
        <label for="email-input">
            Email Address
            <span class="required" aria-label="required">*</span>
        </label>
        <input type="email" 
               id="email-input" 
               name="email"
               required
               aria-required="true"
               aria-describedby="email-error"
               placeholder="Enter your email">
        <span id="email-error" class="error-message" role="alert"></span>
    </div>
    
    <div class="form-group">
        <label for="password-input">
            Password
            <span class="required" aria-label="required">*</span>
        </label>
        <input type="password" 
               id="password-input"
               name="password"
               required
               aria-required="true"
               aria-describedby="password-error"
               placeholder="Enter your password">
        <span id="password-error" class="error-message" role="alert"></span>
    </div>
    
    <button type="submit" class="submit-button">
        Log In
    </button>
</form>
```

---

## 6. Registration Form Fixes

### Updated Registration Form HTML
```html
<form id="registration-form" class="registration-form" role="form" aria-labelledby="register-title">
    <h2 id="register-title" data-lang-key="registerTitle">Create Account</h2>
    
    <!-- Full Name -->
    <div class="form-group">
        <label for="reg-fullname" data-lang-key="fullName">Full Name</label>
        <input type="text" 
               id="reg-fullname" 
               name="fullname"
               required
               aria-required="true"
               data-lang-key-placeholder="fullNamePlaceholder"
               placeholder="Enter your full name"
               autocomplete="name">
    </div>
    
    <!-- Email -->
    <div class="form-group">
        <label for="reg-email" data-lang-key="email">Email</label>
        <input type="email" 
               id="reg-email" 
               name="email"
               required
               aria-required="true"
               data-lang-key-placeholder="emailPlaceholder"
               placeholder="Enter your email"
               autocomplete="email">
    </div>
    
    <!-- Password -->
    <div class="form-group">
        <label for="reg-password" data-lang-key="password">Password</label>
        <div class="password-input-wrapper">
            <input type="password" 
                   id="reg-password" 
                   name="password"
                   required
                   aria-required="true"
                   minlength="8"
                   data-lang-key-placeholder="passwordPlaceholder"
                   placeholder="Create a password"
                   autocomplete="new-password">
            <button type="button" 
                    class="toggle-password"
                    aria-label="Toggle password visibility"
                    onclick="togglePasswordVisibility('reg-password')">
                <i class="fas fa-eye"></i>
            </button>
        </div>
        <p class="form-hint" data-lang-key="passwordHint">
            At least 8 characters
        </p>
    </div>
    
    <!-- Confirm Password -->
    <div class="form-group">
        <label for="reg-confirm-password" data-lang-key="confirmPassword">
            Confirm Password
        </label>
        <input type="password" 
               id="reg-confirm-password" 
               name="confirm_password"
               required
               aria-required="true"
               data-lang-key-placeholder="confirmPasswordPlaceholder"
               placeholder="Confirm your password"
               autocomplete="new-password">
    </div>
    
    <!-- Region Selector -->
    <div class="form-group">
        <label for="reg-region" data-lang-key="region">Region</label>
        <select id="reg-region" 
                name="region"
                required
                aria-required="true"
                class="form-select">
            <option value="" data-lang-key="selectRegion">Select your region</option>
            <option value="UZ">🇺🇿 Uzbekistan</option>
            <option value="KZ">🇰🇿 Kazakhstan</option>
            <option value="KG">🇰🇬 Kyrgyzstan</option>
            <option value="TJ">🇹🇯 Tajikistan</option>
            <option value="TM">🇹🇲 Turkmenistan</option>
            <option value="RU">🇷🇺 Russia</option>
            <option value="OTHER">🌍 Other</option>
        </select>
    </div>
    
    <!-- Recovery Word (Optional) -->
    <div class="form-group">
        <label for="reg-recovery" data-lang-key="secretWordLabel">
            Recovery Word (Optional)
        </label>
        <input type="text" 
               id="reg-recovery" 
               name="recovery_word"
               data-lang-key-placeholder="secretWordPlaceholder"
               placeholder="For account recovery"
               autocomplete="off">
        <p class="form-hint" data-lang-key="recoveryHint">
            Choose a word you'll remember to help recover your account
        </p>
    </div>
    
    <!-- Terms and Conditions -->
    <div class="form-group checkbox-group">
        <label class="checkbox-label">
            <input type="checkbox" 
                   id="reg-terms" 
                   name="terms"
                   required
                   aria-required="true">
            <span data-lang-key="agreeToTerms">
                I agree to the 
                <a href="#terms" class="link">Terms of Service</a> 
                and 
                <a href="#privacy" class="link">Privacy Policy</a>
            </span>
        </label>
    </div>
    
    <!-- Submit Button -->
    <button type="submit" class="submit-button w-full">
        <span data-lang-key="registerNow">Create Account</span>
    </button>
    
    <!-- Already have account link -->
    <p class="form-footer">
        <span data-lang-key="alreadyHaveAccount">Already have an account?</span>
        <a href="#login" class="link" data-lang-key="loginNow">Log in</a>
    </p>
</form>
```

### Password Toggle Functionality
```javascript
function togglePasswordVisibility(inputId) {
    const input = document.getElementById(inputId);
    const button = input.parentElement.querySelector('.toggle-password');
    const icon = button.querySelector('i');
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
        button.setAttribute('aria-label', 'Hide password');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
        button.setAttribute('aria-label', 'Show password');
    }
}
```

### Form Validation
```javascript
document.getElementById('registration-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const password = document.getElementById('reg-password').value;
    const confirmPassword = document.getElementById('reg-confirm-password').value;
    
    // Check password match
    if (password !== confirmPassword) {
        showError('reg-confirm-password', translations[currentLanguage].passwordsDoNotMatch);
        return;
    }
    
    // Check password strength
    if (password.length < 8) {
        showError('reg-password', translations[currentLanguage].passwordTooShort);
        return;
    }
    
    // All validations passed - submit form
    submitRegistration(new FormData(this));
});

function showError(inputId, message) {
    const input = document.getElementById(inputId);
    const errorElement = document.createElement('span');
    errorElement.className = 'error-message';
    errorElement.textContent = message;
    errorElement.setAttribute('role', 'alert');
    
    // Remove existing error if any
    const existingError = input.parentElement.querySelector('.error-message');
    if (existingError) existingError.remove();
    
    // Add new error
    input.parentElement.appendChild(errorElement);
    input.classList.add('error');
    input.focus();
}
```

---

## Implementation Checklist

- [ ] Add language switcher to header
- [ ] Implement coming soon sections for empty content
- [ ] Update search to show neutral "no results" state
- [ ] Add login prompt modals for guest users
- [ ] Implement accessibility improvements (ARIA labels, focus indicators)
- [ ] Fix registration form (placeholders, labels, validation)
- [ ] Test all changes across browsers (Chrome, Firefox, Safari, Edge)
- [ ] Test with screen readers (NVDA, JAWS, VoiceOver)
- [ ] Test keyboard navigation
- [ ] Update all translation files
- [ ] Create documentation for content management

---

## Testing Guide

### Manual Testing
1. **Language Switcher**: Switch between EN, RU, UZ and verify all text updates
2. **Empty Sections**: Navigate to Movies, Sports, Challenges - verify "coming soon" messages
3. **Search**: Search for non-existent content - verify friendly message (no red errors)
4. **Guest Users**: Click Favorites, Profile, Support without login - verify modals appear
5. **Registration**: Fill form with various inputs - verify validation works
6. **Accessibility**: Tab through entire page - verify focus indicators are visible

### Automated Testing
```javascript
// Example test suite (using Jest or similar)
describe('Language Switcher', () => {
    test('should switch language when option clicked', () => {
        switchLanguage('ru');
        expect(window.currentLanguage).toBe('ru');
        expect(localStorage.getItem('preferredLanguage')).toBe('ru');
    });
});

describe('Login Prompts', () => {
    test('should show modal when guest clicks favorites', () => {
        handleFavoritesClick();
        const modal = document.getElementById('login-prompt-modal');
        expect(modal).toBeTruthy();
    });
});
```

---

## Conclusion

This implementation guide provides all the code needed to address the issues identified in the Soundora platform audit. Each section includes:

- Complete, production-ready code
- Proper accessibility attributes
- Multilingual support
- Best practices and modern web standards

Follow the implementation checklist and testing guide to ensure all improvements are properly deployed and verified.
