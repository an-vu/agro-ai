document.addEventListener("DOMContentLoaded", function () {
    // Bootstrap popover + tooltip
    $('[data-toggle="popover"]').popover();
    $('[data-toggle="tooltip"]').tooltip();
  
    // Navbar icon (used in index.html)
    const firstButton = document.querySelector('.first-button');
    if (firstButton) {
      firstButton.addEventListener('click', () => {
        document.querySelector('.animated-icon1')?.classList.toggle('open');
      });
    }
  
    // Modal preview (used in intermediate, final, feedback)
    const modal = document.querySelector(".modal");
    const modalImg = document.getElementById("imgset");
    if (modal && modalImg) {
      document.querySelectorAll(".img-thumbnail, .img-rounded").forEach(img => {
        img.onclick = () => {
          modal.style.display = "block";
          modalImg.src = img.src;
        };
      });
      document.querySelector(".close")?.addEventListener("click", () => {
        modal.style.display = "none";
      });
    }
  });
  