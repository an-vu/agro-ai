// main.js — handles all JS logic for the frontend pages

document.addEventListener("DOMContentLoaded", function () {
  // -----------------------------------------
  // GLOBAL: Bootstrap popovers and tooltips
  // Used in: all pages
  // -----------------------------------------
  $('[data-toggle="popover"]').popover();
  $('[data-toggle="tooltip"]').tooltip();

  // -----------------------------------------
  // INDEX.HTML: Navbar icon toggle
  // -----------------------------------------
  const firstButton = document.querySelector('.first-button');
  if (firstButton) {
    firstButton.addEventListener('click', () => {
      document.querySelector('.animated-icon1')?.classList.toggle('open');
    });
  }

  // -----------------------------------------
  // INTERMEDIATE / FINAL / FEEDBACK: Image modal preview
  // -----------------------------------------
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

  // -----------------------------------------
  // FINAL.HTML: Update disagreement counts
  // -----------------------------------------
  const healthyCount = document.getElementById('healthyselected');
  const unhealthyCount = document.getElementById('unhealthyselected');

  if (healthyCount && unhealthyCount) {
    const updateCount = () => {
      healthyCount.innerHTML = document.querySelectorAll('input[name=healthy]:checked').length;
      unhealthyCount.innerHTML = document.querySelectorAll('input[name=unhealthy]:checked').length;
    };

    document.querySelectorAll("input[name=healthy]").forEach(i => i.onclick = updateCount);
    document.querySelectorAll("input[name=unhealthy]").forEach(i => i.onclick = updateCount);
  }

  // -----------------------------------------
  // FINAL.HTML: Submit feedback and navigate to /feedback/
  // -----------------------------------------
  const submitBtn = document.getElementById('img');
  if (submitBtn) {
    submitBtn.addEventListener('click', function () {
      const hList = [], uList = [], hConf = [], uConf = [];

      $("input[name=healthy]:checked").each(function () {
        hList.push($(this).val());
        hConf.push($(this).attr("conf-value"));
      });
      $("input[name=unhealthy]:checked").each(function () {
        uList.push($(this).val());
        uConf.push($(this).attr("conf-value"));
      });

      window.location.href = `/feedback/${hList.length ? hList : "null"}/${uList.length ? uList : "null"}/${hConf.length ? hConf : "0"}/${uConf.length ? uConf : "0"}`;
    });
  }
});
