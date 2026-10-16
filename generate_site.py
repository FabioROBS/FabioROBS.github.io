import os
import shutil
import markdown
import yaml

def build():
    site_dir = "_site"
    if os.path.exists(site_dir):
        shutil.rmtree(site_dir)
    os.makedirs(site_dir, exist_ok=True)

    # Copy static assets
    for folder in ['assets', 'images', 'files']:
        if os.path.exists(folder):
            shutil.copytree(folder, os.path.join(site_dir, folder))

    # Read config
    with open('_config.yml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    author = config.get('author', {})
    site_title = config.get('title', 'Fabio Solia')
    author_name = author.get('name', 'Fabio Solia')
    author_bio = author.get('bio', '')
    author_location = author.get('location', '')
    author_employer = author.get('employer', '')
    author_email = author.get('email', '')
    author_github = author.get('github', '')
    author_linkedin = author.get('linkedin', '')

    base_html = """<!doctype html>
<html lang="en" class="no-js">
  <head>
    <meta charset="utf-8">
    <!-- begin SEO -->
    <title>{page_title} - {site_title}</title>
    <meta property="og:locale" content="en-US">
    <meta property="og:site_name" content="{site_title}">
    <meta property="og:title" content="{page_title}">
    <meta property="og:url" content="https://fabiorobs.github.io{canonical_path}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script> document.documentElement.className = document.documentElement.className.replace(/\\bno-js\\b/g, '') + ' js '; </script>
    <!-- For all browsers -->
    <link rel="stylesheet" href="/assets/css/main.css">
    <link rel="stylesheet" href="/assets/css/academicons.css"/>
    <link rel="apple-touch-icon" sizes="180x180" href="/images/apple-touch-icon-180x180.png"/>
    <link rel="icon" type="image/svg+xml" href="/images/favicon.svg"/>
    <link rel="icon" type="image/png" href="/images/favicon-32x32.png" sizes="32x32"/>
    <link rel="icon" type="image/png" href="/images/favicon-192x192.png" sizes="192x192"/>
    <link rel="manifest" href="/images/manifest.json"/>
    <link rel="icon" href="/images/favicon.ico"/>
    <meta name="theme-color" content="#ffffff"/>
  </head>
  <body>
    <!--[if lt IE 9]><div class="notice--danger align-center" style="margin: 0;">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> to improve your experience.</div><![endif]-->
    <div class="masthead">
      <div class="masthead__inner-wrap">
        <div class="masthead__menu">
          <nav id="site-nav" class="greedy-nav">
            <button><span class="navicon"></span></button>
            <ul class="visible-links">
              <li class="masthead__menu-item masthead__menu-item--lg persist"><a href="/">{site_title}</a></li>
              <li class="masthead__menu-item {pub_active}"><a href="/publications/">Publications</a></li>
              <li class="masthead__menu-item {cv_active}"><a href="/cv/">CV</a></li>
              <li id="theme-toggle" class="masthead__menu-item persist tail">
                <a role="button" aria-labelledby="theme-icon"><i id="theme-icon" class="fa-solid fa-sun" aria-hidden="true" title="toggle theme"></i></a>
              </li>
            </ul>
            <ul class="hidden-links hidden"></ul>
          </nav>
        </div>
      </div>
    </div>

    <div id="main" role="main">
      <div class="sidebar sticky">
        <div itemscope itemtype="http://schema.org/Person">
          <div class="author__avatar">
            <img src="/images/profile.png" class="author__avatar" alt="{author_name}" fetchpriority="high" />
          </div>
          <div class="author__content">
            <h3 class="author__name">{author_name}</h3>
            <p class="author__bio">{author_bio}</p>
          </div>
          <div class="author__urls-wrapper">
            <button class="btn btn--inverse">Follow</button>
            <ul class="author__urls social-icons">
              {location_li}
              {employer_li}
              {email_li}
              {github_li}
              {linkedin_li}
            </ul>
          </div>
        </div>
      </div>

      <article class="page" itemscope itemtype="http://schema.org/CreativeWork">
        <meta itemprop="headline" content="{page_title}">
        <div class="page__inner-wrap">
          <header>
            <h1 class="page__title" itemprop="headline">{page_title}</h1>
          </header>
          <section class="page__content" itemprop="text">
            {page_body}
          </section>
        </div>
      </article>
    </div>

    <div class="page__footer">
      <footer>
        <div class="page__footer-follow">
          <ul class="social-icons">
            <li><strong>Follow:</strong></li>
            <li><a href="https://github.com/{author_github}" target="_blank"><i class="fab fa-github" aria-hidden="true"></i> GitHub</a></li>
            <li><a href="https://www.linkedin.com/in/{author_linkedin}" target="_blank"><i class="fab fa-linkedin" aria-hidden="true"></i> LinkedIn</a></li>
          </ul>
        </div>
        <div class="page__footer-copyright">
          &copy; 2026 {author_name}. Powered by <a href="https://jekyllrb.com" rel="nofollow">Jekyll</a> &amp; <a href="https://github.com/academicpages/academicpages.github.io">AcademicPages</a>.<br />
        </div>
      </footer>
    </div>

    <script type="module" src="/assets/js/main.min.js"></script>
  </body>
</html>
"""

    location_li = f'<li class="author__desktop"><i class="fas fa-fw fa-location-dot icon-pad-right" aria-hidden="true"></i>{author_location}</li>' if author_location else ''
    employer_li = f'<li class="author__desktop"><i class="fas fa-fw fa-building-columns icon-pad-right" aria-hidden="true"></i>{author_employer}</li>' if author_employer else ''
    email_li = f'<li><a href="mailto:{author_email}"><i class="fas fa-fw fa-envelope icon-pad-right" aria-hidden="true"></i>Email</a></li>' if author_email else ''
    github_li = f'<li><a href="https://github.com/{author_github}" target="_blank"><i class="fab fa-fw fa-github icon-pad-right" aria-hidden="true"></i>GitHub</a></li>' if author_github else ''
    linkedin_li = f'<li><a href="https://www.linkedin.com/in/{author_linkedin}" target="_blank"><i class="fab fa-fw fa-linkedin icon-pad-right" aria-hidden="true"></i>LinkedIn</a></li>' if author_linkedin else ''

    # 1. Render Home / About Me
    with open('_pages/about.md', 'r', encoding='utf-8') as f:
        about_raw = f.read()
    # Strip frontmatter
    about_md = about_raw.split('---', 2)[-1].strip()
    about_html = markdown.markdown(about_md, extensions=['extra'])
    
    home_page = base_html.format(
        page_title="About Me",
        site_title=site_title,
        canonical_path="/",
        pub_active="",
        cv_active="",
        author_name=author_name,
        author_bio=author_bio,
        author_github=author_github,
        author_linkedin=author_linkedin,
        location_li=location_li,
        employer_li=employer_li,
        email_li=email_li,
        github_li=github_li,
        linkedin_li=linkedin_li,
        page_body=about_html
    )
    with open(os.path.join(site_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(home_page)

    # 2. Render CV
    with open('_pages/cv.md', 'r', encoding='utf-8') as f:
        cv_raw = f.read()
    cv_md = cv_raw.split('---', 2)[-1]
    cv_md = cv_md.replace('{% include base_path %}', '')
    cv_md = cv_md.replace('{{ base_path }}', '')
    cv_html = markdown.markdown(cv_md.strip(), extensions=['extra'])

    cv_page = base_html.format(
        page_title="Curriculum Vitae",
        site_title=site_title,
        canonical_path="/cv/",
        pub_active="",
        cv_active="active",
        author_name=author_name,
        author_bio=author_bio,
        author_github=author_github,
        author_linkedin=author_linkedin,
        location_li=location_li,
        employer_li=employer_li,
        email_li=email_li,
        github_li=github_li,
        linkedin_li=linkedin_li,
        page_body=cv_html
    )
    os.makedirs(os.path.join(site_dir, 'cv'), exist_ok=True)
    with open(os.path.join(site_dir, 'cv', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(cv_page)

    # 3. Render Publications
    with open('_pages/publications.html', 'r', encoding='utf-8') as f:
        pub_raw = f.read()
    pub_body = "<p>This page is under construction.</p>"
    
    pub_page = base_html.format(
        page_title="Publications",
        site_title=site_title,
        canonical_path="/publications/",
        pub_active="active",
        cv_active="",
        author_name=author_name,
        author_bio=author_bio,
        author_github=author_github,
        author_linkedin=author_linkedin,
        location_li=location_li,
        employer_li=employer_li,
        email_li=email_li,
        github_li=github_li,
        linkedin_li=linkedin_li,
        page_body=pub_body
    )
    os.makedirs(os.path.join(site_dir, 'publications'), exist_ok=True)
    with open(os.path.join(site_dir, 'publications', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(pub_page)

    print("Successfully built static site in _site/")

if __name__ == '__main__':
    build()
