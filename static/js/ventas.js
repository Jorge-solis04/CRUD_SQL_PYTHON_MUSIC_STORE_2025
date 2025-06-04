
function mostrarProductos() {
  document.getElementById('select-cd').style.display = 'none';
  document.getElementById('select-vinyl').style.display = 'none';
  document.getElementById('select-casete').style.display = 'none';

  var formato = document.getElementById('formato').value;
  if (formato === 'cd') {
    document.getElementById('select-cd').style.display = '';
    document.getElementById('select-cd').name = 'idFormato';
    document.getElementById('select-vinyl').name = '';
    document.getElementById('select-casete').name = '';
  } else if (formato === 'vinyl') {
    document.getElementById('select-vinyl').style.display = '';
    document.getElementById('select-vinyl').name = 'idFormato';
    document.getElementById('select-cd').name = '';
    document.getElementById('select-casete').name = '';
  } else if (formato === 'casete') {
    document.getElementById('select-casete').style.display = '';
    document.getElementById('select-casete').name = 'idFormato';
    document.getElementById('select-cd').name = '';
    document.getElementById('select-vinyl').name = '';
  }
}
