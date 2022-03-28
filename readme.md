# django-links

URL shortener website (python - django project) create a short and unique links. You can test functionality (the final link is not short because the test host is long): https://lestec.pythonanywhere.com/

Features:

- accounts for users (registration, login, logout)
- cut links to unique short link (for all users)
- short link redirect to original link
- individual page with links with: search form (searches from original link), ability delete links, clicks count, time created (for registered users)
- basic interface with appearance of pages (used bootstrap)

<img src="https://github.com/lestec-al/django-links/raw/master/pic-readme-1.jpg" />
<img src="https://github.com/lestec-al/django-links/raw/master/pic-readme-2.jpg" />

To run on your local server, you need:
- install Python (v3.9 or higher)
- install all from requirements.txt (django, django-crispy-forms)