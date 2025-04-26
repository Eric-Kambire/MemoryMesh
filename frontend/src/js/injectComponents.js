// src/js/injectComponents.js

async function loadComponents() {
    const sidebar = await fetch('src/components/sidebar.html').then(res => res.text());
    const topbar = await fetch('src/components/topbar.html').then(res => res.text());
  
    document.getElementById('sidebar').innerHTML = sidebar;
    document.getElementById('topbar').innerHTML = topbar;
  }
  
  document.addEventListener('DOMContentLoaded', loadComponents);
  