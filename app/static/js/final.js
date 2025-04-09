document.addEventListener("DOMContentLoaded", function () {
    const healthyCount = document.getElementById('healthyselected');
    const unhealthyCount = document.getElementById('unhealthyselected');
  
    const updateCount = () => {
      healthyCount.innerHTML = document.querySelectorAll('input[name=healthy]:checked').length;
      unhealthyCount.innerHTML = document.querySelectorAll('input[name=unhealthy]:checked').length;
    };
  
    document.querySelectorAll("input[name=healthy]").forEach(i => i.onclick = updateCount);
    document.querySelectorAll("input[name=unhealthy]").forEach(i => i.onclick = updateCount);
  
    $('#img').on('click', function () {
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
  });
  