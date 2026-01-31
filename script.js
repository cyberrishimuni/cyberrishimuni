// Add active state based on current page
document.addEventListener('DOMContentLoaded', function() {
  const currentPath = window.location.pathname;
  const navItems = document.querySelectorAll('.nav-item');
  
  navItems.forEach(item => {
    const href = item.getAttribute('href');
    if (href && currentPath.includes(href.replace('/', ''))) {
      item.classList.add('active');
    }
  });

  // Close dropdown when clicking outside
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.dropdown')) {
      document.querySelectorAll('.dropdown-menu').forEach(menu => {
        menu.style.opacity = '0';
        menu.style.visibility = 'hidden';
      });
    }
  });
});