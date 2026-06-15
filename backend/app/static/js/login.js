document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('loginForm');
  const errorDiv = document.getElementById('errorMessage');
  const submitBtn = form.querySelector('button[type="submit"]');

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    errorDiv.classList.add('hidden');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Ingresando...';

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          usuario: document.getElementById('usuario').value.trim(),
          password: document.getElementById('password').value,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Error al iniciar sesión');
      }

      localStorage.setItem('token', data.access_token);
      localStorage.setItem('usuario', data.usuario);
      localStorage.setItem('rol', data.rol);
      if (data.nombre_completo) {
        localStorage.setItem('nombre_completo', data.nombre_completo);
      }

      window.location.href = '/dashboard';

    } catch (err) {
      errorDiv.textContent = err.message;
      errorDiv.classList.remove('hidden');
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Iniciar Sesión';
    }
  });
});
