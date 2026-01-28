import os
import subprocess

def create_frontend():
    print("Initializing Frontend...")
    
    # Check if frontend dir exists
    if os.path.exists("frontend"):
        print("Frontend directory already exists. Skipping creation.")
        return

    # Create directory structure manually since 'npx create-vite' is interactive
    os.makedirs("frontend/src/components", exist_ok=True)
    os.makedirs("frontend/src/pages", exist_ok=True)
    os.makedirs("frontend/public", exist_ok=True)

    # Create package.json
    package_json = """
{
  "name": "medsy-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.0",
    "tailwindcss": "^3.4.0",
    "lucide-react": "^0.300.0" 
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.4.0",
    "vite": "^5.0.8"
  }
}
"""
    with open("frontend/package.json", "w") as f:
        f.write(package_json.strip())

    # Create vite.config.js
    vite_config = """
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
"""
    with open("frontend/vite.config.js", "w") as f:
        f.write(vite_config.strip())

    # Create index.html
    index_html = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Medsy Companion</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""
    with open("frontend/index.html", "w") as f:
        f.write(index_html.strip())

    # Create src/main.jsx
    main_jsx = """
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
"""
    with open("frontend/src/main.jsx", "w") as f:
        f.write(main_jsx.strip())

    # Create src/index.css (Tailwind)
    index_css = """
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
    background-color: #f3f4f6;
}
"""
    with open("frontend/src/index.css", "w") as f:
        f.write(index_css.strip())

    print("Frontend structure created successfully.")

if __name__ == "__main__":
    create_frontend()
