/* CV Extractor — main.js */
document.addEventListener('DOMContentLoaded', () => {
  const fileInput = document.getElementById('file-input');
  const fileCount = document.getElementById('file-count');
  const dropZone = document.getElementById('drop-zone');
  const form = document.getElementById('upload-form');
  const submitBtn = document.getElementById('submit-btn');
  const btnText = document.getElementById('btn-text');
  const errorEl = document.getElementById('error');

  function updateFileCount() {
    const n = fileInput.files.length;
    fileCount.textContent = n
      ? `${n} file${n !== 1 ? 's' : ''} selected`
      : '';
  }

  function showError(msg) {
    errorEl.textContent = msg;
    errorEl.hidden = false;
  }

  function clearError() {
    errorEl.hidden = true;
    errorEl.textContent = '';
  }

  fileInput.addEventListener('change', () => {
    clearError();
    updateFileCount();
  });

  dropZone.addEventListener('click', () => {
    fileInput.click();
  });

  dropZone.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      fileInput.click();
    }
  });

  dropZone.addEventListener('dragover', e => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.add('dragover');
  });

  dropZone.addEventListener('dragleave', e => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('dragover');
  });

  dropZone.addEventListener('drop', e => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove('dragover');
    fileInput.files = e.dataTransfer.files;
    updateFileCount();
  });

  form.addEventListener('submit', e => {
    clearError();
    if (!fileInput.files.length) {
      e.preventDefault();
      showError('Please select at least one file.');
      return;
    }
    submitBtn.disabled = true;
    btnText.innerHTML = '<span class="spinner"></span>Extracting…';
  });
});
