document.getElementById('id_avatar').addEventListener('change', function() {
    alert(this.files[0].name);
  });